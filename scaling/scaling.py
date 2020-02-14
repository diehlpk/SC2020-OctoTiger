import numpy as np

def get_line(filename, word):
    with open (filename) as myfile:
        cur_line = myfile.readline()
        while cur_line != "":
            if word in cur_line:
                mystr = cur_line
            cur_line = myfile.readline()
    return mystr

nthreads = [1,2,4,8,16,32,64,128]#,80,160,320,640,1280]
br2threads = [1,2,4,8,16,32]
br2threads_cray = [1,2,4,8,16,32,64,128,256,512,1024,2048,4096]

paths = ["testSod_ref4_cray", "testSod_ref4_AM_off_cray", "testSod_ref4", "testSod_ref4_AM_off", "testSod_ref4_cray_take2", "testSod_ref4_cray", "testSod_ref4_cray_takeNew", "testSod_ref4_AM_off_takeNew"]

paths = ["./level_10_"]#, "./level_11_"]
colors = ['-.ko', '-.k^', '-go', '-g^', '-bo', '-mo', '-ko', '-k^']
titles = ['level 10', 'level 11', 'Octo-QueenBee: angle 0', 'Octo-QueenBee: angle 0, AM off', 'Octo-BigRed: angle 0, try2', 'Octo-BigRed: angle 0, half-full node', 'Octo-BigRed: angle 0, hpx-without guard', 'Octo-BigRed: angle 0, AM off without guard',]
minValue = [1, 64, 1, 1, 1, 16, 64, 64]
maxValue = [32, 128]
Twos = [[], [], [], [], [], [32,64,128,256,512,1024], [], []]

#paths = ["testSod_ref5_cray", "testSod_ref5_AM_off_cray", "testSod_ref5", "testSod_ref5_AM_off"]
#colors = ['-.ro', '-.r^', '-go', '-g^']
#titles = ['Octotiger-br-cray: angle 0', 'Octotiger-br-cray: angle 0, AM off', 'Octotiger: angle 0', 'Octotiger: angle 0, AM off']
#minValue = [8, 4, 1, 1]
#Twos = [[], [], [], [], []]

Octo_times = []
all_threads = []
grids = []

thpath = ""
plotref = 128

compstr = "tota"
endLine = '//'
line = -31
savename = ""
readGrids = True
flash_filename = "periods.log"
search_line = "Total: "
if compstr != "total":
    line = -30
    compstr = "computational"
    savename = "_comp"
    flash_filename = "evol_periods.log"
    search_line = "Computation: "
    endLine = "("
#Total = -31 
#Computational = -30

search_line = ["Computation: ", "Regrid:"]
endLine = ["(", "("]

for i in range(0, len(paths)):
    cur_time = []
    cur_thread = []
    readGrids = True
    output = ''
    if 'cray' in paths[i]:
        maxpernode = 32
        threads = br2threads_cray
        if paths[i] == 'testSod_ref4_cray':
            threads = np.sort(threads).tolist()
            threads.append(40)
            threads.append(80)   
            threads = np.sort(threads).tolist()
    else:
        maxpernode = 0
        threads = nthreads
        if 'ref5' in paths[i]:
            output = '/output'
    for j in range(0, len(threads)):
        print j, threads[j]
        if (len(Twos[i]) == 0):
            if ((threads[j] >= minValue[i]) and (threads[j] <= maxValue[i])):
                thpath = paths[i] + str(threads[j])
                if (threads[j] > maxpernode):
                    thpath += "/slurm.out" #+ str(threads[j])
                else:
                     thpath += output
                timesType = []
                for k in range(0, len(search_line)):
                    mystr = get_line(thpath, search_line[k])    
                    tt=mystr[mystr.find(':')+1:mystr.find(endLine[k])]
                    timesType.append(float(tt))
                cur_thread.append(threads[j])
                cur_time.append(np.array(timesType).sum())
                if (readGrids):
                    mystr = get_line(thpath, '/octotiger{locality#0/total}/subgrids')
                    print mystr
                    tt=mystr[mystr.find('[s],')+4:mystr.find('//')]
                    grids.append(float(tt)*threads[j])
                    readGrids = False
        else:
            cur_hasTwos = np.array(Twos[i])
            if (len(np.where(cur_hasTwos == threads[j])[0]) > 0):
                thpath = paths[i] + "/th" + str(2*threads[j]) + "/th" + str(threads[j]) + "_2"
                mystr = get_line(thpath, search_line)    
                tt=mystr[mystr.find(':')+1:mystr.find('\\')]
                cur_thread.append(threads[j])
                cur_time.append(float(tt))   
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
plt.xlabel(r'\# nodes')
plt.ylabel(compstr+' time (sec)')
#if compstr=="total" and plotref == 256:
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
          fancybox=True, shadow=True, ncol=2, numpoints=1)
plt.xlim(0.8,5000)
plt.savefig('new_scales'+savename+'.eps', bbox_inches="tight")
os.system('epspdf '+'new_scales'+savename+'.eps '+'new_scales'+savename+'.pdf')



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


for i in range(0, len(paths)):
    plt.plot(np.array(all_threads[i]), (grids[i] / np.array(Octo_times[i])) / (grids[i] / Octo_times[i][0]), colors[i], label=titles[i])
#plt.axvline(x=32, color='r', linestyle='-.')
#plt.axvline(x=20, color='g')
plt.xlabel(r'$\#$ nodes')
plt.ylabel('speed-ups')
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
    plt.plot(np.array(all_threads[i]), np.array(all_threads[i])*np.array(Octo_times[i])**2, colors[i], label=titles[i])
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
