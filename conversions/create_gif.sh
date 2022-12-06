#!/bin/bash

### add overlay (forecast) to video

ffmpeg -i ../video/vid.mkv -i ../renders/output.png -filter_complex "[0:v][1:v]overlay" -vcodec libx264 overlayed.mp4 -y;

### convert to 720x1280

ffmpeg -i overlayed.mp4 -ss 00:00:00.000 -t 00:00:05.000 -vf "fps=30, scale=720:1280" -an sm_overlayed.mp4 -y;

### create palette for gif

ffmpeg -i sm_overlayed.mp4 -vf palettegen palette.png -y;

### create gif

ffmpeg -i sm_overlayed.mp4 -i palette.png -filter_complex "fps=30, scale=720:1280[x]; [x][1:v]paletteuse" forecast.gif -y;
