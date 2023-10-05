#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
from main import *
from PIL import Image as im

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd7in5_V2
import time
from PIL import Image, ImageDraw, ImageFont
import traceback

logging.basicConfig(level=logging.DEBUG)

try:
    epd = epd7in5_V2.EPD()

    epd.init()


    i = 0

    while True:
        print(x, y)
        if i % 3 == 0:
            getcontext().prec = getcontext().prec + 1
        arr = render(x, y, w, h, res_x=RES_X, res_y=RES_Y, iter=iterations)

        # Render
        plt.imshow(arr)
        plt.show()

        fig = plt.figure()
        ax1 = fig.add_subplot()
        pos1 = ax1.imshow(arr, cmap='gray')
        image = im.frombytes('1', fig.canvas.get_width_height(), fig.canvas.tostring_rgb())
        image.save('out.bmp')

        epd.Clear()
        Himage = Image.open('out.bmp')
        epd.display(epd.getbuffer(Himage))
        logging.info("Goto Sleep...")
        epd.sleep()

        choices = []
        # Upper left
        if not is_uniform_array(arr, RES_X / 2, RES_Y / 2, 0, 0):
            print("Upper left is not uniform")
            choices += [(x - w / 4, y + h / 4)]
            # Upper right
        if not is_uniform_array(arr, RES_X / 2, RES_Y / 2, RES_X / 2, 0):
            print("Upper right is not uniform")
            choices += [(x + w / 4, y + h / 4)]
         # Lower left
         if not is_uniform_array(arr, RES_X / 2, RES_Y / 2, 0, RES_Y / 2):
            print("Bottom left is not uniform")
            choices += [(x - w / 4, y - h / 4)]
        # Lower right
        if not is_uniform_array(arr, RES_X / 2, RES_Y / 2, RES_X / 2, RES_Y / 2):
            print("Bottom right is not uniform")
            choices += [(x + w / 4, y - h / 4)]

        w = w / 2
        h = h / 2

        x, y = random.choice(choices)
        iterations += 100

        file = open('save.dat', 'w')
        file.write(str(x))
        file.write(str(h))
        file.write(str(w))
        file.write(str(h))
        file.close()

        i += 1

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd7in5_V2.epdconfig.module_exit()
    exit()