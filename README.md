# TikTok_Generator

> [!WARNING] 
> For educational purposes only

# Install
- pip install pytube
- pip install moviepy
- pip install numpy
- apt install imagemagick 
- pip install opencv-python
- pip install scikit-image
- pip install python-dotenv
- pip install unidecode

# How to use
## Principal use
```
python3 main.py entry.csv
```
### csv
| Link | time_code_start | time_code_end | description | Hashtag | on screen message
| ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |
| http from ytb  | 0 (not tested)  | 0 (not tested)  | "not actual in use"  | "separate by space"  | "max 25 characters"  |
## Download video
```
python3 ytb_download.py /path/to/LINK
```
## Create the template and cut in part
```
python3 Template.py /path/to/Principal_video /path/to/Second_video time_code_start time_code_end "Comment" 
```
## Upload video to tiktok
```
python3 tiktok_uploader.py /path/to/video "titre" "hashtag separete by space"
```
### Option 1 (not working)
- https://pypi.org/project/tiktok-uploader/
- pip install tiktok-uploader

### Option 2
- pip install selenium
- https://www.gregbrisebois.com/posts/chromedriver-in-wsl2/

# Bug
- when processing finished before and text input
- can't use emoji and need to put character before # when input to tiktok
- need to have enough size screen to click on post button
- can't use emoji in video editing