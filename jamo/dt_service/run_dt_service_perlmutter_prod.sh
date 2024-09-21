#!/bin/bash

#SBATCH -q cron
#SBATCH -t 23:55:00
#SBATCH -o /global/cfs/cdirs/seqfs/code_and_ui/cori_prod/jamo_source/jgi-sdm-cron/SDM_Prod_CronJobs/LOGS/dt_cron_perlmutter.log
#SBATCH --open-mode=append
#SBATCH --constraint=cron

URL="https://data-dev.taskforce5.lbl.gov"

TIME_TO_RUN=84600  # We want dt_service to run for 23.5 hours as 24 hours is the limit for the SLURM queue

dt-service -D t5 -t 1 -f perlmutter -k ingest,copy,tar,md5 -r $TIME_TO_RUN $URL -l prod
