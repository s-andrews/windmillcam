#!/usr/bin/env python3
import cv2
import time
import numpy
from PIL import Image, ImageFont, ImageDraw
import datetime
from pathlib import Path
from suntime import Sun
from datetime import datetime,timedelta, timezone
import subprocess

data_folder = Path("/home/andrewss/Windmill_Images")
# We use this for getting sunrise and sunset times
sun = Sun(52.1951,0.1313)


def main():

    # We loop forever so we can collect for multiple days
    while True:
        # Figure out how many minutes it is until the next sunset
        sunset_time = get_sunset_time()

        # Create a folder for today
        todays_folder = create_folder_for_today()

        # Capture images
        print("Capturing images until ",sunset_time, flush=True)
        capture_images(sunset_time,todays_folder)

        # Create the video from todays images
        print("Creating video from images in",todays_folder, flush=True)
        create_video(todays_folder)

        # Upload to youtube?

        # Sleep until sunrise
        sleep_until_sunrise()


def get_sunset_time():
    # We don't want the actual sunset time, we'll go 30 mins
    # beyond that so we get a video which fades to black

    return sun.get_sunset_time(datetime.today()+timedelta(days=1))

    #return sun.get_sunset_time(datetime.today())+timedelta(minutes=30)


def create_folder_for_today():
    folder_name = datetime.now().strftime("%Y_%m_%d")
    folder = data_folder / folder_name

    if not folder.exists():
        folder.mkdir()

    return folder

def create_video(folder):
    # ffmpeg -framerate 15 -pattern_type glob -i '*.png' -c:v libx264 -vf fps=15 -pix_fmt yuv420p 2024_03_13.mp4

    # Make an output file name from the folder name
    output_file = folder.name + ".mp4"

    if (folder / output_file).exists():
        # The video has already been made for today
        return
    
    files = [x for x in folder.glob("*png")]
    if not files:
        print("No PNG files, not trying to make video", flush=True)
        return
    

    subprocess.run(["ffmpeg", "-framerate", "15", "-pattern_type", "glob", "-i", "*.png", "-c:v", "libx264", "-vf", "fps=15", "-pix_fmt", "yuv420p", output_file], cwd=folder)

def sleep_until_sunrise():
    tomorrow_sunrise = sun.get_sunrise_time(datetime.today()+timedelta(days=1))
    print("Tomorrows sunrise is at",tomorrow_sunrise, flush=True)
    time_to_wait = (tomorrow_sunrise - datetime.now(timezone.utc)).total_seconds()

    # We want to start the video a bit before the sunrise so we take off 30 mins
    time_to_wait -= (60*30)
    print("Sleeping for",time_to_wait,"seconds", flush=True)

    time.sleep(time_to_wait)



def capture_images(time_until,folder):

    # Rather than restart the camera for each shot (once a minute)
    # we'll leave it running.  Hopefully that will give better
    # consistency in the photos

    print ("Starting camera", flush=True)
    cam = cv2.VideoCapture(0)

    cam.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT,720)

    # We tried setting these values to disable autofocus but they
    # weren't accepted by the gstreamer backend.  We appear to do
    # the same thing using:
    # sudo v4l2-ctl -c focus_automatic_continuous=0
    # via v4l but who knows if that works.
    # It does seem to stick though
    # cam.set(cv2.CAP_PROP_AUTOFOCUS,0)
    # cam.set(cv2.CAP_PROP_FOCUS, 0)

    # When the camera first starts it sometimes takes a while for 
    # the auto-exposure to settle down, so we need to wait for it
    # to stablise 

    time.sleep(5)

    # We'll capture and throw away a few images as these also seem
    # to help the camera to settle
    print("Capturing images to settle camera", flush=True)
    for _ in range(5):
        cam.read()

    while True:

        if datetime.now(timezone.utc) > time_until:
            print("Stopping capture as",datetime.now(timezone.utc),"is later than",time_until, flush=True)
            break

        # Now we can capture the image
        result,image = cam.read()

        image = cv2.rotate(image,cv2.ROTATE_90_COUNTERCLOCKWISE)

        # Convert to PIL image for adding font
        image = Image.fromarray(image)

        # Get a drawing context so we can add the time to the image
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMono.ttf",32)

        # Get the time in a form suitable for writing to the image
        date = datetime.now().strftime("%a %d %b %Y %H:%M")

        # Get the time in a form suitable for generating a filename
        filename = datetime.now().strftime("%Y_%m_%d_%H.%M.%S.png")

        # Add the text to the image in a fixed width font
        draw.text((20,1230),date,(255,255,255), font=font)

        # Convert back to a cv2 object
        image = numpy.array(image)

        # Write the file

        filename = str(folder)+"/"+filename

        cv2.imwrite(filename,image)

        # Wait for the next timepoint.  The whole cycle takes about a minute
        time.sleep(50)


    # When we're finished we shut the camera down
    print("Shutting down camera", flush=True)
    cam.release()

        
if __name__ == "__main__":
    main()
