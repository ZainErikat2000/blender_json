
import bpy
import json
import requests
import datetime
from datetime import date
import os.path
from os.path import exists
from os.path import dirname
from math import radians

###set up the scene by deleting all objects
###check if youre in edit mode
if bpy.context.object != None:
    if bpy.context.object.mode == 'EDIT':
        bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.select_all(action='SELECT')
###delte all objects in the scene
bpy.ops.object.delete()
bpy.context.scene.cursor.location = (0.0, 0.0, 0.0)

###get the parent directory path
path = dirname(dirname(__file__))

###filename = the date in YYY-MM-DD format
filename = date.today().strftime('%Y_%d_%m') + '.json'

###make sure an empty "api_outputs" folder is in the parent directory path
###creates the full path to the http request file
fullPath = path+'/api_outputs/'+filename

###check if the has already been made
###if this is true it will skip the request part
jsonExists = exists(fullPath)

if(not jsonExists):
    r = requests.get('https://api.wasm.live')
    with open(path+'/api_outputs/'+filename,'w') as file:
        file.write(r.text)
else:
    print('latest data already exists')

###open the json file and store the values in jsonRes
with open(fullPath,'r') as file:
    jsonRes = json.load(file)

###get the dates' weekdays in order
###get the basic temps
weekdays = []
allDays = []
allNights = []
mat_names = []
for x in jsonRes:
    dayTemp = jsonRes[x]['times']['all_day']['temperature']['value']
    nightTemp = jsonRes[x]['times']['all_night']['temperature']['value']
    mats = [jsonRes[x]['times']['all_day']['color']['value'],
    jsonRes[x]['times']['all_night']['color']['value']]
    mat_names.append(mats)
    allDays.append(dayTemp)
    allNights.append(nightTemp)
    x = x.split('-')
    year = int(x[0])
    month = int(x[1])
    day = int(x[2])
    wd = datetime.date(year,month,day)
    weekdays.append(wd.strftime("%A"))

###create, set the body and store the text objects
textObjs = []    
for i in range(7):
    bpy.ops.object.text_add()
    bpy.ops.transform.resize(value=(0.65,0.65,0.65))
    textObj = bpy.context.object
    textObj.data.body = weekdays[i]
    textObj.data.align_x = 'CENTER'
    textObjs.append(textObj)

###set the render resolution
bpy.data.scenes['Scene'].render.resolution_x = 1080
bpy.data.scenes['Scene'].render.resolution_y = 1920

###create, store, rotate and place the camera
bpy.ops.object.camera_add()
camera = bpy.context.scene.objects['Camera']
#camera.data.type = 'ORTHO'
camera.data.ortho_scale = 23.7
camera.rotation_euler[0] = radians(0)
camera.location[2] = 32

###fixed locations for the circles
circle_locations = [[0,9,0],
[-3,4.5,0],
[3,4.5,0],
[-3,0,0],
[3,0,0],
[-3,-4.5,0],
[3,-4.5,0]]
###nights locations
nights_loc = [-1.18,-1.23]
night_inner_loc = [1.14734,1.1756]
night_inner_scale = (0.602,0.602,0.602)

##############
#MAIN CIRCLES#
##############

circles = []
###import the circle object
bpy.ops.wm.obj_import(filepath=path+'/objs/Night_Day_Circle.obj')
###store the circle object
circle = bpy.context.object

###set a default position (due to me forgeting to set the origin and location before the export)
circle.location = [0,0,0]
###append into array
circles.append(circle)

for i in range(6):
    bpy.ops.object.duplicate(linked=False)
    new_circle = bpy.context.object
    circles.append(new_circle)

###############
#INNER CIRCLES#
###############

inner_circles = []
###import the circle object
bpy.ops.wm.obj_import(filepath=path+'/objs/Night_Day_Circle_Inner.obj')
###store the circle object
inner_circle = bpy.context.object

###set a default position (due to me forgeting to set the origin and location before the export)
inner_circle.location = [0,0,0]
###append into array
inner_circles.append(inner_circle)

for i in range(6):
    bpy.ops.object.duplicate(linked=False)
    new_circle = bpy.context.object
    inner_circles.append(new_circle)

#####################
#INNER NIGHT CIRCLES#
#####################

inner_circles_night = []
###import the circle object
bpy.ops.wm.obj_import(filepath=path+'/objs/Night_Day_Circle_Inner.obj')
###store the circle object
inner_circle_night = bpy.context.object

###set a default position (due to me forgeting to set the origin and location before the export)
inner_circle_night.location = [0,0,0]
###append into array
inner_circles_night.append(inner_circle_night)

for i in range(6):
    bpy.ops.object.duplicate(linked=False)
    new_circle = bpy.context.object
    inner_circles_night.append(new_circle)


###place circles and append material to them (NOTE NO MAT SLOTS IS PREFERED)
for i in range(7):
    ###MAIN CIRCLES
    material = bpy.data.materials.get('Circle_Mat')
    circles[i].location = circle_locations[i]
    circles[i].data.materials.append(material)
    ###MAIN INNER CIRCLES
    inner_circles[i].location = circle_locations[i]
    inner_circles[i].location[2] -= 0.01
    ###NIGHT INNER CIRCLES
    inner_circles_night[i].location = circle_locations[i]
    inner_circles_night[i].scale = night_inner_scale
    inner_circles_night[i].location[0] -= night_inner_loc[0]
    inner_circles_night[i].location[1] -= night_inner_loc[1]
    inner_circles_night[i].location[2] -= 0.1
        
for i in range(int(7)):
    textObjs[i].location = circle_locations[i]
    textObjs[i].location[1] += 1.3
###create and do the same thing to the other circles

for i in range(7):
    bpy.ops.object.text_add()
    tempObj = bpy.context.object
    tempObj.data.body = str(allDays[i])
    tempObj.data.align_x = 'CENTER'
    tempObj.data.align_y = 'CENTER'
    tempObj.location = circle_locations[i]
    
for i in range(7):
    bpy.ops.object.text_add()
    tempObj = bpy.context.object
    tempObj.data.body = str(allNights[i])
    tempObj.data.align_x = 'CENTER'
    tempObj.data.align_y = 'CENTER'
    tempObj.location = circle_locations[i]
    tempObj.location[0] += nights_loc[0]
    tempObj.location[1] += nights_loc[1]
    tempObj.scale = [0.8,0.8,0.8]
    
bpy.ops.object.light_add(type='SUN')