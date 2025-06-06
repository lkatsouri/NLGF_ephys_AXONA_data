# Python file here: run deeplabcut to train model. 

import deeplabcut
import glob
import os

config_path = r"G:\DLCOutputData\Object_experiments\Karen_Loc_Pytorch-Angela-2025-05-27\config.yaml"

# deeplabcut.dropimagesduetolackofannotation(config_path)

# Make sure the training set has been created properly:
deeplabcut.convertcsv2h5(config_path, userfeedback=False, scorer='MargotTirole') # if .H5 file was not created
print("CSVToH5Done")

deeplabcut.check_labels(config_path, visualizeindividuals=False) # Good practice to run first
print("LabelsChecked")

deeplabcut.create_training_dataset(config_path, augmenter_type='imgaug') # creates actual training set and sub folder in dlc-models
print("TrainingSetCreated")
# Then make sure you have updated any parameters in the pose_cfg.yaml file within the dlc-models sub folder for this particular iteration.
# 		# E.g. Number of iterations, initial network weights etc..
#
# N.B. Iteration number can be changed via config.yaml file + rerunning deeplabcut.create_training_dataset()

deeplabcut.train_network(config_path)
print("NetworkTrained")

deeplabcut.evaluate_network(config_path,Shuffles=[1], plotting=True)
deeplabcut.extract_save_all_maps(config_path, shuffle=1)
print("NetworkEvaluated")

#path to the video folder
video_folder= r'G:\DLCOutputData\Object_experiments\Karen_Loc_Pytorch-Angela-2025-05-27\videos'

#files in the folder
video_list = glob.glob(os.path.join(video_folder, '*cropped.mp4'))
print(len(video_list))


for file_to_analyse in video_list:
    # deeplabcut.analyze_videos(config_path, [file_to_analyse], save_as_csv=True, gputouse=0)
    #
    # #
    # # # filter trajectories
    # deeplabcut.filterpredictions(config_path, [file_to_analyse], shuffle=1, filtertype='arima', p_bound=0.01, ARdegree=3, MAdegree=1, alpha=0.01)
    # print("VideoFiltered")
    #
    # # plot trajectories
    # deeplabcut.plot_trajectories(config_path,[file_to_analyse],shuffle=1,displayedbodyparts= ['snout','left_ear','right_ear','centre','lateral_left','lateral_right','tailbase','tail_end']) # filtered=True,

    #create labeled videos
    deeplabcut.create_labeled_video(config_path, [file_to_analyse], videotype='.mp4', save_frames=False, draw_skeleton=True, filtered= False)

    print(f"{file_to_analyse} Analysed! Yay!")
