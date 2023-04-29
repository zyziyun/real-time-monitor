#!/usr/bin/env bash
# Nik Sultana, Illinois Tech, January 2022

if [ -z "${HANGARGAMES}" ]
then
  echo "Need to define HANGARGAMES environment variable"
  exit 1
fi

if [ -z "${TOPOLOGY}" ]
then
  echo "Need to define TOPOLOGY environment variable"
  exit 1
fi

if [ -z "${HGSWITCH}" ]
then
  echo "Need to define HGSWITCH environment variable"
  exit 1
fi

CMD=$1

if [ -z "${CMD}" ]
then
  echo "Usage: $0 <command>"
  exit 1
fi

if [ -z "${QUIET}" ]
then
  echo "Using TOPOLOGY=${TOPOLOGY}"
  echo "Using HGSWITCH=${HGSWITCH}"
fi

echo "${CMD}" | python3 ${HANGARGAMES}/BMv2/send_bmv2_commands.py ${TOPOLOGY} ${HGSWITCH}

exit 0
