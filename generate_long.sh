#!/usr/bin/bash

#   Copyright (c) 2020 Patrick Diehl
#
#   Distributed under the Boost Software License, Version 1.0. (See accompanying
#   file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)


#Config
EXECUTABLE=""
PROGRAM_ARGS=""
HPX_ARGS="--hpx:ini=hpx.stacks.use_guard_pages=0 --hpx:bind=numa-balanced --hpx:options-file=../agas-pfx-counters.cfg"


for l in {13..13}
do

    mkdir -p level_${l}
cat << _EOF_ > level_${l}/submit-job.sh
#!/bin/bash
#SBATCH --job-name=Octotiger_Level_${l}
#SBATCH --output=slurm.out
#SBATCH --error=slurm.err
#SBATCH --nodes=${NODES}
#SBATCH --time=${TIME}

echo "Activate APEX"
APEX_SCREEN_OUTPUT=0
APEX_CSV_OUTPUT=1

echo "$(date +%H:%M:%S) launching octotiger"
srun -n ${EXECUTABLE} ${PROGRAM_ARGS} ${HPX_ARGS} 
_EOF_

chmod a+x level_${l}/submit-job.sh
done
