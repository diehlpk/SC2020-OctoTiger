#!/bin/bash

#   Copyright (c) 2020 Patrick Diehl
#
#   Distributed under the Boost Software License, Version 1.0. (See accompanying
#   file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)


#Config
PROGRAM_ARGS=""
HPX_ARGS="--hpx:ini=hpx.stacks.use_guard_pages=0 --hpx:bind=numa-balanced --hpx:options-file=../agas-pfx-counters.cfg"
FAB_ENABLE=

for LEVEL in {10..12}
do

    mkdir -p level_${LEVEL}
cat << _EOF_ > level_${LEVEL}/submit-job.sh
#!/bin/bash
#SBATCH --job-name=Octotiger_Level_${LEVEL}
#SBATCH --output=slurm.out
#SBATCH --error=slurm.err
#SBATCH --nodes=32
#SBATCH --time=24:00:00
#SBATCH --constraint=haswell
#SBATCH -A xpress
#SBATCH --qos=regular

echo #Load paths"
source /project/projectdirs/xpress/sc2020/load_octoMPI.sh

echo "Activate APEX"
APEX_SCREEN_OUTPUT=0
APEX_CSV_OUTPUT=1

./copy_restart.sh
echo "$(date +%H:%M:%S) launching octotiger"
srun -N \${SLURM_JOB_NUM_NODES} -n \${SLURM_JOB_NUM_NODES} -c 32 --cpu_bind=cores \$OCTOPATH/octotiger --config_file=rcb.ini ${HPX_ARGS} ${FAB_ENABLE} 
_EOF_

cp -r rcb${LEVEL}/* level_${LEVEL}/  
chmod a+x level_${LEVEL}/submit-job.sh 

done
