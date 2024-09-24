#!/bin/bash
# dt_service (prod)
#SCRON -q workflow
#SCRON -A m4521
#SCRON -c 2
#SCRON -t 90-00:00:00
#SCRON --time-min=12:00:00
#SCRON --job-name=jamo_dt_service
#SCRON --chdir=${DTS_LOG_DIR}
#SCRON --dependency=singleton
#SCRON --output=${DTS_LOG_DIR}/dt_service.perlmutter.%j.log
#SCRON --open-mode=append
* * * * * $DTS_SCRIPT_DIR/run_dt_service_perlmutter_prod.sh
