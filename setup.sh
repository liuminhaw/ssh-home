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
    cp ip_record.py ${DESTDIR}
    checkCode 11 "Copy ip_record.py failed." &> /dev/null    
    chmod 755 ${DESTDIR}/ip_record.py
    checkCode 13 "Change ip_record.py file permission failed." &> /dev/null    
}


# Calling setup format check
USAGE="setup.sh DESTINATION"

if [[ "${#}" -ne 1 ]];  then
    echo -e "USAGE:\n    ${USAGE}"
    exit 1
fi

if [[ ! -d ${1} ]]; then
    echo "ERROR: Destination directory does not exist"
    exit 3
fi


# System checking
SYSTEM_RELEASE=$(uname -a)
case ${SYSTEM_RELEASE} in
  *Linux*)
    echo "Linux detected"
    echo ""
    Installation ${1}
    ;;
  *)
    echo "System not supported."
    exit 1
esac

echo "ssh-home setup success."
exit 0