import os
import random
from moviepy.editor import CompositeVideoClip, VideoFileClip, VideoClip, TextClip, clips_array, ColorClip
from moviepy.editor import *
from moviepy.config import change_settings
import scipy.ndimage
import shutil
import numpy as np
import sys
import cv2

change_settings({"IMAGEMAGICK_BINARY": r"C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"})
# Set the dimensions for a TikTok video (vertical orientation)
width = 1080 # width remains constant
height = 1920  # height for 9:16 aspect ratio
time_clip = 65
background_color = [220, 220, 220]
max_line_length = 26

def background_txt_color():
    # Define an array of RGB color values
    colors = [
        (255, 0, 0),    # Red
        (0, 255, 0),    # Green
        (0, 0, 255),    # Blue
        (255, 255, 0),  # Yellow
        (255, 0, 255),  # Magenta
        (0, 255, 255),  # Cyan
        (128, 0, 128),  # Purple
        (255, 165, 0),  # Orange
        (0, 128, 0),    # Dark Green
        (128, 128, 128) # Gray
    ]

    # Choose a random RGB color
    random_color = random.choice(colors)
    return (random_color)


# Define a custom blur function (box blur)
def blur(image):
    """ Returns a blurred (radius=2 pixels) version of the image with preserved color """
    blurred_red = scipy.ndimage.gaussian_filter(image[:, :, 0].astype(float), sigma=2)
    blurred_green = scipy.ndimage.gaussian_filter(image[:, :, 1].astype(float), sigma=2)
    blurred_blue = scipy.ndimage.gaussian_filter(image[:, :, 2].astype(float), sigma=2)
    
    blurred_image = np.stack((blurred_red, blurred_green, blurred_blue), axis=-1)
    
    return blurred_image


# Create a function to generate the frame
def make_frame(t):
    frame = (background_color * np.ones((height, width, 3))).astype('uint8')  # White background
    return frame

def Template(path, path2, comment):
    background_txt_color_value = background_txt_color()
    # create list with all video data
    data_info = []
    
    # create directory to store video
    new_directory, file_extension = os.path.splitext(path)
    filename = os.path.basename(path)
    basename, basename_extension = os.path.splitext(filename)

    if not os.path.exists(new_directory):
        os.mkdir(new_directory)
    
    # Define the path to the new folder
    new_folder_path = os.path.join(os.getcwd(), new_directory)
    
    # Load the original video
    original_video = VideoFileClip(path)
    original_second_video = VideoFileClip(path2)
    
    # Calculate the total number of parts
    total_parts = int(original_video.duration // time_clip) + 1
    
    # Split the video into multiple parts
    video_parts = []
    for part_index in range(total_parts):
        start_time = part_index * time_clip
        end_time = min((part_index + 1) * time_clip, original_video.duration)
        if original_video.duration - end_time < 20:
            end_time = original_video.duration
            part = original_video.subclip(start_time, end_time)
            video_parts.append(part)
            break
        part = original_video.subclip(start_time, end_time)
        video_parts.append(part)
    
    # Write each part to a separate file
    for part_index, part in enumerate(video_parts):
        # Resize the original video to fit within the TikTok frame while maintaining aspect ratio
        resized_video = part.resize(width=width)
        resized_video = resized_video.set_position(('center', 0.2), relative=True)  # Center vertically

        # Create a video clip with the make_frame function
        video_clip = VideoClip(make_frame, duration=15)  # Duration in seconds

        # Write the video to a file
        video_clip.write_videofile("tiktok_frame.mp4", fps=24)
        # Convert the black frame into a VideoClip with the same duration as the resized video
        tiktok_frame_clip = VideoFileClip("tiktok_frame.mp4").subclip(0, resized_video.duration)
        tiktok_frame_clip = tiktok_frame_clip.set_position(("center", "center"))  # Center vertically

        # Generate a text clip
        
        # Split the long text into multiple lines
        lines = [comment[i:i+max_line_length] for i in range(0, len(comment), max_line_length)]
        # Create a list of TextClip objects for each line
        txt_clip = TextClip(
            txt=f"Part {part_index + 1} - {comment}",
            fontsize = 64,
            font= 'Roboto-Bold',
            color = 'black'
            )
        txt_clip = txt_clip.set_position('center')
        
        image_width, image_height = txt_clip.size
        
        color_clip = ColorClip(
                        size=(int(image_width*1.1), int(image_height*1.4)),
                        color=background_txt_color_value
                    )
        color_clip = color_clip#.set_opacity(.5)
        
        
        clip_to_overlay = CompositeVideoClip([color_clip, txt_clip])
        clip_to_overlay = clip_to_overlay.set_position(('center', 0.6), relative=True).set_duration(resized_video.duration)
        # setting position of text in the center and duration will be 10 seconds
        
        # second video
        # Calculate the scaling factor for width and height
        width_scale = width / original_video.size[0]
        height_scale = height / original_video.size[1]
        # Choose the larger scaling factor to ensure the video fills the frame
        scale_factor = max(width_scale, height_scale)
        
        # Second video
        # Generate a random start time within the valid range
        start_time_random = random.uniform(0, original_second_video.duration - time_clip)
        # Calculate the end time based on the start time and sub-video duration
        end_time_random = start_time_random + time_clip
        random.seed()
        # Select the sub-video using subclip and blur
        second_video = original_second_video.without_audio().subclip(start_time_random, end_time_random).fl_image(blur)
        cropped_video = second_video.resize(height=int(original_video.size[1] * scale_factor)).set_position("center", "center").set_duration(resized_video.duration) 
        
        
        # Composite the resized video onto the TikTok frame
        video_with_frame = CompositeVideoClip([tiktok_frame_clip, cropped_video, resized_video, clip_to_overlay])
        # Write the final video to a file 
        # Construct the full output file path
        output_file_path = os.path.join(new_folder_path, f"part_{part_index + 1}_"+ filename)
        video_with_frame.write_videofile(output_file_path, codec="libx265", fps=original_video.fps)

        # add data to data_info
        data_info.append(f"part {part_index + 1} {basename} | {output_file_path}" )
    # Close the original video clip
    original_video.close()
    cropped_video.close()
    tiktok_frame_clip.close()
    # Check if the file exists before attempting to remove it
    if os.path.exists("tiktok_frame.mp4"):
        # Remove the file
        os.remove("tiktok_frame.mp4")

    # Open the file for writing
    data_path = os.path.join(new_folder_path, basename + ".txt")
    with open(data_path, "w") as file:
        # Write each text element from the list to the file
        for item in data_info:
            file.write(item + "\n")
    
#for i in range(1, len(sys.argv)):
Template(sys.argv[1], sys.argv[2], sys.argv[3])
#    i += 1
