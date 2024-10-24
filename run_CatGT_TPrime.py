import subprocess
import os
import glob
import time
import numpy as np


def main(basefolder, tprimesavefolder, runcatGT=True, runsupercat=True, runtprime=True, prbnum='0'):
    supercatcmd = catgt(basefolder, runcatGT=runcatGT, prbnum=prbnum)
    supercat(basefolder, supercatcmd, runsupercat=runsupercat, prbnum=prbnum)
    tprime(basefolder, tprimesavefolder, runtprime=runtprime, runsupercat=runsupercat, prbnum=prbnum)


def runprocess(command):
    start = time.time()
    subprocess.Popen(command, shell='False').wait()
    execution_time = time.time() - start
    print('completed: ' + str(np.around(execution_time, 2)) + ' s')


def catgt(basefolder, runcatGT=True, prbnum='0'):
    recordingfolders = glob.glob(basefolder + '/*_g*')
    catgtcmd = 'C:/CatGT_newversion/CatGT'
    supercatcmd = '-supercat='

    for f, ff in enumerate(recordingfolders):
        rundir = os.path.split(ff)[1]
        rundir = rundir[:-3]
        gvalue = ff[-1]
        command = catgtcmd + ' -dir=' + basefolder + ' -run=' + rundir + ' -g=' + gvalue + ' -t=0 -ni -ap -prb_fld -prb=' + prbnum
        command = command + ' -apfilter=butter,12,300,9000'
        command = command + ' -loccar_um=200,400' #' -gbldmx' #
        command = command + ' -gfix=0.4,0.1,0.02 -xid=0,0,0,2,0'
        print(command)

        if runcatGT:
            runprocess(command)

        supercatpath = '{' + basefolder + ',' + os.path.split(ff)[1] + '}'
        supercatcmd = supercatcmd + supercatpath

    return supercatcmd


def supercat(basefolder, supercatcmd, runsupercat=True, prbnum='0'):
    catgtcmd = 'C:/CatGT_newversion/CatGT'
    supercatcmd = catgtcmd + ' -t=cat -prb_fld -ap -prb=' + prbnum + ' -no_auto_sync ' + supercatcmd + ' -dest=' + basefolder
    print(supercatcmd)

    if runsupercat:
        runprocess(supercatcmd)




def tprime(basefolder, savefolder, runtprime=True, runsupercat=True, prbnum='0'):
    tprimecmd = 'C:/TPrime/TPrime'
    recordingfolders = glob.glob(basefolder + '/*_g*')

    if runsupercat:
        recordingfolders = recordingfolders[:-1]

    for f, ff in enumerate(recordingfolders):
        foldername = os.path.split(ff)[1]
        foldername = foldername+'_imec'+prbnum
        spikeglxsync = glob.glob(ff+'/'+foldername+'/*500.txt')[0]
        nisync = glob.glob(ff+'/*500.txt')[0]
        nicamsync = glob.glob(ff+'/*xid*txt')[0]
        savefile = savefolder+foldername[:-6]+'_spikeglx.txt'
        command = tprimecmd + ' -syncperiod=1.0 -tostream=' + spikeglxsync + ' -fromstream=1,' + nisync + ' -events=1,' + nicamsync + ',' + savefile
        print(command)

        if runtprime:
            runprocess(command)
