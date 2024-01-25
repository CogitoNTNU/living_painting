# Run project

## Prerequisites
### From scratch
To run the application one needs to have the video file of the person to style transfer.

One should make the background of the video file white and the person should be in the center of the video.

### With preprocessed images
1. Download the preprocessed images folder and make sure it is unpacked.
2. Alter the `parent_dir` variable in the function `preprocess_folders()` in `preprocessing/split.py` to the root preprocessed image folder 

## Install 
```bash	
pip install -r requirements.txt
```

## Run
```bash
python main.py
```


