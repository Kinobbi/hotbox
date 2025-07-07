#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Make Desat Rainbow
#
#----------------------------------------------------------------------------------------------------------

import nukescripts
import colorsys

backdrops = nuke.allNodes('BackdropNode')

for i, item in enumerate(backdrops):

#    item['note_font_size'].setValue(30)
    item['note_font_color'].setValue(100)
    item['note_font'].setValue('Verdana Bold')

    rainbow = (float(i) * (1 / float(len(backdrops))))
    # convert TileColor to HSV
    originalTileColor = item.knob('tile_color').value()
    originalRGB = [(0xFF & originalTileColor >>  i) / 255.0 for i in [24,16,8]]
    originalHSV = colorsys.rgb_to_hsv(originalRGB[0],originalRGB[1],originalRGB[2])

    # modify HSV
    hue = rainbow
    saturation = 0.3
    value = 0.2

    # convert HSV to TileColor
    newHSV =  [hue,saturation,value]
    newRGB = colorsys.hsv_to_rgb(newHSV[0],newHSV[1],newHSV[2])
    newTileColor = int('%02x%02x%02x%02x' % (int(newRGB[0]*100*255/100),int(newRGB[1]*100*255/100),int(newRGB[2]*100*255/100),255),16)

    # set new Tile Color
    item.knob('tile_color').setValue(newTileColor)

pyscript_text = '''import nukescripts
import colorsys
import random     
def newDesatRainbowBackdrop():    
    r = nuke.root()
    pausebutton = r.knob('noDesatRainbow')
    pause = pausebutton.getValue()
    if pause == 0:
        item = nuke.thisNode()
        item['note_font_color'].setValue(100)
        item['note_font'].setValue('Verdana Bold')
        
        rainbow = random.uniform(0,1)
        # convert TileColor to HSV
        originalTileColor = item.knob('tile_color').value()
        originalRGB = [(0xFF & originalTileColor >>  i) / 255.0 for i in [24,16,8]]
        originalHSV = colorsys.rgb_to_hsv(originalRGB[0],originalRGB[1],originalRGB[2])
        
        # modify HSV
        hue = rainbow
        saturation = 0.3
        value = 0.2
        
        # convert HSV to TileColor
        newHSV =  [hue,saturation,value]
        newRGB = colorsys.hsv_to_rgb(newHSV[0],newHSV[1],newHSV[2])
        newTileColor = int('%02x%02x%02x%02x' % (int(newRGB[0]*100*255/100),int(newRGB[1]*100*255/100),int(newRGB[2]*100*255/100),255),16)
        
        # set new Tile Color
        item.knob('tile_color').setValue(newTileColor)
    else:
        return
nuke.addOnUserCreate(newDesatRainbowBackdrop, nodeClass="BackdropNode")
'''

r = nuke.root()
if r.knob("DesatRainbowTab") == None:
    tab = nuke.Tab_Knob("DesatRainbowTab","Desat Rainbow")
    pybutton = nuke.PyScript_Knob("DesatRainbow","Desat Rainbow onScriptLoad",pyscript_text)
    Pause = nuke.Boolean_Knob("noDesatRainbow","pause Desat Rainbow",False)
    Pause.setFlag(nuke.STARTLINE)
    
    r.addKnob(tab)
    r.addKnob(pybutton)
    r.addKnob(Pause)

r.knob('onScriptLoad').setValue("nuke.root().knob('DesatRainbow').execute()")
nuke.root().knob('DesatRainbow').execute()