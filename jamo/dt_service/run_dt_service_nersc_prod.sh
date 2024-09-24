#!/bin/bash

DOMAIN="data-dev.taskforce5.lbl.gov"
URL="https://$DOMAIN"

cd $HOME
jamo_status=$(curl -k -s $URL/api/tape/diskusage | grep files)
search="^[^tmux].*dt-service.*$DOMAIN.*prod"

if [[ "$jamo_status" == "" ]] ; then

    echo $(date) $0 JAMO down

elif [[ -f "STOP" ]] ; then

    # if STOP is in the home directory
    if [[ ! -z "$(pgrep -u $(whoami) -f $search)" ]]; then
        echo $(date) $0 STOP set, stopping any running services
        kill -s SIGINT $(pgrep -u $(whoami) -f $search)
    fi

# we are expecing the invocations to end with the log extension so we can have multiple prods to handle ingress
elif [[ -z "$(pgrep -u $(whoami) -f $search)" ]]; then

    machine=`uname -n`
    #export PYTHONHTTPSVERIFY=0
    cd $DTS_LOG_DIR

    # use tmux attach -t <service name> to get to session
    if [ "$machine" == "dtn03.nersc.gov" ] ; then
        echo $(date) $0 start dt_service prod ingest,delete,purge,put,copy,md5,tar
        tmux new-session -s dt_service_1 -d "dt-service -D t5 -t 5 -f nersc,repo_w,hsi_1,hsi_2,compute,globus_4 -k ingest,delete,purge,put,copy,md5,tar,untar -r 43200 $URL -l prod"

    elif [ "$machine" == "dtn04.nersc.gov" ] ; then
        echo $(date) $0 start dt_service prod starting prep,pull
        tmux new-session -s dt_service_1 -d "dt-service -D t5 -t 10 -f repo_w,hsi_1,compute -k prep,pull -r 43200 $URL -l prod"
    fi

fi
