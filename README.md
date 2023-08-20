# TikTok_Money_Generator

# Install
- pip install pytube
- pip install moviepy
- pip install numpy
- apt install imagemagick 
- pip install opencv-python
- pip install scikit-image
- pip install python-dotenv

# How to use
## Download video
python3 ytb_download.py $LINK

## Create the template and cut in part
python3 Template.py $Principal_video $Second_video $Comment 

## Upload video to tiktok

### Option 1 (not working)
- https://pypi.org/project/tiktok-uploader/
- pip install tiktok-uploader

### Option 2
- pip install selenium
- https://www.gregbrisebois.com/posts/chromedriver-in-wsl2/