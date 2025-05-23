# Python file here: run deeplabcut to train model. 

import deeplabcut
config_path = r"C:\Users\mtirole\Documents\DeepLabCut\RoomG\config.yaml"

file_to_analyse= r'C:\Users\mtirole\Documents\DeepLabCut\RoomG\to_analyse\MT17_202-02-25\Video\1_2023-02-25_10-24-44.mp4'

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

# add analyse video
deeplabcut.analyze_videos(config_path, [file_to_analyse], save_as_csv=True, gputouse=0)
print("VideoAnalysed")

# filter trajectories
deeplabcut.filterpredictions(config_path, [file_to_analyse], shuffle=1, filtertype='arima', p_bound=0.01, ARdegree=3, MAdegree=1, alpha=0.01)
print("VideoFiltered")

# plot trajectories
deeplabcut.plot_trajectories(config_path,[file_to_analyse],shuffle=1,displayedbodyparts= ['nose','leftEar','rightEar','neck','body1','body2','body3','tailBase']) # filtered=True,
 
# create labeled videos
# deeplabcut.create_labeled_video(config_path, [file_to_analyse], videotype='.mp4', save_frames=True,
# 						 displayedbodyparts= ['nose','leftEar','rightEar','neck','body1','body2','body3','tailBase',
# 						 'leftLightOn','rightLightOn','leftPortScrew','rightPortScrew','odorPort','leftEdgeWell',
# 						 'leftWell','midEdgeWell','rightWell','rightEdgeWell'], draw_skeleton=True) #, filtered= True
# 						 # draw_skeleton=True, trailpoints=0, filtered= False,

deeplabcut.create_labeled_video(config_path, [file_to_analyse], videotype='.mp4', save_frames=False, draw_skeleton=True, filtered= True)
print("Labelled video(s) created")
