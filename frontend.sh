#!/usr/bin/env bash
# usage:
#   run: `./frontend.sh`
#   run detached: `./frontend.sh detached`
#   kill detached: `./frontend.sh kill`
#   install: `./frontend.sh install`
#   update: `./frontend.sh update`
#   build: `./frontend.sh build`
#   types: `./frontend.sh types`


# -------------------------------------
# Check prereqs installed
# -------------------------------------
# determine if Windows
[[ $(uname -s) == MINGW64_NT* ]] && WINDOWS=true || WINDOWS=false

# Check universal requirements
hash node 2>/dev/null || { echo >&2 "Node.js must be installed."; exit 1; }
hash npm 2>/dev/null || { echo >&2 "NPM must be installed."; exit 1; }
hash yarn 2>/dev/null || { echo >&2 "Yarn must be installed."; exit 1; }

# Check non-Windows requirements
if [ "$WINDOWS" = false ] ; then
  hash lsof 2>/dev/null || { echo >&2 "lsof linux utility should be installed."; exit 1; }
fi

# Check Windows requirements
if [ "$WINDOWS" = true ] ; then
  hash netstat 2>/dev/null || { echo >&2 "netstat must be installed."; exit 1; }
  hash findstr 2>/dev/null || { echo >&2 "findstr must be installed."; exit 1; }
fi

# Check linux tools
support_linux_tools_error() {
  echo >&2 "$1 must be installed. If on PC, Git Bash should come installed with these!"
}
hash grep 2>/dev/null || { support_linux_tools_error "grep"; exit 1; }
hash awk 2>/dev/null || { support_linux_tools_error "awk"; exit 1; }
hash xargs 2>/dev/null || { support_linux_tools_error "xargs"; exit 1; }


# -------------------------------------
# Determine run option
# -------------------------------------

if [ $# -gt 0 ]; then
  flag=$1
fi;

main() {
  cd frontend/
  if [ "$flag" == "detached" ]; then
    run_detached
  elif [ "$flag" == "kill" ]; then
    kill_detached
  elif [ "$flag" == "install" ]; then
    install
  elif [ "$flag" == "update" ]; then
    update
  elif [ "$flag" == "build" ]; then
    build
  elif [ "$flag" == "types" ]; then
    check_types
  else
    run
  fi
  cd ../
}


# -------------------------------------
# Commands
# -------------------------------------

run() {
  yarn start
}

run_detached() {
  run &>/dev/null &
}

kill_detached() {
  if [ "$WINDOWS" = true ] ; then
    netstat -aon | findstr :3000 | awk '{ print $5 }' | xargs tskill
  else
    lsof -n -i4TCP:3000 | grep LISTEN | awk '{ print $2 }' | xargs kill
  fi
}

install() {
  yarn install
}

update() {
  yarn install
}

build() {
  yarn build
}

check_types() {
  yarn flow
}


main "$@"
