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

bpy.context.scene.cursor.location = (0.0, 0.0, 0.0)


###get the dates' weekdays in order
###get the basic temps
weekdays = []
allDays = []
allNights = []
for x in jsonRes:
    dayTemp = jsonRes[x]['times']['all_day']['temperature']['value']
    nightTemp = jsonRes[x]['times']['all_night']['temperature']['value']
    allDays.append(dayTemp)
    allNights.append(nightTemp)
    x = x.split('-')
    year = int(x[0])
    month = int(x[1])
    day = int(x[2])
    wd = datetime.date(year,month,day)
    weekdays.append(wd.strftime("%A"))

for i in range(7):
    print(allDays[i])
    print(allNights[i])
###create, set the body and store the text objects
textObjs = []    
for i in range(7):
    bpy.ops.object.text_add()
    bpy.ops.transform.resize(value=(0.8,0.8,0.8))
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
camera.rotation_euler[0] = radians(0)
camera.location[2] = 30

###fixed locations for the circles
circle_locations = [[0,8,0],
[-3,4.5,0],
[3,4.5,0],
[-3,0,0],
[3,0,0],
[-3,-4.5,0],
[3,-4.5,0]]

circles = []
###import the circle object
bpy.ops.wm.obj_import(filepath=path+'/objs/test_proj.obj')
###store the circle object
circle = bpy.context.object
###set the origin to the geometry
bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
###set a default position (due to me forgeting to set the origin and location before the export)
circle.location = [0,0,0]
###append into array
circles.append(circle)

for i in range(6):
    bpy.ops.object.duplicate(linked=False)
    new_circle = bpy.context.object
    circles.append(new_circle)
    
for i in range(7):
    circles[i].location = circle_locations[i]
    
for i in range(int(7)):
    plh = circle_locations
    plh[i][1] += 1.3
    textObjs[i].location = plh[i]
###create and do the same thing to the other circles