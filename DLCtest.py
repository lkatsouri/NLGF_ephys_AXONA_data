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
####example for single
####           'bodyparts': ['snout', 'left_ear', 'right_ear', 'centre', 'lateral_left',
#                           'lateral_right', 'tailbase', 'tail_end'],
####           'skeleton': [['part1', 'part2'], ['part2', 'part3'], ...],
####           'start': ['numVideoFrac'], 'stop': ['numVideoFrac'],
####           'numframes2pick': [...'],
####           'identity': True (i.e. whether you can tell multianimals apart)}
#### for single mode: keywords = 'bodyparts'

#### When you call the variables of the functions DO NOT use = sign as it will clash
#### Just call each variable in THAT order. i.e:
# import DLCtest
# configEdits = {'bodyparts': ['snout', 'left_ear', 'right_ear', 'centre', 'lateral_left', 'lateral_right', 'tailbase', 'tail_end'], 'start': 0.1, 'stop': 0.9, 'numframes2pick':10}


# savepath = 'D:/DlcTrainedNetworks/'
#### TO TRAIN FROM A DIFFERENT SNAPSHOT: deeplabcut.train_network(config, max_snapshots_to_keep=None,saveiters=5000,maxiters=50000,gputouse=0,keepdeconvweights=False)
# DLCtest.DLC_step1('MouseTopDown', videolist, savepath, configEdits) #NO = SIGNS OTHERWiSE IT WONT WORK
#### DLCtest.DLC_step1('MouseTopDown', videolist, savepath, configEdits)

def DLC_step1(projectname, videopath, savepath, configEdits, multi=False):
    configpath = deeplabcut.create_new_project(projectname, 'Loukia', videopath, copy_videos=True, multianimal=multi,
                                               working_directory=savepath)
    deeplabcut.auxiliaryfunctions.edit_config(configpath, configEdits)
    deeplabcut.extract_frames(configpath, mode='automatic', algo='kmeans', userfeedback=False, crop=False)
    deeplabcut.label_frames(configpath)
    deeplabcut.check_labels(
        configpath)  # added this SO IT WILL create the images with the labels that I have added so I can check them manually

    return configpath


def DLC_trainmodel(configpath, multi=False, saveiters=10000,
                   maxiters=300000):  # when I will run this, I just need to give the configpath, everything else is predetermined
    if multi:
        deeplabcut.create_multianimaltraining_dataset(configpath)
    else:
        deeplabcut.create_training_dataset(configpath, augmenter_type='imgaug')

    ###IF YOU NEED TO AUGMENT YOU DATASET USE THE LINES BELOW
    # print('choose trainposeconfigfile')
    # trainposeconfigfile = fd.askopenfilename()
    # cfg_dlc = deeplabcut.auxiliaryfunctions.read_plainconfig(trainposeconfigfile)
    # cfg_dlc['augmentationprobability'] = .5
    # #cfg_dlc['batch_size'] = 1  # pick that as large as your GPU can handle it
    # cfg_dlc['elastic_transform'] = True
    # cfg_dlc['init_weights'] = D:\DlcTrainedNetworks\MouseTopDown-Loukia-2022-09-13\dlc-models\iteration-1\MouseTopDownSep13-trainset90shuffle1\train\snapshot-340000
    # cfg_dlc['rotation'] = 180
    # cfg_dlc['covering'] = True
    # cfg_dlc['motion_blur'] = True
    # cfg_dlc['multi_step'] = [[1e-4, 7500], [5.0e-5, 12000], [1e-5, 300000]]
    # deeplabcut.auxiliaryfunctions.write_plainconfig(trainposeconfigfile, cfg_dlc)

    deeplabcut.train_network(configpath, max_snapshots_to_keep=None, saveiters=saveiters, maxiters=maxiters,
                             keepdeconvweights=False)  # this will save all snapshots, change to ANy for n=5 or write any integer
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
    #deeplabcut.create_labeled_video(configpath, videolist,filtered=True)
    deeplabcut.create_labeled_video(configpath, videolist, filtered=False)
    deeplabcut.plot_trajectories(configpath, videolist, filtered=True, showfigures=True,
                                 displayedbodyparts=['snout', 'centre', 'tailbase'])  # this will plot the trajectories


def DLC_verifymodel_multi(configpath, videopath, savepath, trackmethod='ellipse', iduserdefined=True):
    deeplabcut.analyze_videos(configpath, videopath, auto_track=False, destfolder=savepath, identity_only=iduserdefined)
    deeplabcut.convert_detections2tracklets(configpath, videopath, track_method=trackmethod,
                                            identity_only=iduserdefined, destfolder=savepath, overwrite=True)
    deeplabcut.stitch_tracklets(configpath, videopath, track_method=trackmethod, output_name='test',
                                destfolder=savepath)


def downsample(videofolder, height=512, outpath=True):
    if outpath:
        outpath = videofolder
    for f, file in enumerate(os.listdir(videofolder)):
        print(f)
        if file[-4:] == '.avi' or '.mp4':
            deeplabcut.DownSampleVideo(os.path.join(videofolder, file), width=-1, height=height, outsuffix='_downsample',
                                       outpath=outpath)


###To plot the trajectories
# basepath = 'D:/DlcTrainedNetworks/MouseTopDown_EPM-Loukia-2022-10-11/videos/'  # write your path here that contains the videos
# config = 'D:/DlcTrainedNetworks/MouseTopDown_EPM-Loukia-2022-10-11/config.yaml'
# import os
#
# os.listdir(basepath)
# directory = os.listdir(basepath)
# for i, ii in enumerate(directory):
#     print(os.path.join(basepath, ii))  # this is to see if it can join the path and print all the files
#
# videolist = []
# import numpy as np
#
# for i, ii in enumerate(directory):
#     if ii[-3:] == 'mp4':
#         videolist = np.append(videolist, os.path.join(basepath, ii))  # this is to append the list with all the videos
# print(len(videolist))
# deeplabcut.plot_trajectories(config, videolist, videotype='mp4', filtered=True, displayedbodyparts=['snout, centre, tailbase'])
