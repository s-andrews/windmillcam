WindmillCam
===========

This is the code which runs the capture systems for generating images of Burwell Windmill.  The system generates a time lapse video each day and uploads it to our [YouTube Channel](https://www.youtube.com/#BurwellWindmillcam)

The system runs on a Raspberry Pi and is connected to a Logitech C920 webcam.

Installation
------------

To run the system we use a default Raspberry Pi OS image.  Package installs we added were:

```
apt-get install build-essential cmake pkg-config libjpeg-dev libtiff5-dev libjasper-dev libpng-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libfontconfig1-dev libcairo2-dev libgdk-pixbuf2.0-dev libpango1.0-dev libgtk2.0-dev libgtk-3-dev libatlas-base-dev gfortran libhdf5-dev libhdf5-serial-dev libhdf5-103 python3-pyqt5 python3-dev python3-opencv
```

Importantly, on our Pi3 we found that the wireless card would stop talking after a few hours.  To fix this we disabled the cards power management.

We put this into /etc/rc.local

```
/sbin/iwconfig wlan0 power off
```


For the system we initially check out a copy of the code

```
git clone https://github.com/s-andrews/windmillcam.git
```

We then create a virtual env in which to run the system and install the dependencies

```
cd windmillcam
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

We can then run the system

```
nohup ./capture_images.py > ~/windmillcam.log &
```