#!/usr/bin/bash

#   Copyright (c) 2020 Patrick Diehl
#
#   Distributed under the Boost Software License, Version 1.0. (See accompanying
#   file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)


#Config
EXECUTABLE=""
PROGRAM_ARGS=""
HPX_ARGS="--hpx:ini=hpx.stacks.use_guard_pages=0 --hpx:bind=numa-balanced --hpx:options-file=../../agas-pfx-counters.cfg"
TIME=01:00:00


mkdir -p scaling
cd scaling

for LEVEL in 1 2 3
do
    if [ "$LEVEL" == 1 ]; then
        N1=0 # 2^0 = 1
        N2=1 # 2^  =
    elif [ "$LEVEL" == 2  ]; then
        N1=0
        N2=1
    elif [ "$LEVEL" == 3 ]; then
        N1=0
        N2=1
    fi

    for NPOWER in $(seq $N1 1 $N2)
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


echo "$(date +%H:%M:%S) launching octotiger"
srun -n ${EXECUTABLE} ${PROGRAM_ARGS} ${HPX_ARGS} 
_EOF_

chmod a+x level_${LEVEL}_${NODES}/submit-job.sh
done
done
