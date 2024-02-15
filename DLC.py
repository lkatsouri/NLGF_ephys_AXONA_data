# Layout of DLC steps for projects
import deeplabcut
import warnings
from tkinter import filedialog as fd
import numpy as np
import os

warnings.filterwarnings('ignore', category=DeprecationWarning)


#### configEdits that should be made (example for multi)
#### edits = {'individuals': ['implanted', 'conspecific1', 'conspecific2'],
####           'uniquebodyparts': ['topright', 'bottomright', 'bottomleft', 'topleft', 'topdoor', 'bottomdoor'],
####           'multianimalbodyparts': [...],
####           'skeleton': [['part1', 'part2'], ['part2', 'part3'], ...],
####           'start': ['numVideoFrac'], 'stop': ['numVideoFrac'],
####           'numframes2pick': [...'],
####           'identity': True (i.e. whether you can tell multianimals apart)}
#### for single mode: keywords = 'bodyparts'


def DLC_step1(projectname, videopath, savepath, configEdits, multi=True):
    configpath = deeplabcut.create_new_project(projectname, 'Cristina', videopath, copy_videos=True, multianimal=multi,
                                               working_directory=savepath)
    deeplabcut.auxiliaryfunctions.edit_config(configpath, configEdits)
    deeplabcut.extract_frames(configpath, mode='automatic', algo='kmeans', userfeedback=False, crop=False)
    deeplabcut.label_frames(configpath)

    return configpath


def DLC_trainmodel(configpath, multi=False, saveiters=10000, maxiters=200000):
    if multi:
        deeplabcut.create_multianimaltraining_dataset(configpath)
    else:
        deeplabcut.create_training_dataset(configpath)

    deeplabcut.train_network(configpath, saveiters=saveiters, maxiters=maxiters)
    deeplabcut.evaluate_network(configpath, plotting=True)


def DLC_analyze_single():
    print('choose configpath')
    configpath = fd.askopenfilename()
    print('choose video directory')
    videopathdir = fd.askdirectory()

    videolist = []
    for x, xx in enumerate(os.listdir(videopathdir)):
        videolist = np.append(videolist, os.path.join(videopathdir, xx))

    deeplabcut.analyze_videos(configpath, videolist, save_as_csv=True)
    deeplabcut.filterpredictions(configpath, videolist, save_as_csv=True)


def DLC_verifymodel_multi(configpath, videopath, savepath, trackmethod='ellipse', iduserdefined=True):
    deeplabcut.analyze_videos(configpath, videopath, auto_track=False, destfolder=savepath, identity_only=iduserdefined)
    deeplabcut.convert_detections2tracklets(configpath, videopath, track_method=trackmethod,
                                            identity_only=iduserdefined, destfolder=savepath, overwrite=True)
    deeplabcut.stitch_tracklets(configpath, videopath, track_method=trackmethod, output_name='test',
                                destfolder=savepath)


def downsample(videofolder, width=500, outpath=True):
    if outpath:
        outpath = videofolder
    for f, file in enumerate(os.listdir(videofolder)):
        if file[-4:] == '.avi':
            deeplabcut.DownSampleVideo(os.path.join(videofolder, file), width=width, height=-1, outsuffix='_downsample',
                                       outpath=outpath)

// # ###To plot the trajectories
// # basepath = 'D:/DlcTrainedNetworks/MouseTopDown_EPM-Loukia-2022-10-11/videos/'  # write your path here that contains the videos
// # config = 'D:/DlcTrainedNetworks/MouseTopDown_EPM-Loukia-2022-10-11/config.yaml'

// # import os
// # os.listdir(basepath)


// # directory = os.listdir(basepath)
// # for i, ii in enumerate(directory):

// #     print(os.path.join(basepath, ii))  # this is to see if it can join the path and print all the files