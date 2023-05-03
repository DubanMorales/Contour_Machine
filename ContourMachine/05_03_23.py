import rhinoscriptsyntax as rs
import scriptcontext as sc
import Rhino
import math
import color_tools as ct
import viewport_tools as vt

from math import radians
from math import sin
from math import cos
from imp import reload
from math import pi as pi
import time

reload(vt)
reload(ct)

rs.MessageBox("This program transforms color values from a RGB cubic grid into 3d points from the points into a series of diffrent mathematical equations to map out the virtual experience")

def save_low_res():
    time_stamp = time.localtime()
    vt.create_parallel_view("test", (1000,1000))
    vt.set_viewports_mode()
    vt.capture_view(1.0, "Test"+ str(time_stamp), "Captures")


def assign_material_color(object, color):
    rs.AddMaterialToObject(object)
    index = rs.ObjectMaterialIndex(object)
    rs.MaterialColor(index, color)

def remap(value, source_min, source_max, target_min, target_max):
   source = float(source_max - source_min)
   target = float(target_max - target_min)
   value_less = float(value - source_min)
   new_value = float(target *value_less/source) + target_min
   return new_value

def clamp(value, floor, ceiling):
    if value < floor:
        return floor
    if value > ceiling:
        return ceiling
    else:
        return value

def point_to_rgb(point, min, max):
    x, y, z = point 
    r = clamp(remap(x, min, max, 0, 255), 0, 255)
    g = clamp(remap(y, min, max, 0, 255), 0, 255)
    b = clamp(remap(z, min, max, 0, 255), 0, 255)
    factor = ct.color_height(r,g,b)
    
    return r, g, b
    return factor

def grid(x_num, y_num, z_num, space):
    point_list =[]
    for i in range(0,x_num, space):
        for j in range(0,y_num, space):
            for p in range(0,z_num, space):
                x = i 
                y = j
                z = p
                point = (x,y,z)
                point_list.append(point)
    return point_list
    
def center_cube(center, radius):
    cx, cy, cz = center 
    
    p1 = (cx - radius, cy - radius, cz - radius)
    p2 = (cx + radius, cy - radius, cz - radius)
    p3 = (cx + radius, cy + radius, cz - radius)
    p4 = (cx - radius, cy + radius, cz - radius)
    #upper points
    p5 = (cx - radius, cy - radius, cz + radius)
    p6 = (cx + radius, cy - radius, cz + radius)
    p7 = (cx + radius, cy + radius, cz + radius)
    p8 = (cx - radius, cy + radius, cz + radius)
    
    points = [p1, p2, p3, p4, p5,p6, p7, p8]
    
    cube = rs.AddBox(points)
    return (cube)
    
def box_contour_sqr(point,length, width, height,steps,user_x, user_y, func):
    x, y, z = point
    value_x = user_x
    value_y = user_y
    trig_func = func
    for i in rs.frange(0,height, height/steps):
    
        color = point_to_rgb((x, y, z), 0, height)
        
        h, s, v = ct.rgb_to_hsv(color[0], color[1], color[2])
        
        x_factor,y_factor,z2 = ct.radial_transform_pixel(h,s,v)
        
        x_factor = s/value_x*color[0]
        y_factor = v/value_y*s
        z2 = h*s
        
        if trig_func == "sin":
            rect = rs.AddRectangle((math.pi*90300*cos(x*x_factor*i),math.pi*90300*sin(y*y_factor*i),(z2*i/2)), 0.1+v*90*2, 0.1+s*90*2)
            #nature example(1+x*(1+v*99)), (1+s*(99+y*2))), OG 0.1+v*90*2, 0.1+s*90*2)
        else:
            pass
        if trig_func == "atan2":
            rect = rs.AddRectangle((math.pi*90300*math.cos(x*x_factor*i),math.pi*90300*math.atan2(x*x_factor*i, y*y_factor*i),(z2*i/2)), 0.1+v*90*2, 0.1+s*90*2)
        else:
            pass
        if trig_func == "cos":
            rect = rs.AddRectangle((math.pi*90300*math.cos(x*x_factor*i),math.pi*90300*math.cos(y*y_factor*i),(z2*i/2)), 0.1+v*90*2, 0.1+s*90*2)
        else:
            pass
            
            
        rs.ObjectColor(rect, color)
        rect_srf= rs.AddPlanarSrf(rect)
        centroid = rs.CurveAreaCentroid(rect)[0]
        if getattr(centroid, 'z', None) in [15, 30, 93]:
            continue #skip this iteration
        if isinstance(centroid, Rhino.Geometry.Point3d):
            if centroid.Z % 15 == 0:
                rs.RotateObject(rect_srf, centroid, 90, [0,0,1])

            else:
                pass
            if centroid.Z % 20 == 0:
                rs.RotateObject(rect_srf, centroid, 90, [0,0,1])
                rs.ScaleObject(rect_srf, centroid,([1.2,1.2,1.2]))
            else:
                pass
            if centroid.Z % 93 == 0:
                rs.RotateObject(rect_srf, centroid, 90, [1,0,0])

            else:
                pass
        assign_material_color(rect_srf,color)

def box_contour(point,length, width, height,steps,user_x, user_y, func):
    x, y, z = point
    value_x = user_x
    value_y = user_y
    trig_func = func
    for i in rs.frange(0,height, height/steps):
    
        color = point_to_rgb((x, y, z), 0, height)
        
        h, s, v = ct.rgb_to_hsv(color[0], color[1], color[2])
        
        x_factor,y_factor,z2 = ct.radial_transform_pixel(h,s,v)
        
        x_factor = s/value_x*color[0]
        y_factor = v/value_y*s
        z2 = h*s
        
        if trig_func == "sin":
            rect = rs.AddRectangle((math.pi*90300*cos(x*x_factor*i),math.pi*90300*sin(y*y_factor*i),(z2*i/2)), (1+x*(1+v*99)), (1+s*(99+y*2)))
            #nature example(1+x*(1+v*99)), (1+s*(99+y*2))), OG 0.1+v*90*2, 0.1+s*90*2)
        else:
            pass
        if trig_func == "atan2":
            rect = rs.AddRectangle((math.pi*90300*math.cos(x*x_factor*i),math.pi*90300*math.atan2(x*x_factor*i, y*y_factor*i),(z2*i/2)),(1+x*(1+v*99)), (1+s*(99+y*2)))
        else:
            pass
        if trig_func == "cos":
            rect = rs.AddRectangle((math.pi*90300*math.cos(x*x_factor*i),math.pi*90300*math.cos(y*y_factor*i),(z2*i/2)),(1+x*(1+v*99)), (1+s*(99+y*2)))
            pass
            
            
        rs.ObjectColor(rect, color)
        rect_srf= rs.AddPlanarSrf(rect)
        centroid = rs.CurveAreaCentroid(rect)[0]
        if getattr(centroid, 'z', None) in [10, 26, 100]:
            continue #skip this iteration
        if isinstance(centroid, Rhino.Geometry.Point3d):
            if centroid.Z % 10 == 0:
                rs.RotateObject(rect_srf, centroid, 90, [0,0,1])
            else:
                pass
            if centroid.Z % 26 == 0:
                rs.RotateObject(rect_srf, centroid, 90, [0,0,1])
                rs.ScaleObject(rect_srf, centroid, [1.2,1.2,1.2])
            else:
                pass
            if centroid.Z % 100 == 0:
                rs.RotateObject(rect_srf, centroid, 90, [1,0,0])
            else:
                pass
        assign_material_color(rect_srf,color)



def box_contour_circle_srf(point,length, width, height,steps,user_x, user_y, func):
    x, y, z = point
    value_x = user_x
    value_y = user_y
    trig_func = func
    
    for i in rs.frange(0,height, height/steps):
    
        color = point_to_rgb((x, y, z), 0, height)
        
        h, s, v = ct.rgb_to_hsv(color[0], color[1], color[2])
        
        x_factor,y_factor,z2 = ct.radial_transform_pixel(h,s,v)
        
        x_factor = s/value_x*color[0]
        y_factor = v/value_y*s
        z2 = h*s
        
        if trig_func == "atan2":
            circ = rs.AddCircle((math.pi*90000*math.cos(x*x_factor*i),math.pi*99999*math.atan2(x*x_factor*i, y*y_factor*i),(z2*i/2)), 0.1+v*98)
        else:
            pass
        if trig_func == "sin":
            circ = rs.AddCircle((math.pi*90000*math.cos(x*x_factor*i),math.pi*90000*math.sin(y*y_factor*i),(z2*i/2)), 0.1+v*98)
        else:
            pass
        if trig_func == "cos":
            circ = rs.AddCircle((math.pi*90000*math.cos(x*x_factor*i), math.pi*90000*math.cos(y*y_factor*i),(z2*i/2)),  0.1+s*98)
        else:
            pass

        rs.ObjectColor(circ, color)
        CircSrf = rs.AddPlanarSrf(circ)
        assign_material_color(CircSrf,color)
        centroidCirc = rs.CurveAreaCentroid(circ)[0]

        if getattr(centroidCirc, 'z', None) in [10, 12]:
            continue #skip this iteration
        if isinstance(centroidCirc, Rhino.Geometry.Point3d):
            if centroidCirc.Z % 10 == 0:
                rs.RotateObject(CircSrf, centroidCirc, 90, [1,0,0])
                rs.ScaleObject(CircSrf, centroidCirc, ([1.2,2,1.2]))
            else:
                pass

            if centroidCirc.Z % 12 == 0:
                rs.RotateObject(CircSrf, centroidCirc, 90, [1,0,0])
            else:
                pass


def box_contours_boxes_color(point,length, width, height,steps,user_x, user_y, func):
    x, y, z = point
    value_x = user_x
    value_y = user_y
    box_list = []
    trig_func = func

    for i in rs.frange(0,height, height/steps):

        color = point_to_rgb((x, y, z), 0, height)

        h, s, v = ct.rgb_to_hsv(color[0], color[1], color[2])

        x_factor,y_factor,z2 = ct.radial_transform_pixel(h,s,v)

        x_factor = s/value_x*color[0]
        y_factor = v/value_y*s
        z2 = h*s
        
        if trig_func == "sin":
            boxes1 = center_cube((math.pi*90000*cos(x*x_factor*i),math.pi*90000*sin(y*y_factor*i),(z2*i/2)),0.1+v*95 )
        else:
            pass
        if trig_func == "cos":
        
            boxes1 = center_cube((math.pi*90000*cos(x*x_factor*i),math.pi*90000*cos(y*y_factor*i),(z2*i/2)),0.1+v*95 )
        else:
            pass
        if trig_func == "atan2":
            boxes1 = center_cube((math.pi*90000*cos(x*x_factor*i),math.pi*math.atan2(x*x_factor*i, y*y_factor*i),(z2*i/2)), 0.1+v*95)
        else:
            pass
        assign_material_color(boxes1, color)
        
def option_1():
    points = grid(20, 20, 15,1)
    value = rs.GetString("select a geometric value that is going to create the space", "circle", ["circle", "rectangle", "boxes", "square" ])

    if value == "rectangle":
        user_input_1 = rs.RealBox("Please provide an x_value that will determine your starting position in the color model. 1 min - 360 max.  ", 1.0, 'value_x', 1.0, 360.0)
        user_input_2 = rs.RealBox("Please provide an y_value that will determine your starting position in the color model. 1 min - 360 max.", 1.0, 'value_y', 1.0, 360.0)
        
        user_input_3 = rs.GetString("select a geometric function that will transform the spacing", "sin", ["sin", "atan2","cos"])
        for i in points:
            rect = box_contour(i, 15, 15, 15, 1, user_input_1, user_input_2,user_input_3)

    else:
        pass

    if value == "circle":
        user_input_1 = rs.RealBox("Please provide an x_value that will determine your starting position in the color model. 1 min - 360 max.  ", 1.0, 'value_x', 1.0, 360.0)
        user_input_2 = rs.RealBox("Please provide an y_value that will determine your starting position in the color model. 1 min - 360 max.", 1.0, 'value_y', 1.0, 360.0)
        user_input_3 = rs.GetString("select a geometric function that will transform the spacing", "sin", ["sin", "atan2", "cos"])
        for i in points:
            circ = box_contour_circle_srf(i, 15, 15, 15, 1, user_input_1, user_input_2, user_input_3)
    else:
        pass
        
    if value == "square":
        user_input_1 = rs.RealBox("Please provide an x_value that will determine your starting position in the color model. 1 min - 360 max.  ", 1.0, 'value_x', 1.0, 360.0)
        user_input_2 = rs.RealBox("Please provide an y_value that will determine your starting position in the color model. 1 min - 360 max.", 1.0, 'value_y', 1.0, 360.0)
        user_input_3 = rs.GetString("select a geometric function that will transform the spacing", "sin", ["sin", "atan2", "cos"])
        for i in points:
            rect = box_contour_sqr(i, 15, 15, 15, 1, user_input_1, user_input_2,user_input_3)
    else:
        pass
        
    if value == "boxes":
        user_input_1 = rs.RealBox("Please provide an x_value that will determine your starting position in the color model. 1 min - 360 max.  ", 1.0, 'value_x', 1.0, 360.0)
        user_input_2 = rs.RealBox("Please provide an y_value that will determine your starting position in the color model. 1 min - 360 max.", 1.0, 'value_y', 1.0, 360.0)
        user_input_3 = rs.GetString("select a geometric function that will transform the spacing", "sin", ["sin", "atan2", "cos"])
        for i in points:
            rect = box_contours_boxes_color(i, 15, 15, 15, 1, user_input_1, user_input_2,user_input_3)
        
def option_2():
    test = rs.GetString("Run again?" , "No", ["yes","no"])
    if test == "yes" :
        option_1()
    else:
        pass

def main():
    rs.EnableRedraw(False)
    option_1()
    option_2()
    option_2()
    
    
    save_low_res()
    rs.EnableRedraw(True)
        
    view_name = "axo_cube_2"
    time_stamp = time.localtime()
    vt.create_parallel_view(view_name, (1000, 1000))
    vt.set_axon_view(-140, 60, view_name)
    rs.ZoomExtents()
    vt.zoom_scale(1)
    vt.set_display_mode(view_name, "Rendered")
    vt.capture_view(1.0, "axo_cube_2"+ str(time_stamp), "Captures")


main()
