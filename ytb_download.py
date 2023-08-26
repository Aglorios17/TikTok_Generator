import os
from pytube import YouTube
import sys
from dotenv import load_dotenv
from unidecode import unidecode
import re

def delete_parenthese(input_string):
    try:
        # Define a regular expression pattern to match text within parentheses
        pattern = r'\([^)]*\)'
        # Use the re.sub() function to remove the matched text
        output_string = re.sub(pattern, '', input_string)
        return output_string
    except:
        return input_string

def Download(link, output_directory):
    youtubeObject = YouTube(link)
    youtubeObject = youtubeObject.streams.get_highest_resolution()
    try:
        video_title = delete_parenthese(unidecode(youtubeObject.title)).strip().replace("/", "") + ".mp4"
        #print(f"{video_title} | {output_directory}")
        # Use os.path.join() to create the full file path
        video_path = os.path.join(output_directory, video_title)
        # Set the file path to save the video
        video = youtubeObject.download(output_path=output_directory, filename=video_title)
    except Exception as e:
        print(f"An error has occurred (ytb download) : {e}")
        return None
    print("Download is completed successfully")
    return video  # Return the path to the downloaded file

def Downloader(link, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    return (Download(link, output_directory))

def main():
    for i in range(1, len(sys.argv)):
        Download(sys.argv[i], "./background_videos")

if __name__ == "__main__":
    main()