import numpy as np

def get_line(filename, word, last_line=-1):
    mystr=""
    line_num=0
    with open (filename) as myfile:
        cur_line = myfile.readline()
        count = 1
        while cur_line != "" and count * last_line / np.abs(last_line) < np.abs(last_line):
            if word in cur_line:
                mystr = cur_line
                line_num = count
            count += 1
            cur_line = myfile.readline()
    return mystr, line_num

nthreads = [1,2,4,8,16,32,64,128,256,512,1024]#,80,160,320,640,1280]

paths = ["scaling/level_10_", "scaling/level_11_","./scaling/level_12_","./scaling_hpx_apex/level_10_","./scaling_no_apex/level_10_","./scaling_pure_hpx/level_10_"]
paths = ["./scaling_old/level_10_","./scaling_old/level_11_","./scaling/level_12_"]
colors = ['-k^', '--ko', '-.kP', '--kP', '-.kp', ':ko', '-ko', '-k^']
titles = ['level 10', 'level 11', 'level 12', 'level 10 (II)', 'level 10 (III)','level 10 (IV)','Octo-QueenBee: angle 0', 'Octo-QueenBee: angle 0, AM off', 'Octo-BigRed: angle 0, try2', 'Octo-BigRed: angle 0, half-full node', 'Octo-BigRed: angle 0, hpx-without guard', 'Octo-BigRed: angle 0, AM off without guard',]
minValue = [1, 64, 1024, 1, 1, 1, 1024, 16, 64, 64]
maxValue = [64, 1024, 1024, 64, 64, 64, 1024]

#paths = ["testSod_ref5_cray", "testSod_ref5_AM_off_cray", "testSod_ref5", "testSod_ref5_AM_off"]
#colors = ['-.ro', '-.r^', '-go', '-g^']
#titles = ['Octotiger-br-cray: angle 0', 'Octotiger-br-cray: angle 0, AM off', 'Octotiger: angle 0', 'Octotiger: angle 0, AM off']
#minValue = [8, 4, 1, 1]
#Twos = [[], [], [], [], []]

Octo_times = []
all_threads = []
grids = []
amrbds = []
leafs = []

threads = nthreads

#thpath = ""
#plotref = 128

#compstr = "total"
#endLine = ['//']
#line = -31
savename = ""
#readGrids = True
#flash_filename = "periods.log"
#search_line = ["Total: "]
#if compstr != "total":
#    line = -30
#    compstr = "computational"
#    savename = "_comp"
#    flash_filename = "evol_periods.log"
#    search_line = "Computation: "
#    endLine = "("
#Total = -31 
#Computational = -30

search_line = ["Computation: ", "  Regrid:"]
endLine = ["(", "("]

for i in range(0, len(paths)):
    cur_time = []
    cur_thread = []
    readGrids = True
    output = ''
    for j in range(0, len(threads)):
        print j, threads[j]
        if ((threads[j] >= minValue[i]) and (threads[j] <= maxValue[i])):
            thpath = paths[i] + str(threads[j])
            thpath += "/slurm.out" #+ str(threads[j])
            timesType = []
            for k in range(0, len(search_line)):
                mystr = get_line(thpath, search_line[k])[0]    
                tt=mystr[mystr.find(':')+1:mystr.find(endLine[k])]
                timesType.append(float(tt))
                print mystr
            mystr = get_line(thpath, "OMEGA = ")
            mystr = get_line(thpath, "regrid done in ", mystr[1])
            tt = mystr[0]
            tt = tt[tt.find('in')+2:tt.find("seconds")]
            timesType.append(-1*float(tt))
            cur_thread.append(threads[j])
            #if 'level_10' in paths[i]:  # for level 10 the counters were different computatiion= Total - Output - Initial regridd
             #   mystr = get_line(thpath, "Computation: ")[0]
             #   tt=mystr[mystr.find(':')+1:mystr.find("(")]
             #   computation_time = float(tt)
             #   mystr = get_line(thpath, "Regrid: ")[0]
             #   tt=mystr[mystr.find(':')+1:mystr.find("(")]
             #   regrid_time = float(tt)
             #   mystr = get_line(thpath, "OMEGA = ")
             #   mystr = get_line(thpath, "regrid done in ", mystr[1])
             #   regrid_initial_tot = 0.0
             #   while mystr[0] != "":
             #       print mystr
             #       tt = mystr[0]
             #       tt = tt[tt.find('in')+2:tt.find("seconds")]
             #       regrid_initial_tot += float(tt)
             #       mystr = get_line(thpath, "regrid done in ", mystr[1])
             #   print timesType[0], ' - ', computation_time, ' - ', regrid_initial_tot
            #    cur_time.append(computation_time + regrid_time - regrid_initial_tot)
            #else:
            #print timesType[0], timesType[1], timesType[2]
            cur_time.append(np.array(timesType).sum())
            subgrids_tot = 0
            mystr = get_line(thpath, '/total}/subgrids,')
            while mystr[0] != "": 
                print mystr
                tt = mystr[0]
                tt=tt[tt.find('[s],')+4:tt.find('//')]
                subgrids_tot += int(tt)
                lineOld = mystr[1]
                mystr = get_line(thpath, '/total}/subgrids,', mystr[1])
                if (lineOld - mystr[1] > 1000):
                    mystr = [""]
            print subgrids_tot
            amrbds_tot = 0
            mystr = get_line(thpath, '/total}/amr_bounds,')
            while mystr[0] != "":
                print mystr
                tt = mystr[0]
                tt=tt[tt.find('[s],')+4:tt.find('//')]
                amrbds_tot += int(tt)
                lineOld = mystr[1]
                mystr = get_line(thpath, '/total}/amr_bounds,', mystr[1])
                if (lineOld - mystr[1] > 1000):
                    mystr = [""]
            print amrbds_tot
            leafs_tot = 0
            mystr = get_line(thpath, '/total}/subgrid_leaves,')
            while mystr[0] != "":
                print mystr
                tt = mystr[0]
                tt=tt[tt.find('[s],')+4:tt.find('//')]
                leafs_tot += int(tt)
                lineOld = mystr[1]
                mystr = get_line(thpath, '/total}/subgrid_leaves,', mystr[1])
                if (lineOld - mystr[1] > 1000):
                    mystr = [""]
            print leafs_tot
            if (readGrids):
                grids.append(subgrids_tot)
                amrbds.append(amrbds_tot)
                leafs.append(leafs_tot)
                readGrids = False
    all_threads.append(cur_thread)
    Octo_times.append(cur_time)

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import os

plt.close()
fig = plt.figure(figsize=(8, 6))
ax = plt.axes([0.15,0.15,0.8,0.8])
ax.tick_params(direction='in', length=6, width=2, colors='black',bottom=True, top=True, left=True, right=True)
plt.rc('font', family='serif',size=28)
plt.rc('text', usetex=True)
plt.rc('xtick', labelsize=30)
plt.rc('ytick', labelsize=30)

for i in range(0, len(paths)):
    plt.loglog(np.array(all_threads[i]), np.array(Octo_times[i]), colors[i], label=titles[i])
#plt.axvline(x=32, color='r', linestyle='-.')
#plt.axvline(x=20, color='g')
plt.xlabel(r'$\#$ nodes')
plt.ylabel('computation time (sec)')
#if compstr=="total" and plotref == 256:
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
          fancybox=True, shadow=True, ncol=2, numpoints=1)
plt.xlim(0.8,5000)
plt.savefig('new_scales'+savename+'.eps', bbox_inches="tight")
os.system('epspdf '+'new_scales'+savename+'.eps '+'new_scales'+savename+'.pdf')


import matplotlib.ticker as ticker

print 'grids: ', grids
print 'amr boundaries: ', amrbds
print 'leafs subgrids: ', leafs

plt.close()
fig = plt.figure(figsize=(8, 6))
ax = plt.axes([0.15,0.15,0.8,0.8])
ax.tick_params(direction='in', length=6, width=2, colors='black',bottom=True, top=True, left=True, right=True)
plt.rc('font', family='serif',size=28)
plt.rc('text', usetex=True)
plt.rc('xtick', labelsize=30)
plt.rc('ytick', labelsize=30)
plt.grid(True)
#ax.set_xscale('symlog', basex=2)
#ax.set_yscale('symlog', basey=2)

for i in range(0, len(paths)):
    if ('level_10' in paths[i]) and (grids[i] == 0):
        grids[i] = 23709
    plt.plot(np.array(all_threads[i]), grids[i] / np.array(Octo_times[i]), colors[i], label=titles[i])
#plt.axvline(x=32, color='r', linestyle='-.')
#plt.axvline(x=20, color='g')
plt.xlabel(r'$\#$ nodes')
plt.ylabel('subgrids per sec')
#if compstr=="total" and plotref == 256:
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
          fancybox=True, shadow=True, ncol=2, numpoints=1)
#plt.xlim(0.8,40)
plt.savefig('grids_per_sec'+savename+'.eps', bbox_inches="tight")
os.system('epspdf '+'grids_per_sec'+savename+'.eps '+'grids_per_sec'+savename+'.pdf')



plt.close()
fig = plt.figure(figsize=(8, 6))
ax = plt.axes([0.15,0.15,0.8,0.8])
ax.tick_params(direction='in', length=6, width=2, colors='black',bottom=True, top=True, left=True, right=True)
#ax.set_xscale('symlog', basex=2)
#ax.set_yscale('symlog', basey=2)
plt.rc('font', family='serif',size=28)
plt.rc('text', usetex=True)
plt.rc('xtick', labelsize=30)
plt.rc('ytick', labelsize=30)
plt.grid(True)

for i in range(0, len(paths)):
    plt.plot(np.array(all_threads[i]), (grids[i] / np.array(Octo_times[i])) / (grids[0] / Octo_times[0][0]), colors[i], label=titles[i])
#plt.axvline(x=32, color='r', linestyle='-.')
#plt.axvline(x=20, color='g')
plt.xlabel(r'$\#$ nodes')
plt.ylabel('speed-ups')
#plt.gca().yaxis.set_major_formatter(ticker.PercentFormatter(1))
#plt.gca().xaxis.set_major_locator(ticker.FixedLocator(nthreads))
#if compstr=="total" and plotref == 256:
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
          fancybox=True, shadow=True, ncol=2, numpoints=1)
#plt.xlim(0.8,70)
plt.savefig('speed-up'+savename+'.eps', bbox_inches="tight")
os.system('epspdf '+'speed-up'+savename+'.eps '+'speed-up'+savename+'.pdf')



plt.close()
fig = plt.figure(figsize=(8, 6))
ax = plt.axes([0.15,0.15,0.8,0.8])
ax.tick_params(direction='in', length=6, width=2, colors='black',bottom=True, top=True, left=True, right=True)
plt.rc('font', family='serif',size=28)
plt.rc('text', usetex=True)
plt.rc('xtick', labelsize=30)
plt.rc('ytick', labelsize=30)
#ax.set_xscale('symlog', basex=2)
#ax.set_yscale('symlog', basey=2)

for i in range(0, len(paths)):
    plt.loglog(np.array(all_threads[i]), np.array(all_threads[i])*np.array(Octo_times[i]), colors[i], label=titles[i])
#plt.axvline(x=32, color='r', linestyle='-.')
#plt.axvline(x=20, color='g')
plt.xlabel(r'$\#$ nodes')
plt.ylabel('total node time (sec)')
#if compstr=="total" and plotref == 256:
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
          fancybox=True, shadow=True, ncol=2, numpoints=1)
#plt.xlim(0.8,40)
plt.savefig('node_time'+savename+'.eps', bbox_inches="tight")
os.system('epspdf '+'node_time'+savename+'.eps '+'node_time'+savename+'.pdf')
