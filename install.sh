#!/bin/sh

dir=$(dirname $0)

addon=~/.config/blender/3.2/scripts/addons/asset_libraries/

rm -r $addon
mkdir $addon
cp -r $dir/* $addon

~/.steam/steam/steamapps/common/Blender/blender
clear
