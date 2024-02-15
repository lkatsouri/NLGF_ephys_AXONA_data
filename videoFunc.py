import os.path
from tkinter import *

import cv2
import numpy as np
import imutils
import warnings
import colorsys
from tkinter import filedialog as fd

warnings.filterwarnings('ignore', category=DeprecationWarning)


def flick(x):
    pass


def basicControls(key, speed, i, framejump):
    if key == 'speedup':
        speed = speed - 5
        if speed < 1:
            speed = 1
        cv2.setTrackbarPos('Framerate', 'controls', speed)
        key = 'play'
    if key == 'slowdown':
        speed = speed + 5
        cv2.setTrackbarPos('Framerate', 'controls', speed)
        key = 'play'
    if key == 'rewind':
        i -= 1
        cv2.setTrackbarPos('Video', 'controls', i)
        key = 'pause'
    if key == 'fastforward':
        i += 1
        cv2.setTrackbarPos('Video', 'controls', i)
        key = 'pause'
    if key == 'ffastforward':
        i += framejump
        cv2.setTrackbarPos('Video', 'controls', i)
        key = 'pause'
    if key == 'rrewind':
        i -= framejump
        cv2.setTrackbarPos('Video', 'controls', i)
        key = 'pause'

    return key, speed, i


def behaviorLabels(listnumber):
    if listnumber == 1:
        labels = 'Conspecific #1 1: Headhead, 2: Anogenital, 3: GeneralSniff, 4: Approach, 5: Leaving, 6: Dominance, 7: Passive, 8: Following, 9: Allogrooming, 0: nan'
        behaviorkeys = {ord('1'): 'headhead', ord('2'): 'anogenital', ord('3'): 'sniff', ord('4'): 'approach',
                        ord('5'): 'leave', ord('6'): 'dominance', ord('7'): 'passive', ord('8'): 'follow', ord('9'): 'allogroom',
                        ord('0'): 'nan'}

    if listnumber == 2:
        labels = 'Conspecific #2 1: Headhead, 2: Anogenital, 3: GeneralSniff, 4: Approach, 5: Leaving, 6: Dominance, 7: Passive, 8: Following, 9: Allogrooming, 0: nan'
        behaviorkeys = {ord('1'): 'headhead', ord('2'): 'anogenital', ord('3'): 'sniff', ord('4'): 'approach',
                        ord('5'): 'leave', ord('6'): 'dominance', ord('7'): 'passive', ord('8'): 'follow',
                        ord('9'): 'allogroom',
                        ord('0'): 'nan'}
    if listnumber == 3:
        labels = '1: Start Analysis, 2: Stop Analysis, 3: Intervention'
        behaviorkeys = {ord('1'): 'Start Analysis', ord('2'): 'Stop Analysis', ord('3'): 'Intervention', ord('0'): 'nan'}
    if listnumber == 4:
        labels = 'Nonsocial 1: rearing, 2: self-grooming 2, 3: scratching, 0: nan'
        behaviorkeys = {ord('1'): 'rearing', ord('2'): 'groom', ord('3'): 'scratch', ord('0'): 'nan'}
    if listnumber == 5:
        labels = '1: object1, 2: object2, 0: nan'
        behaviorkeys = {ord('1'): 'object1', ord('2'): 'object2', ord('0'): 'nan'}
    if listnumber == 6:
        labels = '1: approach food, 2: sniff food, 3: eat food, 0: nan'
        behaviorkeys = {ord('1'): 'approach_food', ord('2'): 'sniff_food', ord('3'): 'eat_food', ord('0'): 'nan'}
    return labels, behaviorkeys


def addTracking(frame, xcoords, ycoords, probability, numbodyparts, i, reducefrac, threshold=.9):
    HSV_tuples = [(x / numbodyparts, 1, .75) for x in range(numbodyparts)]

    for x in range(numbodyparts):
        color = list(map(lambda j: int(j * 255), colorsys.hsv_to_rgb(*HSV_tuples[x])))

        if probability[i, x] > threshold:
            cv2.circle(frame, center=(np.int(xcoords[i, x] * reducefrac), np.int(ycoords[i, x] * reducefrac)), radius=4,
                       color=(color[2], color[1], color[0]), thickness=-1)
    return frame


def playVideo(widthset=500, framejump=10, annotation=False, listnumber=1, tracking=False, threshold=0.9):
    print('choose Video File')
    root = Tk()
    videopath = fd.askopenfilename()
    root.withdraw()
    videofolder = os.path.split(videopath)[0]
    videofile = os.path.split(videopath)[1]

    # create video windows
    cv2.namedWindow('image')
    cv2.namedWindow('controls')
    controls = np.zeros((50, 750), np.uint8)
    cv2.putText(controls, 'Z: play, X: pause, S: SlowDown, Q: SpeedUp, r/R: Rewind, f/F: Fastforward, P: Exit',
                (40, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)

    # import video
    cap = cv2.VideoCapture(videopath)
    framenum = np.int(cap.get(7))
    originalwidth = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    reducefrac = widthset / originalwidth

    # initialize parameters for video viewing
    i = 0
    speed = 30
    cv2.createTrackbar('Video', 'controls', 0, int(framenum) - 1, flick)
    cv2.setTrackbarPos('Video', 'controls', 0)
    cv2.createTrackbar('Framerate', 'controls', 1, 200, flick)
    cv2.setTrackbarPos('Framerate', 'controls', speed)
    key = 'pause'
    initialkey = {ord('z'): 'play', ord('x'): 'pause', ord('s'): 'slowdown', ord('q'): 'speedup', ord('p'): 'quit',
                  ord('r'): 'rewind', ord('f'): 'fastforward', ord('F'): 'ffastforward', ord('R'): 'rrewind'}

    if annotation:
        cv2.namedWindow('labelbar')
        labelbar = np.zeros((50, 1500), np.uint8)
        cv2.putText(labelbar, behaviorLabels(listnumber)[0], (40, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)
        cv2.imshow('labelbar', labelbar)
        setText = 'nan'
        initialkey.update(behaviorLabels(listnumber)[1])
        # try to load annotated file
        try:
            annotateValues = np.load(videofolder + '/' + videofile[:-4] + '_annotation_set'+str(listnumber)+'.npy')
            annotateValues = np.array(annotateValues, dtype='<U32')
        except:
            annotateValues = np.array(np.full(framenum, 'nan'), dtype='<U32')

    if tracking:
        root = Tk()
        trackingpath = fd.askopenfilename()
        root.withdraw()
        coords = np.loadtxt(trackingpath, delimiter=',', skiprows=3, dtype=np.float16)[:, 1:]
        numbodyparts = np.int(coords.shape[1] / 3)
        probcols = np.arange(2, coords.shape[1], 3)
        xcoords = coords[:, probcols - 2]
        ycoords = coords[:, probcols - 1]
        probability = coords[:, probcols]

    initialkey.update({-1: key, 27: 'exit'})

    while i < framenum:
        cv2.imshow('controls', controls)
        try:
            if i == framenum - 1:
                i = 0

            # load individual frame
            cap.set(cv2.CAP_PROP_POS_FRAMES, i)
            (grabbed, frame) = cap.read(i)
            frame = imutils.resize(frame, width=widthset)
            cv2.putText(frame, str(i), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255))
            if annotation:
                if annotateValues[i] != 'nan':
                    cv2.putText(frame, annotateValues[i], (300, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0))
                else:
                    annotateValues[i] = setText
                    cv2.putText(frame, annotateValues[i], (300, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255))
            if tracking:
                frame = addTracking(frame, xcoords, ycoords, probability, numbodyparts, i, reducefrac,
                                    threshold=threshold)
            cv2.imshow('image', frame)

            # key commands
            initialkey[-1] = key
            key = initialkey[cv2.waitKey(speed)]
            if key == 'play':
                i += 1
                cv2.setTrackbarPos('Video', 'controls', i)
                continue
            elif key == 'pause':
                i = cv2.getTrackbarPos('Video', 'controls')
            elif key == 'quit':
                break
            elif (key == 'slowdown') | (key == 'speedup') | (key == 'rewind') | (key == 'fastforward') | (
                    key == 'ffastforward') | (key == 'rrewind'):
                key, speed, i = basicControls(key, speed, i, framejump)
            else:
                annotateValues[i] = key
                setText = key
                i = i
                key = 'pause'

        except KeyError:
            print('Error')

    cap.release()
    cv2.destroyAllWindows()
    if annotation:
        np.save(videofolder + '/' + videofile[:-4] + '_annotation_set'+str(listnumber)+'.npy', annotateValues)
