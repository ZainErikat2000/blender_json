
from pickle import FALSE
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
###weekday text properties
weekday_text_loc_y = 1.38496
weekday_text_scale = [0.835,0.835,0.835]
###night text properties
night_text_loc = [-1.11195,-1.19667,0.0]
night_text_scale = [0.637,0.637,0.637]
###objects arrays
weekdays_texts = []
day_texts = []
night_texts = []
circles_outer_day = []
circles_inner_day = []
circles_outer_night = []
circles_inner_night = []

###import outer day circles
bpy.ops.wm.obj_import(filepath=path+'/weekday_objs/circle_outer_day.obj')
circle_outer_day_main = bpy.context.object
circles_outer_day.append(circle_outer_day_main)
###import inner day circles
bpy.ops.wm.obj_import(filepath=path+'/weekday_objs/circle_inner_day.obj')
circle_inner_day_main = bpy.context.object
circles_inner_day.append(circle_inner_day_main)
###import outer night circles
bpy.ops.wm.obj_import(filepath=path+'/weekday_objs/circle_outer_night.obj')
circle_outer_night_main = bpy.context.object
circles_outer_night.append(circle_outer_night_main)
###import inner night circles
bpy.ops.wm.obj_import(filepath=path+'/weekday_objs/circle_inner_night.obj')
circle_inner_night_main = bpy.context.object
circles_inner_night.append(circle_inner_night_main)
###create the texts
bpy.ops.object.text_add()
weekday_text = bpy.context.object
weekday_text.data.body = 'WEEKDAY'
weekday_text.data.align_x = 'CENTER'
weekday_text.name = 'weekday_text'
weekdays_texts.append(weekday_text)
###create day text
bpy.ops.object.text_add()
day_text = bpy.context.object
day_text.data.align_x = 'CENTER'
day_text.data.align_y = 'CENTER'
day_text.data.body = '88'
day_text.name = 'day_text'
bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
day_texts.append(day_text)
###create night text
bpy.ops.object.text_add()
night_text = bpy.context.object
night_text.data.body = '88'
night_text.data.align_x = 'CENTER'
night_text.data.align_y = 'CENTER'
night_text.name = 'night_text'
bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
night_texts.append(night_text)

###mian loc prep
circle_outer_day_main.location = circle_locations[0]
circle_inner_day_main.location = circle_locations[0]
circle_outer_night_main.location = circle_locations[0]
circle_inner_night_main.location = circle_locations[0]
day_text.location = circle_locations[0]

weekday_text.location = circle_locations[0]
weekday_text.location[1] += weekday_text_loc_y
weekday_text.scale = weekday_text_scale
night_text.location = circle_locations[0]
night_text.location[0] += night_text_loc[0]
night_text.location[1] += night_text_loc[1]
night_text.scale = night_text_scale

###############
#DUPING BEGINS#
###############

###WEEKDAYS

bpy.context.object.select_set(False)

objectToSelect = bpy.data.objects[weekday_text.name]
objectToSelect.select_set(True)    
bpy.context.view_layer.objects.active = objectToSelect

###weekday texts
for i in range(6):
    bpy.ops.object.duplicate()
    swt = bpy.context.object
    weekdays_texts.append(swt)
    swt.location = circle_locations[i+1]
    swt.location[1] += weekday_text_loc_y
    
###MAIN DAY CIRCLES

bpy.context.object.select_set(False)

objectToSelect = bpy.data.objects[circle_outer_day_main.name]
objectToSelect.select_set(True)    
bpy.context.view_layer.objects.active = objectToSelect

for i in range(6):
    bpy.ops.object.duplicate()
    smnc = bpy.context.object
    circles_outer_day.append(smnc)
    smnc.location = circle_locations[i+1]

###SECONDARY DAY CIRCLES

bpy.context.object.select_set(False)

objectToSelect = bpy.data.objects[circle_inner_day_main.name]
objectToSelect.select_set(True)    
bpy.context.view_layer.objects.active = objectToSelect

for i in range(6):
    bpy.ops.object.duplicate()
    ssdc = bpy.context.object
    circles_inner_day.append(ssdc)
    ssdc.location = circle_locations[i+1]

####MAIN NIGHT CIRCLES

bpy.context.object.select_set(False)

objectToSelect = bpy.data.objects[circle_outer_night_main.name]
objectToSelect.select_set(True)    
bpy.context.view_layer.objects.active = objectToSelect

for i in range(6):
    bpy.ops.object.duplicate()
    smnc = bpy.context.object
    circles_outer_night.append(smnc)
    smnc.location = circle_locations[i+1]

####SECONDARY DAY CIRCLES

bpy.context.object.select_set(False)

objectToSelect = bpy.data.objects[circle_inner_night_main.name]
objectToSelect.select_set(True)    
bpy.context.view_layer.objects.active = objectToSelect

for i in range(6):
    bpy.ops.object.duplicate()
    ssnc = bpy.context.object
    circles_inner_night.append(ssnc)
    ssnc.location = circle_locations[i+1]
    
####DAY TEXT CIRCLES

bpy.context.object.select_set(False)

objectToSelect = bpy.data.objects[day_text.name]
objectToSelect.select_set(True)    
bpy.context.view_layer.objects.active = objectToSelect

for i in range(6):
    bpy.ops.object.duplicate()
    dt = bpy.context.object
    bpy.ops.object.origin_set = 'ORIGIN_GEOMETRY'
    day_texts.append(dt)
    dt.location = circle_locations[i+1]
    
####NIGHT TEXT CIRCLES

bpy.context.object.select_set(False)

objectToSelect = bpy.data.objects[night_text.name]
objectToSelect.select_set(True)    
bpy.context.view_layer.objects.active = objectToSelect

for i in range(6):
    bpy.ops.object.duplicate()
    nt = bpy.context.object
    bpy.ops.object.origin_set = 'ORIGIN_GEOMETRY'
    night_texts.append(nt)
    nt.location = circle_locations[i+1]
    nt.location[0] += night_text_loc[0]
    nt.location[1] += night_text_loc[1]
    
for i in range(7):
    weekdays_texts[i].data.body = weekdays[i]
    
for i in range(7):
    day_texts[i].data.body = str(allDays[i])
    
for i in range(7):
    night_texts[i].data.body = str(allNights[i])
    
  #################
 ###################
#####################
#MATERIAL_MANAGEMENT#
#####################
 ###################
  #################
  
  ###################
 #####################
#######################
#BACKGROUND_MANAGEMENT#
#######################
 #####################
  ###################