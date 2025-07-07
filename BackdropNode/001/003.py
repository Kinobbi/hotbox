#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Size +
#
#----------------------------------------------------------------------------------------------------------

nodes = nuke.selectedNodes()

for i in nodes:
    w = i.knob('bdwidth').value()
    h = i.knob('bdheight').value()
    i.knob('bdwidth').setValue(w+50)
    i.knob('bdheight').setValue(h+50)

    position = [i.xpos(),i.ypos()]
    i.setXpos(position[0]-25)
    i.setYpos(position[1]-25)


