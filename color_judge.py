import PIL
import numpy as np
from matplotlib import pyplot as plt
from tkinter import*
import math
import random
class Center(object):
    def __init__(self,centerposition=[0,0,0]):
        self.position=centerposition
        self.buddies=[]

class Point(object):
    def __init__(self,pointposition=[0,0,0]):
        self.position=pointposition
        self.boss=None

#=====================================================

def hsv2rgb(hsv):
    h = float(hsv[0])
    s = float(hsv[1])
    v = float(hsv[2])
    h60 = h / 60.0
    h60f = math.floor(h60)
    hi = int(h60f) % 6
    f = h60 - h60f
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    r, g, b = 0, 0, 0
    if hi == 0: r, g, b = v, t, p
    elif hi == 1: r, g, b = q, v, p
    elif hi == 2: r, g, b = p, v, t
    elif hi == 3: r, g, b = p, q, v
    elif hi == 4: r, g, b = t, p, v
    elif hi == 5: r, g, b = v, p, q
    r, g, b = int(r * 255), int(g * 255), int(b * 255)
    return (r,g,b)


def rgb2hsv(rgb):
    r, g, b = rgb[0]/255.0, rgb[1]/255.0, rgb[2]/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx-mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:
        h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b:
        h = (60 * ((r-g)/df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = df/mx
    v = mx
    return [h,s,v]

#====================================================


img = PIL.Image.open("test.png")
img=img.resize((160,160),PIL.Image.ANTIALIAS)
img_array = np.array(img)
arr1 = img_array[:]
print(arr1.shape)
points=[]
for x in range(1,arr1.shape[0]):
    for y in range(1,arr1.shape[1]):
        a = img_array[x,y][0]
        b = img_array[x,y][1]
        c = img_array[x,y][2]
        points.append(Point([a,b,c]))
        #points.append(Point(rgb2hsv([a,b,c])))
print("picture loaded")

def distance(a_point,a_center):
    return ((a_center.position[0]-a_point.position[0])**2+(a_center.position[1]-a_point.position[1])**2+(a_center.position[2]-a_point.position[2])**2)**0.5
#def distance(a_point,a_center):
#	theta1=a_point.position[0]/360*2*3.1415926
#	rho1=a_point.position[1]
#	z1=a_point.position[2]
#	theta2=a_center.position[0]/360*2*3.1415926
#	rho2=a_center.position[1]
#	z2=a_center.position[2]
	
#	return math.sqrt(rho1**2+rho2**2-2*rho1*rho2*math.cos(theta1-theta2)+(z1-z2)**2)
def rand_position():
    return [random.randint(1,255),random.randint(1,255),random.randint(1,255)]
centers=[]
for i in range(0,6):
    centers.append(Center(rand_position()))

#for i in range(0,4):
#    centers.append(Center(rgb2hsv(rand_position())))


for i in range(0,10):
    print('finding theme colors step ',i)
    for apoint in points:
        mindist=99999
        for acenter in centers:
            present_dist=distance(apoint,acenter)
            if present_dist<=mindist:
                mindist=present_dist
                apoint.boss=acenter

    for acenter in centers:
        acenter.buddies=[]
        for apoint in points:
            if apoint.boss==acenter:
                acenter.buddies.append(apoint)
        
    for acenter in centers:
        new_x_total,new_y_total,new_z_total=0,0,0
        for apoint in acenter.buddies:
            new_x_total+=apoint.position[0]
            new_y_total+=apoint.position[1]
            new_z_total+=apoint.position[2]
        total_number=len(acenter.buddies)
        if total_number == 0:
            continue
        else:
            acenter.position=[new_x_total/total_number,new_y_total/total_number,new_z_total/total_number]

def color(value):
    digit = list(map(str, range(10))) + list("ABCDEF")
    if isinstance(value, tuple):
        string = '#'
        for i in value:
            a1 = i // 16
            a2 = i % 16
            string += digit[a1] + digit[a2]
        return string
    elif isinstance(value, str):
        a1 = digit.index(value[1]) * 16 + digit.index(value[2])
        a2 = digit.index(value[3]) * 16 + digit.index(value[4])
        a3 = digit.index(value[5]) * 16 + digit.index(value[6])
        return (a1, a2, a3)


 
tk = Tk()
canvas = Canvas(tk,width=500,height=155)
canvas.pack()
x_base=0
X=0
for acenter in centers:
    X=x_base+len(acenter.buddies)/len(points)*500
    r=int(acenter.position[0])
    g=int(acenter.position[1])
    b=int(acenter.position[2])
#=======================================================
    #co=color(hsv2rgb([r,g,b]))
#=======================================================
    #print([r,g,b],len(acenter.buddies))
    co=color((r,g,b))
    canvas.create_rectangle(x_base,0,X,50,fill=co)
    x_base+=len(acenter.buddies)/len(points)*500

#======================================================================================

copyofcenters=[]
for i in centers:
    copyofcenters.append(i)     #copy of centers, just don't wanna use copy.deepcopy

minbuddynum=999999
for acenter in copyofcenters:
    if len(acenter.buddies)==0:
        continue
    else:
        if len(acenter.buddies)<=minbuddynum:
            minbuddynum=len(acenter.buddies)

total_major_color=[[0,0,0],0]
for acenter in copyofcenters:
    if len(acenter.buddies)==0:
        continue
    elif len(acenter.buddies)==minbuddynum:
        minorcolor=acenter.position
        minorcolornum=len(acenter.buddies)
    else:
        total_major_color[0][0]+=len(acenter.buddies)*acenter.position[0]
        total_major_color[0][1]+=len(acenter.buddies)*acenter.position[1]
        total_major_color[0][2]+=len(acenter.buddies)*acenter.position[2]
        total_major_color[1]+=len(acenter.buddies)
majorcolor=[total_major_color[0][0]/total_major_color[1],total_major_color[0][1]/total_major_color[1],total_major_color[0][2]/total_major_color[1]]

minorcolor=rgb2hsv(minorcolor)
majorcolor=rgb2hsv(majorcolor)
#print(minorcolor,majorcolor)
minorcolornum=minorcolornum
majorcolornum=total_major_color[1]

degree_of_180=(180-abs(abs(minorcolor[0]-majorcolor[0])-180))/180*100
degree_of_85percent=(1-abs(minorcolornum/majorcolornum-0.15))*100

print('opposite-color-principle score:',degree_of_180)
print('color percentage score:        ',degree_of_85percent)

back1 = canvas.create_rectangle(0, 60, 500, 90, width=0, fill="white")
degree=canvas.create_rectangle(0, 60, degree_of_180*5, 90, width=0, fill="green")

back2 = canvas.create_rectangle(0, 95, 500, 125, width=0, fill="white")
degree2=canvas.create_rectangle(0, 95, degree_of_85percent*5, 125, width=0, fill="green")


tk.mainloop()
