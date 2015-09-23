# Warper
Warp images and display the warped in the corners selected.

Requirements:
-------------
The following should be installed in your system:
* Python 2.7.x
* OpenCV 2.4.8 with Python wrappers
* Numpy 1.8.1 or above


Usage:
------
Assuming you have made the `wrp.py` script executable, you can do:

    ./wrp.py <path-to-main-image> <path-to-overlay-image> <1 or 0 to save transitions>

The third arg, if provided, will save the transitions to disk. It can be anything. Will improve later with optargs.

Example:

	./wrp.py main.jpg logo.jpg 1  # Will save transitions to disk
	./wrp.py main.jpg logo.jpg    # Transitions will not be saved
