# Warper - Warp images and display the warped in the corners selected.

About:
======
This is the Python version of the code here:
    https://github.com/ramsrigouthamg/codes_public/tree/master/opencv/homography

Which is explained here:
    http://ramsrigoutham.com/2014/06/14/perspective-projection-with-homography-opencv/

Nothing extra going on in here.
Except for the save_transitions part, which saves images to visualize and better understand
the process.


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
