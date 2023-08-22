import os
import sys
from dataclasses import dataclass
import time
from typing import List
import random
import ytb_download
import Template
import tiktok_uploader
from unidecode import unidecode

video_stock = "./base_video"
video_background_stock = "./background_videos"
modified_video_path = "./videos"

@dataclass
class YouTubeVideo:
    url: str
    start_time: int
    end_time: int
    description: str
    hashtag: str
    message: str

def get_new_txt_files(directory):
    # Get a list of all files in the specified directory
    all_files = os.listdir(directory)
    
    # Filter the list to include only files that start with "new_" and end with ".txt"
    new_txt_files = [f for f in all_files if f.startswith("new_") and f.endswith(".txt")]
    
    return new_txt_files

def rename_files(directory):
    # Get a list of all files in the specified directory
    all_files = os.listdir(directory)

    for filename in all_files:
        if filename.startswith("new_") and filename.endswith(".txt"):
            # Construct the new file name by removing "new_" from the start
            new_filename = filename.replace("new_", "")

            # Create the full paths for the old and new file names
            old_file_path = os.path.join(directory, filename)
            new_file_path = os.path.join(directory, new_filename)

            # Rename the file
            os.rename(old_file_path, new_file_path)
            print(f"Renamed: {old_file_path} -> {new_file_path}")

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
                description=unidecode(row[3]).strip(),
                hashtag=unidecode(row[4]).strip(),
                message=unidecode(row[5]).strip()
            ))
    return(entry_list)

def main():
    if len(sys.argv) != 3:
        print("Usage: python your_script.py input_file.csv")
        sys.exit(1)
    input_file = sys.argv[1]
    all_script = sys.argv[2]
    data_list = parsed_csv(input_file)
    
    
    base_video_path = os.path.join(os.getcwd(), video_stock)
    background_video_path = os.path.join(os.getcwd(), video_background_stock)
    complete_video_path = os.path.join(os.getcwd(), modified_video_path)
    
    # Now, you can work with the video_list
    for video in data_list:
        if all_script == "1":
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
            time.sleep(5)
            
        # Get a list of all text files that start with "new_"
        new_txt_files = get_new_txt_files(complete_video_path)
        succes = False
        if new_txt_files:
            print("Found the following new_txt files:")
            for file in new_txt_files:
                path_file = os.path.join(complete_video_path, file)
                with open(path_file, 'r') as file:  
                    for line in file:
                        data = line.split("|")
                        print(data)
                        success = tiktok_uploader.uploader(data[1], data[0], video.hashtag)
                        time.sleep(2)
            if succes:
                rename_files(complete_video_path)
        else:
            print("No new_txt files found.")
if __name__ == "__main__":
    main()   