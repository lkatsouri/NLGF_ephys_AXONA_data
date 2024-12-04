import subprocess
import os
import glob
import time
import numpy as np


def main(basefolder, tprimesavefolder, runcatGT=True, runsupercat=True, runtprime=False, prbnum='0', sync='NI'):
    supercatcmd = catgt(basefolder, runcatGT=runcatGT, prbnum=prbnum, sync=sync)
    supercat(basefolder, supercatcmd, runsupercat=runsupercat, prbnum=prbnum)

    if runtprime:
        tprime(basefolder, tprimesavefolder, runtprime=runtprime, runsupercat=runsupercat, prbnum=prbnum)


def runprocess(command):
    start = time.time()
    subprocess.Popen(command, shell='False').wait()
    execution_time = time.time() - start
    print('completed: ' + str(np.around(execution_time, 2)) + ' s')


def catgt(basefolder, runcatGT=True, prbnum='0', sync='NI'):
    recordingfolders = glob.glob(basefolder + '/*_g*')
    catgtcmd = 'C:/Users/Loukia/Downloads/CatGTWinApp/CatGT-win/CatGT'
    supercatcmd = '-supercat='

    for f, ff in enumerate(recordingfolders):
        rundir = os.path.split(ff)[1]
        rundir = rundir[:-3]
        gvalue = ff[-1]
        command = (catgtcmd + ' -dir=' + basefolder + ' -run=' + rundir + ' -g=' + gvalue + ' -t=0 -ap')

        if sync == 'NI':
            command = command + ' -ni'

        command = command + ' -prb_fld -prb=' + prbnum + ' -apfilter=butter,12,300,9000 -loccar_um=200,400 -gfix=0.4,0.1,0.02'

        # this is to extract the sync information present on the last channel of the imec stream
        if sync == 'imec':
            command = command + ' -xd=2,0,-1,6,0 -xid=2,0,-1,6,0 -no_auto_sync'

        print(command)

        if runcatGT:
            runprocess(command)

        supercatpath = '{' + basefolder + ',' + os.path.split(ff)[1] + '}'
        supercatcmd = supercatcmd + supercatpath

    return supercatcmd


def supercat(basefolder, supercatcmd, runsupercat=True, prbnum='0'):
    catgtcmd = 'C:/Users/Loukia/Downloads/CatGTWinApp/CatGT-win/CatGT'
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
        foldername = foldername + '_imec' + prbnum
        spikeglxsync = glob.glob(ff + '/' + foldername + '/*500.txt')[0]
        nisync = glob.glob(ff + '/*500.txt')[0]
        nicamsync = glob.glob(ff + '/*xid*txt')[0]
        savefile = savefolder + foldername[:-6] + '_spikeglx.txt'
        command = tprimecmd + ' -syncperiod=1.0 -tostream=' + spikeglxsync + ' -fromstream=1,' + nisync + ' -events=1,' + nicamsync + ',' + savefile
        print(command)

        if runtprime:
            runprocess(command)

basefolder = 'C:/Users/Loukia/Documents/Ephys/Recordings/M1123843/20241029/LinearTrack'
tprimesavefolder = 'nan'

main(basefolder, tprimesavefolder, runcatGT=True, runsupercat=True, runtprime=False, sync='imec')
