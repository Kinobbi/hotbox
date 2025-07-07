#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Appearance
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    i.knob('appearance').setValue(1-int(i.knob('appearance').getValue()))
