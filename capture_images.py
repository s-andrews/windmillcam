#!/usr/bin/env python3
import cv2
import time
import numpy
from PIL import Image, ImageFont, ImageDraw
import datetime


for i in range(600):
    cam = cv2.VideoCapture(0)

    cam.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT,720)

    # We don't want the camera to try to autofocus otherwise it 
    # sometimes ends up focussing on the window instead of the mill

    cam.set(cv2.CAP_PROP_AUTOFOCUS,0)
    cam.set(cv2.CAP_PROP_FOCUS, 0)

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
    cv2.imwrite(filename,image)

    # Wait for the next timepoint.  The whole cycle takes about a minute
    time.sleep(50)
    
    
