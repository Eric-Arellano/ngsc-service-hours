#!/usr/bin/env bash

# -----------------------------------
# Check pre-reqs installed
# -----------------------------------
# Check universal requirements
hash git 2>/dev/null || { echo >&2 "Git must be installed."; exit 1; }
hash heroku 2>/dev/null || { echo >&2 "Heroku CLI must be installed."; exit 1; }
hash jq 2>/dev/null || { echo >&2 "JQ must be installed. See https://stedolan.github.io/jq/"; exit 1; }

# Check linux tools
support_linux_tools_error() {
  echo >&2 "$1 must be installed. If on PC, please use Windows Subsytem for Linux."
}
hash curl 2>/dev/null || { support_linux_tools_error curl; exit 1; }
hash sed 2>/dev/null || { support_linux_tools_error sed; exit 1; }


# -----------------------------------
# Check for project updates 
# -----------------------------------
# Check on master branch
BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [[ "$BRANCH" != "master" ]]; then
  git checkout master
fi

# Check for clean local
if ! git diff-index --quiet HEAD --; then
    echo >&2 "Make sure the branch is clean before running this script."
    exit 1
fi

# Update from master
git fetch origin master
git merge --ff-only  # abort if merge required


# -----------------------------------
# Get new student info & save
# -----------------------------------
# Get student JSON
student_info=$(curl http://ngsc-app.org/api/demographics/all_students --silent)

# Save to file
echo $student_info | jq . > backend/src/student_ids.py  # pretty-prints json to file
first_line="student_ids = {"
sed -i '.bak' "1s/.*/$first_line/" backend/src/student_ids.py  # replaces first line with $first_line

# -----------------------------------
# Redeploy
# -----------------------------------
# Exit if no changes
if ! git diff-index --quiet HEAD --; then
    echo "There were no updates to student info."
    exit 0
fi

git add backend/src/student_ids.py
git commit -m 'update demographics'
git push origin master
git push heroku master