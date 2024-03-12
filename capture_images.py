#!/usr/bin/env python3
import cv2
import time
import numpy
from PIL import Image, ImageFont, ImageDraw
import datetime
from pathlib import Path

data_folder = Path("/home/andrewss/Windmill_Images")

def main():
    # We loop forever
    while True:
        # Figure out how many minutes it is until the next sunset
        mins_to_sunset = get_mins_to_sunset()

        # Create a folder for today
        todays_folder = create_folder_for_today()

        # Capture images
        capture_images(mins_to_sunset,todays_folder)

        # Create the video from todays images
        create_video(todays_folder)

        # Sleep until sunrise
        sleep_until_sunrise()


def get_mins_to_sunset():
    return 10


def create_folder_for_today():
    folder_name = datetime.datetime.now().strftime("%Y_%m_%d")
    folder = data_folder / folder_name

    if not folder.exists():
        folder.mkdir()

    return folder

def create_video(folder):
    pass

def sleep_until_sunrise():
    pass


def capture_images(minutes,folder):
    for i in range(minutes):
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

        # Now we can capture the image
        result,image = cam.read()

        # We can shut the camera down now
        cam.release()

        image = cv2.rotate(image,cv2.ROTATE_90_COUNTERCLOCKWISE)

        # Convert to PIL image for adding font
        image = Image.fromarray(image)

        # Get a drawing context so we can add the time to the image
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMono.ttf",32)

        # Get the time in a form suitable for writing to the image
        date = datetime.datetime.now().strftime("%a %d %b %Y %H:%M.%S")

        # Get the time in a form suitable for generating a filename
        filename = datetime.datetime.now().strftime("%Y_%m_%d_%H.%M.%S.png")

        # Add the text to the image in a fixed width font
        draw.text((20,1230),date,(255,255,255), font=font)

        # Convert back to a cv2 object
        image = numpy.array(image)

        # Write the file

        filename = str(folder)+"/"+filename

        cv2.imwrite(filename,image)

        # Wait for the next timepoint.  The whole cycle takes about a minute
        time.sleep(50)
        
if __name__ == "__main__":
    main()
