#!/bin/bash

#   Copyright (c) 2020 Patrick Diehl
#
#   Distributed under the Boost Software License, Version 1.0. (See accompanying
#   file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)


#Config
HPX_ARGS="--hpx:localities \$SLURM_JOB_NUM_NODES  --hpx:ini=hpx.stacks.use_guard_pages=0 --hpx:bind=numa-balanced --hpx:options-file=../../agas-pfx-counters.cfg"
FAB_ENABLE= #"-Ihpx.parcel.libfabric.enable=1 -Ihpx.parcel.bootstrap=libfabric -Ihpx.parcel.message_handlers=0"
TIME=00:10:00

mkdir -p scaling
cd scaling

for LEVEL in 10 11 12
do
    if [ "$LEVEL" == 10 ]; then
        N1=0 # 2^0 = 1
        N2=6 # 2^6 = 64 
    elif [ "$LEVEL" == 11  ]; then
        N1=6 # 2^6 = 64
        N2=10 # 2^10 = 1024
    elif [ "$LEVEL" == 12 ]; then
        N1=0
        N2=1
    fi

    for NPOWER in $(seq $N1 $N2)
    do
        NODES=$(( 2 ** $NPOWER))

    mkdir -p level_${LEVEL}_${NODES}
cat << _EOF_ > level_${LEVEL}_${NODES}/submit-job.sh
#!/bin/bash
#SBATCH --job-name=Octotiger_Level_${LEVEL}_${NODES}
#SBATCH --output=slurm.out
#SBATCH --error=slurm.err
#SBATCH --nodes=${NODES}
#SBATCH --time=${TIME}
#SBATCH --constraint=haswell
#SBATCH -A xpress
#SBATCH --mail-type=begin,end,fail
#SBATCH --mail-user=patrickdiehl@lsu.edu
#SBATCH --qos=regular

set -x
source /project/projectdirs/xpress/sc2020/load_octoMPI.sh

echo "Activate APEX"
export APEX_SCREEN_OUTPUT=0
export APEX_CSV_OUTPUT=1


echo "$(date +%H:%M:%S) launching octotiger"
./copy_restart.sh
srun -N \${SLURM_JOB_NUM_NODES} -n \${SLURM_JOB_NUM_NODES} -c 32 --cpu_bind=cores \$OCTOPATH/octotiger --config_file=rcb.ini ${HPX_ARGS} ${FAB_ENABLE} 
_EOF_

cp -r ../rcb${LEVEL}/* level_${LEVEL}_${NODES}/  
chmod a+x level_${LEVEL}_${NODES}/submit-job.sh 
done
done
