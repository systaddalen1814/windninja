#!/bin/bash
#python3 prepare_varyWnCfg_dems.py
# export CPL_DEBUG=NINJAFOAM
#export WINDNINJA_DATA=/mnt/ohpc/WN_src/windninja/data/
# source /opt/openfoam8/etc/bashrc
# mkdir -p $FOAM_RUN/../applications
# cp -r /home/sathwik/Latest/windninja/src/ninjafoam/8/* $FOAM_RUN/../applications
# cd $FOAM_RUN/../applications/
# wmake libso
# echo "done!\n\n\n\n"
# cd utility/applyInit
# wmake
export OMPI_ALLOW_RUN_AS_ROOT=1
export OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1
/usr/local/bin/WindNinja_cli $*







# OUTPUT_FOLDER="/output"
# LOG_FILE="${OUTPUT_FOLDER}/simulation.log"
# python3 /home/sathwik/Latest/scripts/run_caryWnCfg3.py > "${LOG_FILE}" 2>&1