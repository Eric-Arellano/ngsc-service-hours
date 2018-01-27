#!/usr/bin/env bash
# usage:
#   run: `./backend.sh`
#   run detached: `./backend.sh detached`
#   kill detached: `./backend.sh kill`
#   install: `./backend.sh install`
#   types: `./backend.sh types`


# -------------------------------------
# Check prereqs installed & if Windows
# -------------------------------------
# determine if Windows
[[ $(uname -s) == MINGW64_NT* ]] && WINDOWS=true || WINDOWS=false

# Check non-Windows requirements
if [ "$WINDOWS" = false ] ; then
  hash python3 2>/dev/null || { echo >&2 "Python 3 must be installed."; exit 1; }
  hash lsof 2>/dev/null || { echo >&2 "lsof linux utility should be installed."; exit 1; }
fi

# Check Windows requirements
if [ "$WINDOWS" = true ] ; then
  hash python 2>/dev/null || { echo >&2 "Python must be installed and on your path."; exit 1; }
fi

# Check linux tools
support_linux_tools_error() {
  echo >&2 "$1 must be installed. If on PC, Git Bash should come installed with these!"
}
hash grep 2>/dev/null || { support_linux_tools_error grep; exit 1; }
hash awk 2>/dev/null || { support_linux_tools_error awk; exit 1; }
hash xargs 2>/dev/null || { support_linux_tools_error xargs; exit 1; }

# Venv helper
activate_venv() {
  if [ "$WINDOWS" = true ] ; then
    source backend/Scripts/activate
  else
    source backend/bin/activate
  fi
}

# Windows not implemented
check_windows_not_impl() {
  if [ "$WINDOWS" = true ] ; then
    echo >&2 "Feature not implemented yet for Windows! Hang tight."
    exit 1
  fi
}

# -------------------------------------
# Determine run option
# -------------------------------------

if [ $# -gt 0 ]; then
  flag=$1
fi;

main() {
  if [ "$flag" == "detached" ]; then
    run_detached
  elif [ "$flag" == "kill" ]; then
    kill_detached
  elif [ "$flag" == "install" ]; then
    install
  elif [ "$flag" == "types" ]; then
    check_types
  else
    run
  fi
}


# -------------------------------------
# Commands
# -------------------------------------

run() {
  activate_venv
  export FLASK_APP=backend/src/app.py
  flask run
}

run_detached() {
  check_windows_not_impl
  run &>/dev/null &
}

# TODO: add Windows support, no lsof command
kill_detached() {
  check_windows_not_impl
  lsof -n -i4TCP:5000 | grep LISTEN | awk '{ print $2 }' | xargs kill
}

install() {
  cd backend/
  if [ "$WINDOWS" = true ] ; then
    python -m venv ./
  else
    python3 -m venv ./
  fi
  cd ../
  activate_venv
  pip install -r requirements.txt
}

check_types() {
  activate_venv
  cd backend/
  mypy --strict-optional --ignore-missing-imports --package src
  cd ../
}


main "$@"