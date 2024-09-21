# dt_service (prod)
#SCRON --constraint=cron
*/2 * * * * /global/cfs/cdirs/seqfs/code_and_ui/cori_prod/jamo_source/jgi-sdm-cron/SDM_Prod_CronJobs/check_dt_service_perlmutter_prod.bash

# dt_service (dev)
#SCRON --constraint=cron
1-59/2 * * * * /global/cfs/cdirs/seqfs/code_and_ui/cori_dev/jamo_source/jgi-sdm-cron/SDM_Prod_CronJobs/check_dt_service_perlmutter_dev.bash