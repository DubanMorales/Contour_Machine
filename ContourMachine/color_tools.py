import rhinoscriptsyntax as rs
import Rhino
import imp
from math import radians
from math import sin
from math import cos




def pixel_color_name(r, g, b):
    """This funcion breaks the HSL colorwheel into 6 segments
    and returns a name for each."""
    #convert an rgb value to and h, l, s value. 
    h, s, v = rgb_to_hsv(r, g, b)
    h_degrees = h

    #specifiy the color breaks
    if 330 <= h_degrees or h_degrees<= 30:
        return "red"
    if 30 <= h_degrees <= 90:
        return "yellow"
    if 90 <= h_degrees <= 150:
        return "green"
    if 150 <= h_degrees <= 210:
        return "cyan"
    if 210 <= h_degrees <= 270:
        return "magenta"
    if 270 <= h_degrees <= 330:
        return "blue"
    if h_degrees >= 360:
        return "red"



def rgb_to_hsv(r, g, b):
    #source https://www.w3resource.com/python-exercises/math/python-math-exercise-77.php
    r, g, b = r/255.0, g/255.0, b/255.0
    max_val = max(r, g, b)
    min_val = min(r, g, b)
    
    diff = max_val - min_val
    
    if max_val == min_val:
        h = 0
    elif max_val == r:
        h = (60 * ((g-b)/diff) + 360)%360
    elif max_val == g:
        h = (60 * ((b-r)/diff) + 120)%360
    elif max_val == b:
        h = (60 * ((r-g)/diff) + 240)%360
    if max_val == 0:
        s = 0
    else:
        s = (diff/max_val)*100
    v = max_val*100
    
    return h, s, v


def hsv_to_rgb(h, s, v):
    # https://stackoverflow.com/questions/24852345/hsv-to-rgb-color-conversion
    if s == 0.0: v*=255; return (v, v, v)
    i = int(h*6.)
    f = (h*6.)-i; p,q,t = int(255*(v*(1.-s))), int(255*(v*(1.-s*f))), int(255*(v*(1.-s*(1.-f)))); v*=255; i%=6
    v = int(v)
    t = int(t)
    p = int(p)
    q = int(q)
    if i == 0: return (v, t, p)
    if i == 1: return (q, v, p)
    if i == 2: return (p, v, t)
    if i == 3: return (p, q, v)
    if i == 4: return (t, p, v)
    if i == 5: return (v, p, q)



def color_height( r, g, b):
    name = pixel_color_name(r, g, b)

    if name == "red":
        return .5
    if name == "yellow":
        return .6
    if name == "green":
        return .7
    if name == "cyan":
        return .8
    if name == "magneta":
        return .9
    if name == "blue":
        return 1.0
        
        
def radial_transform_pixel(r,g,b):
    h,s,v = rgb_to_hsv(r,g,b)
    rad_angle = radians(h)

    x = cos(rad_angle)*(s)
    y = sin(rad_angle)*(s)
    z = v

    return x,y,z