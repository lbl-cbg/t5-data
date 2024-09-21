# m h  dom mon dow   command
BIN_HOME=$CFS/m4521/jamo_code/dt_service/scripts
DT_ERROR=$CFS/m4521/jamo_code/dt_service/dt_cron.log

# dt_services
#
*/2 * * * * env /bin/bash -c $BIN_HOME/run_dt_service_nersc_prod.bash >> $DT_ERROR 2>&1
1-59/2 * * * * env /bin/bash -c $BIN_HOME/run_dt_service_nersc_ingest.bash >> $DT_ERROR 2>&1
