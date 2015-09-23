#!/usr/bin/env python
"""
ABOUT:
======
This is the Python version of the code here:
    https://github.com/ramsrigouthamg/codes_public/tree/master/opencv/homography

Which is explained here:
    http://ramsrigoutham.com/2014/06/14/perspective-projection-with-homography-opencv/

Nothing extra going on in here.
Except for the save_transitions part, which saves images to visualize and better understand
the process.

USAGE:
======
 ./wrp.py <path-to-main-image> <path-to-overlay-image> <1 or 0 to save transitions>

The third arg, if provided, will save the transitions to disk. It can be anything.
Will improve later with optargs.

Example:
./wrp.py main.jpg logo.jpg 1  # Will save transitions to disk
./wrp.py main.jpg logo.jpg    # Transitions will not be saved

"""
import sys
import os

import cv2
import numpy as np

__author__ = "github.com/noodlebreak"
__license__ = "Apache v2.0"


class Warper:

    # We need 4 corresponding 2D points(x, y) to calculate homography.
    left_image = []     # Stores 4 points(x,y) of the logo image. Here the four points are 4 corners of image.
    right_image = []    # stores 4 points that the user clicks(mouse left click) in the main image.

    gray = None
    gray_inv = None
    src1final, src2final = None, None

    SAVE_TRANSITIONS = False

    def load_images(self, path1, path2):
        # Load images from arguments passed.
        self.image_main = cv2.imread(path1, 1)
        self.image_logo = cv2.imread(path2, 1)

    def lr_populate(self):
        # Push the 4 corners of the logo image as the 4 points for correspondence to calculate homography.
        self.left_image.append((float(0), float(0)))
        self.left_image.append((float(0), float(self.image_logo.shape[0])))
        self.left_image.append((float(self.image_logo.shape[1]), float(self.image_logo.shape[0])))
        self.left_image.append((float(self.image_logo.shape[1]), float(0)))

    def save_transitions(self, src1, src2):

        if not os.path.exists('out'):
            # Create output dir for transition images
            os.mkdir('out')

        if self.SAVE_TRANSITIONS:
            cv2.imwrite('out/1_main.jpg', src1)
            cv2.imwrite('out/1_logo_warped.jpg', src2)
            cv2.imwrite('out/2_logowarped_gray.jpg', self.gray)
            cv2.imwrite('out/3_logowarped_gray_inv.jpg', self.gray_inv)
            cv2.imwrite('out/4_main_AND_logograyinv.jpg', self.src1final)
            cv2.imwrite('out/5_logowarped_AND_lgwgray.jpg', self.src2final)
            cv2.imwrite('out/6_final.jpg', self.final_image)

    def show_final(self, src1, src2):
        """
        Function to add main image and transformed logo image and show final output.
        Icon image replaces the pixels of main image in this implementation.
        """

        self.gray = cv2.cvtColor(src2.astype('float32'), cv2.COLOR_BGR2GRAY)
        retval, self.gray = cv2.threshold(self.gray, 0, 255, cv2.THRESH_BINARY)
        # adaptiveThreshold(gray,gray,255,ADAPTIVE_THRESH_MEAN_C,THRESH_BINARY,5,4);
        self.gray_inv = cv2.bitwise_not(self.gray.astype('uint8'))
        print("gray shape: {} gray_inv shape: {} \n".format(self.gray.shape, self.gray_inv.shape))

        # Works with bool masks
        self.src1final = cv2.bitwise_and(src1, src1, dst=self.src1final, mask=self.gray_inv)
        self.src2final = cv2.bitwise_and(src2, src2, self.gray)
        self.src2final = self.src2final.astype('uint8')

        # final_image = cv2.add(src1final, src2final)
        self.final_image = self.src1final + self.src2final
        self.save_transitions(src1, src2)

        cv2.imshow("output", self.final_image)
        #  Press "Escape button" to exit
        while True:
            key = cv2.waitKey(10) & 0xff
            if key == 27:
                break
        sys.exit(0)

    def on_mouse(self, e, x, y, d, ptr):
        """
        Here we get four points from the user with left mouse clicks.
        On 5th click we output the overlayed image.
        """
        if e == cv2.EVENT_LBUTTONDOWN:
            if len(self.right_image) < 4:
                self.right_image.append((float(x), float(y)))
                print("%d  %d \n" % (x, y))
            else:
                print(" Calculating Homography \n")
                # Deactivate callback
                # cv2.setMouseCallback("Display window", None)
                cv2.destroyWindow('Display window')

                self.left_image = np.array(self.left_image)
                self.right_image = np.array(self.right_image)

                # once we get 4 corresponding points in both images calculate homography matrix
                H, status = cv2.findHomography(self.left_image, self.right_image, 0)
                logoWarped = None

                # Warp the logo image to change its perspective
                logoWarped = np.int32(cv2.warpPerspective(self.image_logo, H, self.image_main.shape[:2][::-1]))
                self.show_final(self.image_main, logoWarped)

if __name__ == '__main__':
    #  We need two argumemts. "Main image" and "logo image"
    argc = len(sys.argv)
    argv = sys.argv

    if argc < 3:
        print(" Usage: error \n")
        sys.exit(0)

    warper = Warper()
    warper.load_images(argv[1], argv[2])
    warper.lr_populate()

    if len(argv) == 4:
        warper.SAVE_TRANSITIONS = True

    # cv2.imshow("Display window", WINDOW_AUTOSIZE)  # Create a window for display.
    cv2.imshow("Display window", warper.image_main)
    cv2.setMouseCallback("Display window", warper.on_mouse, warper)

    #  Press "Escape button" to exit
    while True:
        key = cv2.waitKey(10) & 0xff
        if key == 27:
            break

    sys.exit(0)
