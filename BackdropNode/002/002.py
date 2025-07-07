#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Z order +
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    x = i.knob('z_order').value()
    i.knob('z_order').setValue(x+1)
