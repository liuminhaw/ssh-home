#!/bin/bash
#
# Program:
#   ssh-home setup script
#
# Exit Code:
#   1 - Calling syntax error
#   3 - Destination directory does not exist
#
#   11 - Copy file failed
#   13 - Change file permission failed


# ----------------------------------------------------------------------------
# Function definition
#
# Usage: show_help
# ----------------------------------------------------------------------------
showHelp() {
cat << EOF
Usage: ${0##*/} home-connect|home-rsync|ip-record|all DESTINATION

    home-connect            Setup for home-connect function
    home-rsync              Setup for home-rsync function
    ip-record               Setup for ip-record function
    all                     Setup for all functions
EOF
}

# ============================
# Check exit code function
# USAGE:
#   checkCode EXITCODE MESSAGE
# ============================
function checkCode() {
  if [[ ${?} -ne 0 ]]; then
    echo ${2}
    exit ${1}
  fi
}

# ===========================
# Usage: Installation DESTDIR 
# ===========================
function Installation() {
    DESTDIR=${1}

    # Setup process
    cp README.md ${DESTDIR}
    checkCode 11 "Copy README.md failed." &> /dev/null    
    cp requirements.txt ${DESTDIR}
    checkCode 11 "Copy requirements.txt failed." &> /dev/null    

    if [[ ! -f ${DESTDIR}/config.ini ]]; then
        cp template.ini ${DESTDIR}/config.ini
        checkCode 11 "Copy template.ini to config.ini failed." &> /dev/null    
    fi

    cp -r module_pkg ${DESTDIR}
    checkCode 11 "Copy module_pkg directory failed." &> /dev/null    
    cp -r general_pkg ${DESTDIR}
    checkCode 11 "Copy general_pkg directory failed." &> /dev/null    

    # ip_record setup
    if [[ "${IP_RECORD}" = true ]]; then
        cp ip_record.py ${DESTDIR}
        checkCode 11 "Copy ip_record.py failed." &> /dev/null    
        chmod 755 ${DESTDIR}/ip_record.py
        checkCode 13 "Change ip_record.py file permission failed." &> /dev/null    
    fi

    # home_connect setup
    if [[ "${HOME_CONNECT}" = true ]]; then
        cp home_connect.py ${DESTDIR}
        checkCode 11 "Copy home_connect.py failed." &> /dev/null    
        chmod 755 ${DESTDIR}/home_connect.py
        checkCode 13 "Change home_connect.py file permission failed." &> /dev/null    
    fi

    # home_rsync setup
    if [[ "${HOME_RSYNC}" = true ]]; then
        cp home_rsync.py ${DESTDIR}
        checkCode 11 "Copy home_rsync.py failed." &> /dev/null    
        chmod 755 ${DESTDIR}/home_rsync.py
        checkCode 13 "Change home_rsync.py file permission failed." &> /dev/null    
    fi
}


# Calling setup format check
if [[ "${#}" -ne 2 ]];  then
    showHelp
    exit 1
fi

DESTINATION=${2}
if [[ ! -d ${DESTINATION} ]]; then
    echo "ERROR: Destination directory does not exist"
    exit 3
fi

SETUP_TYPE=${1}
case ${SETUP_TYPE} in
    home-connect)
        HOME_CONNECT=true
        ;;
    home-rsync)
        HOME_RSYNC=true
        ;;
    ip-record)
        IP_RECORD=true
        ;;
    all)
        HOME_CONNECT=true
        HOME_RSYNC=true
        IP_RECORD=true
        ;;
    *)
        showHelp
        exit 1
        ;;
esac


# System checking
SYSTEM_RELEASE=$(uname -a)
case ${SYSTEM_RELEASE} in
  *Linux*)
    echo "Linux detected"
    echo ""
    Installation ${DESTINATION}
    ;;
  *)
    echo "System not supported."
    exit 1
esac

echo "ssh-home setup success."
exit 0