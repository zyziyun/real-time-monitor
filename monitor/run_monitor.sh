#!/usr/bin/env bash
# Example script to run networks generated by generate_alv_network.py
# Nik Sultana, UPenn, February 2020
# Nik Sultana, Illinois Tech, November 2021
#
# NOTE might need to run this script with "sudo"

if [ -z "${HANGARGAMES}" ]
then
  echo "Need to define HANGARGAMES environment variable"
  exit 1
fi

if [ -z "${TOPOLOGY}" ]
then
  TOPOLOGY=${HANGARGAMES}/networks/p4_tutorials/monitor/topology.yml
fi
echo "Using TOPOLOGY=${TOPOLOGY}"

if [ -z "${START_CFG}" ]
then
  START_CFG=""
fi

MODES+=(interactive)
MODES+=(selftest)

if [ -z "${MODE}" ]
then
  MODE="interactive"
  echo "Using default MODE from $0"
fi
if [[ ! " ${MODES[@]} " =~ " ${MODE} " ]]
then
  echo "Unrecognised MODE: $MODE. Possible choices: ${MODES[*]}"
  exit 1
fi
echo "Using MODE=${MODE}. Possible choices: ${MODES[*]}"

TESTDIR=`pwd`/hangargames_output
BASENAME=$(basename $TOPOLOGY .yml)
OUTDIR=$TESTDIR/$BASENAME
PCAP_DUMPS=$OUTDIR/pcap_dump/
LOG_DUMPS=$OUTDIR/log_files/

rm -rf $PCAP_DUMPS $LOG_DUMPS $OUTDIR
mkdir -p $PCAP_DUMPS
mkdir -p $LOG_DUMPS

sudo mn -c 2> $LOG_DUMPS/mininet_clean.err

function interactive {
  sudo -E python3 ${HANGARGAMES}/BMv2/start_flightplan_mininet.py ${TOPOLOGY} \
          --pcap-dump $PCAP_DUMPS \
          --log $LOG_DUMPS \
          --verbose \
          --showExitStatus \
     --fg-host-prog "${START_CFG}" \
     --cli
         2> $LOG_DUMPS/flightplan_mininet_log.err
}


# FIXME adapt this definition to this example
function selftest {
 sudo -E python3 ${HANGARGAMES}/BMv2/start_flightplan_mininet.py ${TOPOLOGY} \
         --pcap-dump $PCAP_DUMPS \
         --log $LOG_DUMPS \
         --verbose \
         --showExitStatus \
    --fg-host-prog "${START_CFG}" \
    --fg-host-prog "h0: ping -c 1 192.0.0.2" \
    --fg-host-prog "h0: ping -c 1 192.0.0.3" \
    --fg-host-prog "h1: ping -c 1 192.0.0.2" \
    --fg-host-prog "h1: ping -c 1 192.0.0.3" \
         2> $LOG_DUMPS/flightplan_mininet_log.err
}

eval $MODE

exit 0


