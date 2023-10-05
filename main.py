from math import *
from decimal import *
import random

def mandel_point(C_x,C_y, iter):
    Z_x = C_x
    Z_y = C_y
    for i in range(0,iter):
        Z_x_old = Z_x
        Z_x = Z_x*Z_x - Z_y*Z_y + C_x
        Z_y = 2*Z_x_old*Z_y + C_y
        if (Z_x**2+Z_y**2)>4:
            return 0
    return 1

def render(x,y,w,h,res_x=800,res_y=800, iter=100):
    columns = []
    for y_offset_i in range(res_y,0,-1):
        row = []
        for x_offset_i in range(0,res_x):
            p_x = x-w/Decimal(2)+Decimal(x_offset_i)/Decimal(res_x)*w
            p_y = y-h/Decimal(2)+Decimal(y_offset_i)/Decimal(res_y)*h

            row += [mandel_point(p_x,p_y, iter)]
        columns += [row]

    return columns


def is_uniform_array(arr,w,h,x_offset,y_offset):
    first_point = arr[int(y_offset)][int(x_offset)]
    for x in range(0,int(w)):
        for y in range(0,int(h)):
            if first_point != arr[int(y_offset)+y][int(x_offset)+x]:
                return False
    return True

RES_X = 800
RES_Y = 480

w = Decimal(4)
h = Decimal(2)
x = Decimal(-1)
y = Decimal(0)

iterations = 100


import matplotlib.pyplot as plt

if __name__ == "__main__":
    for i in range(0,100):
        print(x,y)
        if i%3==0:
            getcontext().prec = getcontext().prec+1
        arr = render(x, y, w, h, res_x = RES_X, res_y = RES_Y, iter=iterations)

        print(i,"is done")
        if i%20==0:
            plt.imshow(arr)
            plt.show()

        choices = []
        #Upper left
        if not is_uniform_array(arr, RES_X/2, RES_Y/2, 0,0):
            print("Upper left is not uniform")
            choices += [(x-w/4,y+h/4)]
        #Upper right
        if not is_uniform_array(arr, RES_X/2, RES_Y/2, RES_X/2,0):
            print("Upper right is not uniform")
            choices += [(x+w/4,y+h/4)]
        #Lower left
        if not is_uniform_array(arr, RES_X/2, RES_Y/2, 0,RES_Y/2):
            print("Bottom left is not uniform")
            choices += [(x-w/4,y-h/4)]
        #Lower right
        if not is_uniform_array(arr, RES_X/2, RES_Y/2, RES_X/2,RES_Y/2):
            print("Bottom right is not uniform")
            choices += [(x+w/4,y-h/4)]

        w = w/2
        h = h/2

        x, y = random.choice(choices)
        iterations += 100

        file = open('save.dat', 'w')
        file.write(str(x))
        file.write(str(h))
        file.write(str(w))
        file.write(str(h))
        file.close()
