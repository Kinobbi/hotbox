#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Rnadom Hue
#
#----------------------------------------------------------------------------------------------------------

import nukescripts
import colorsys
import random

backdrops = nuke.selectedNodes('BackdropNode')

for i, item in enumerate(backdrops):


    # convert TileColor to HSV
    originalTileColor = item.knob('tile_color').value()
    originalRGB = [(0xFF & originalTileColor >>  i) / 255.0 for i in [24,16,8]]
    originalHSV = colorsys.rgb_to_hsv(originalRGB[0],originalRGB[1],originalRGB[2])

    # modify HSV
    hue = random.uniform(0, 5)
    saturation = originalHSV[1]
    value = originalHSV[2]

    # convert HSnV to TileColor
    newHSV =  [hue,saturation,value]
    newRGB = colorsys.hsv_to_rgb(newHSV[0],newHSV[1],newHSV[2])
    newTileColor = int('%02x%02x%02x%02x' % (int(newRGB[0]*255),int(newRGB[1]*100*255/100),int(newRGB[2]*100*255/100),255),16)

    # set new Tile Color
    item.knob('tile_color').setValue(newTileColor)
