# DeepFaceLab Innstalation Guide

## Minimum Requirements:
- Windows or Linux operating system
- 16GB of RAM
- plenty of storage space and pagefile set to 4 x of RAM size minimum
- modern 4 core CPU supporting AVX and SEE intructions
- modern Nvidia or AMD GPU with 6GB og VRAM

## Download and install 
- Go to: https://github.com/iperov/DeepFaceLab and scroll down to the releases.
- Download one of the releases.
- Doubleclick on the .exe file or use another zipfileprogram to extract. Now you will have a folder labeled: *DeepFaceLab_NVIDIA*

# DeepFaceLab Deepfake Guide

## Add your own videos
If you already have to files labeled:
- *data_dst.mp4*
- *data_src.mp4*

Delete them. Add your videos to the *workspace* folder and rename the video of the person that will be deepfaked to:
- *data_dst.mp4*

Rename the video of the person that you will use the face of to:
- *data_src.mp4*


## Extract Images
- Doubleclick on the file labeled: *2) extract images from video data_src.bat*
  - Click on enter a few times to use the default values
- Doubleclick on the file labeled: *3) extract images from video data_dst FULL FPS.bat*  
  - Click on enter a few times to use the default values

## Extract Facesets
- Doubleclick on the file labeled: *4) data_src faceset extract.bat*
  - Use the default settings
  - After a few minutes the extraction will complete and report on the number og images and faces detected 
- Doubleclick on the file labeled: *5) data_sdst faceset extract.bat*
  - Do the same as the last step

### View Facesets
You can view the extracted faces and remove unwanted ones by opening these files:
- *4.1) data_src view aligned result*
- *5.1) data_dat view aligned result*
<img width="1013" alt="image" src="https://user-images.githubusercontent.com/99129702/199445989-4f4fc012-6b11-4daf-9089-5e0b0d988130.png">

## Training
- Doubleclick on the file labeled: *6) train Quick96.bat*
  - Click on enter a few times to use the default values
- If the run is successful the training preview window will open
  - If it fails, then you will need to try CPU only training
<img width="474" alt="image" src="https://user-images.githubusercontent.com/99129702/199446808-5a677a14-5d51-4cbc-a618-0a798ad496f5.png">

### Preview Window
- Press *p* to update the preview window
- The lower the line, the better the results will be
- Press *enter* to save the model and exit
  - You can save and restart the training at any time

## Merging
***Stage when the training is complete***
- Doubleclick on the file labeled: *7) merge Quick96.bat*
  - Click on enter a few times to use the default values
In the merging window you will se a map of keyboard commands:
<img width="640" alt="image" src="https://user-images.githubusercontent.com/99129702/199444946-fa7285f7-14e9-4dd4-83e3-1bb77f27de45.png">
You do not need to use all of the commands. These are the most important:
<img width="637" alt="image" src="https://user-images.githubusercontent.com/99129702/199448396-763f0f7f-f4b6-4ae5-9b41-137e01cfae01.png">
The command window will show you wich image you are wathcing and details of the deepfake:
<img width="192" alt="image" src="https://user-images.githubusercontent.com/99129702/199451018-fd19e85a-00e3-46f9-9e07-bad6154d46c5.png">


### The Important Keys
#### Tab
> Switch between the keyboard map and the preview window
#### Period / Greater than
> Advance to the first frame
#### W and S
> Erode mask (boarder of the face)
#### E and D
> Blur mask (blur the boarder of the face)
#### Slash keys
> Override cfg to next frame
#### Shift
> Override cfg up to the last frame
#### Shift + Period / Greater than
> Process reimain frames

### Start the merging
- Advance to the first frame
- Change the erode mask value to 20
- Change the blur mask value to 100
- Apply these setting to the rest of the frames by pressing shift and the slah keys simultaneously
- Process the remaining frames by pressing the shift and period / greater than keys
- Once the merger reahes 100% we can close both windows

## Finishing
Merge our new deepfake frames into a video file with our destination audio
- Doubleclick on the file labeled: *8) merged to mp4.bat*
  - Press *enter* to begin processing
  - Close the window when the merging is done
The video is now done
- Navigate to the *workspace* folder
- The result is called *result.mp4*
You can restart the training at anytime to improve the deepfake
<img width="554" alt="image" src="https://user-images.githubusercontent.com/99129702/199458575-8173a5f1-7501-4d02-973e-de5f1b0173d5.png">


