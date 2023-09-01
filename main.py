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
    channel: str
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

def get_channel(url):
    # Input string
    # Split the string by '=' from the right, with a maximum of 1 split
    parts = url.rsplit('=', 1)

    # Check if there was a '=' in the string
    if len(parts) > 1:
        # The text after the last '=' is in parts[1]
        result = parts[1]
    else:
        # There was no '=', so result is the original string
        result = ""

    # Print the result
    return result.strip()

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
                channel=f"credits : {get_channel(row[0])}",
                start_time=row[1],
                end_time=row[2],
                hashtag=unidecode(row[3]).strip(),
                message=unidecode(row[4]).strip()
            ))
    return(entry_list)

def new_file_failed(index, path):
    try:
        save = []
        with open(path, 'r') as file:
            i = 0 
            for line in file:
                if i == index:
                    save.append[line]
                else:
                    i += 1
        with open(path, 'w') as file:
            for line in save:
                file.write(line)
        print("File has been rewritten.")
    except:
        print("File has failed rewritten.")

def send_to_template(video, all_script, base_video_path, background_video_path, complete_video_path):
    if all_script == "1" or all_script == "2":
            print(f"URL: {video.url}")
            video_path = ytb_download.Downloader(video.url, base_video_path)
            if video_path is None:
                return None
            # List all files in the directory
            all_files = os.listdir(background_video_path)
            file_list = [f for f in all_files if os.path.isfile(os.path.join(background_video_path, f))]
            # Check if there are any files in the directory
            if file_list is None:
                print("No files found in the directory.")
                return None
            else:
                # Choose a random file from the list
                random_file = os.path.join(background_video_path,random.choice(file_list))
            print(random_file)
            if Template.Template(complete_video_path, video_path, random_file, video.start_time, video.end_time, video.message) is None:
                return None
            time.sleep(5)
    return 1

def send_to_tiktok(complete_video_path, video):
    new_txt_files = get_new_txt_files(complete_video_path)
    succes = False
    if new_txt_files:
        print("Found the following new_txt files:")
        for file in new_txt_files:
            path_file = os.path.join(complete_video_path, file)
            index = 0
            with open(path_file, 'r') as file:  
                for line in file:
                    data = line.split("|")
                    print(data)
                    success = tiktok_uploader.uploader(data[1], data[0], video.hashtag, video.channel)
                    if succes is None:
                        new_file_failed(index ,file)
                        return None
                    index += 1
                    time.sleep(1)
        if succes is not None:
            rename_files(complete_video_path)
    else:
        print("No new_txt files found.")
        return None
    return 1

def tiktok_automated(input_file, all_script):
    data_list = parsed_csv(input_file)
    print("----debug----",data_list, all_script)
    base_video_path = os.path.join(os.getcwd(), video_stock)
    background_video_path = os.path.join(os.getcwd(), video_background_stock)
    complete_video_path = os.path.join(os.getcwd(), modified_video_path)
    # Now, you can work with the video_list
    for video in data_list:        
        if send_to_template(video, all_script, base_video_path, background_video_path, complete_video_path) is None:
            print("Template error")
            return None
        # Get a list of all text files that start with "new_"
        if all_script != "2" and send_to_tiktok(complete_video_path, video) is None:
            print("Send to Tiktok error")
            return None
    return True

def main():
    if len(sys.argv) != 3:
        print("Usage: python your_script.py input_file.csv flag(0/1/2)")
        sys.exit(1)
    input_file = sys.argv[1]
    all_script = sys.argv[2]
    
    if tiktok_automated(input_file, all_script) is None:
        return None

if __name__ == "__main__":
    main()   