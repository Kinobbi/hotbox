#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Label
#
#----------------------------------------------------------------------------------------------------------

import nukescripts

myKnobPanel = nuke.Panel('Label')
myKnobPanel.addSingleLineInput('Label','')

#show the panel
panel = myKnobPanel.show()

if panel:
    text = myKnobPanel.value('Label')

    for i in nuke.selectedNodes():
        i.knob('label').setValue(text)
