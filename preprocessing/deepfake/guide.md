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

## Training
- Doubleclick on the file labeled: *6) train Quick96.bat*
  - Click on enter a few times to use the default values
- If the run is successful the training preview window will open
  - If it fails, then you will need to try CPU only training
### Preview Window
- Press *p* to update the preview window
- The lower the line, the better the results will be
- Press *enter* to save the model and exit
  - You can save and restart the training at any time

## Merging
**Stage when the training is complete**
- Doubleclick on the file labeled: *7) merge Quick96.bat*
  - Click on enter a few times to use the default values
