import os
import sys
from dataclasses import dataclass
from typing import List
import random
import ytb_download
import Template

video_stock = "./base_video"
video_background_stock = "./background_videos"
modified_video_path = "./videos"

@dataclass
class YouTubeVideo:
    url: str
    start_time: int
    end_time: int
    description: str
    hashtag: List[str]
    message: str

def parsed_csv(path):
    print("Parsing CSV")
    entry_list = []
    with open(path, 'r') as file:  
        for line in file:
            if "#" in line:
                continue
            row = line.split("|")
            entry_list.append(YouTubeVideo(
                url=row[0],
                start_time=row[1],
                end_time=row[2],
                description=row[3],
                hashtag=row[4].split(' '),
                message=row[5]
            ))
    return(entry_list)

def main():
    if len(sys.argv) != 2:
        print("Usage: python your_script.py input_file.csv")
        sys.exit(1)
    input_file = sys.argv[1]
    data_list = parsed_csv(input_file)
    
    
    base_video_path = os.path.join(os.getcwd(), video_stock)
    background_video_path = os.path.join(os.getcwd(), video_background_stock)
    complete_video_path = os.path.join(os.getcwd(), modified_video_path)
    
    # Now, you can work with the video_list
    for video in data_list:
        print(f"URL: {video.url}")
        video_path = ytb_download.Downloader(video.url, base_video_path)
        # List all files in the directory
        all_files = os.listdir(background_video_path)
        file_list = [f for f in all_files if os.path.isfile(os.path.join(background_video_path, f))]
        # Check if there are any files in the directory
        if not file_list:
            print("No files found in the directory.")
        else:
            # Choose a random file from the list
            random_file = os.path.join(background_video_path,random.choice(file_list))
        print(random_file)
        Template.Template(complete_video_path, video_path, random_file, video.start_time, video.end_time, video.message)

    
if __name__ == "__main__":
    main()   