#!/bin/bash
echo "---- Job ID: $SLURM_JOB_ID ----"

URL="https://data-dev.taskforce5.lbl.gov"
TIME_TO_RUN=2592000  # We want dt_service to run for
cd $DTS_LOG_DIR

dt-service -D t5 -t 1 -f perlmutter -k ingest,copy,tar,md5 -r $TIME_TO_RUN $URL -l prod
