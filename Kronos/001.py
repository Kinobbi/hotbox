#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Control Panel
#
#----------------------------------------------------------------------------------------------------------

'''Version 3.0 // Last updated: 22/05/2025'''
'''UPDATES: Debug bakevalues error.'''
'''BUGS: Channels knob doesn't bake into Kronos.'''


# Select and group nodes individually in loop
selection = nuke.selectedNodes()
[deselect.setSelected(False) for deselect in selection]


for each in selection:
    # Checking if there is an existing Ctrl Panel
    dup = bool([dup for dup in nuke.allNodes() if dup.name() == str(each.name()+'Ctrl')])
    if dup:
        nuke.message('There is already a control panel')
    else:
        # We will pick knobs from this node for knobChanged later
        nuke.createNode('NoOp')
        
        # Creating control panel
        ctrlPanel = nuke.collapseToGroup()
        ctrlPanel['name'].setValue(each.name()+'Ctrl')
        ctrlPanel['hide_input'].setValue(True)
        ctrlPanel.setXYpos(each.xpos()-150, each.ypos())

        # Obtaining Kronos knob values
        def valueType(label,type):
            if type == float:
                return float(each.knob(label).getValue())
            elif type == int:
                return int(each.knob(label).getValue())
            elif type == str:
                return str(each.knob(label).value())
            elif type == bool:
                return bool(each.knob(label).value())
        
        # Setting expression link and check if animated
        def linkKnobs(label,type):
            if each.knob(label).isAnimated() == False:
                ctrlPanel.knob(label).setValue(valueType(label,type))
                each.knob(label).setExpression(str(ctrlPanel.name()+'.'+label))
            elif each.knob(label).isAnimated() == True:
                ctrlPanel.knob(label).copyAnimation(0, each.knob(label).animation(0))
                each.knob(label).clearAnimated()
                each.knob(label).setExpression(str(ctrlPanel.name()+'.'+label))


        # Creating user knobs
        tab = nuke.Tab_Knob('Kronos', 'Kronos')
        ctrlPanel.addKnob(tab)

        name = nuke.Text_Knob('gpuName', 'Local GPU:')
        ctrlPanel.addKnob(name)
        linkKnobs('gpuName', str)

        GPU = nuke.Disable_Knob('useGPUIfAvailable', 'Use GPU if available')
        GPU.setDefaultValue([True])
        GPU.setFlag(nuke.STARTLINE)
        GPU.setFlag(nuke.ALWAYS_SAVE)
        ctrlPanel.addKnob(GPU)
        linkKnobs('useGPUIfAvailable', bool)

        line = nuke.Text_Knob('', '')
        ctrlPanel.addKnob(line)

        inputFirst = nuke.Int_Knob('input.first', 'Input Range')
        inputFirst.setDefaultValue([1])
        inputFirst.setFlag(nuke.ALWAYS_SAVE)
        ctrlPanel.addKnob(inputFirst)
        linkKnobs('input.first', int)

        inputLast = nuke.Int_Knob('input.last', '')
        inputLast.setDefaultValue([100])
        inputLast.clearFlag(nuke.STARTLINE)
        inputLast.setFlag(nuke.ALWAYS_SAVE)
        ctrlPanel.addKnob(inputLast)
        linkKnobs('input.last', int)

        resetFramerange = '''
    group = nuke.thisNode()

    group['input.first'].setValue(nuke.Root().firstFrame())
    group['input.last'].setValue(nuke.Root().lastFrame())
    '''

        reset = nuke.PyScript_Knob('resetInputRange', 'Reset', resetFramerange)
        ctrlPanel.addKnob(reset)

        channels = nuke.ChannelMask_Knob('')
        channels.setName('retimedChannels')
        channels.setLabel('Channels')
        channels.setFlag(0x00000001 | 0x00000002)
        channels.setFlag(nuke.ALWAYS_SAVE)
        ctrlPanel.addKnob(channels)
        linkKnobs('retimedChannels', str)


        # Creating custom knobs in internal Kronos node for knobChanged to work
        with ctrlPanel:
            [select.setSelected(True) for select in nuke.allNodes('NoOp')]
            for user in nuke.selectedNodes():
                method = nuke.Enumeration_Knob('interpolation', 'Method', ['Frame', 'Blend', 'Motion'])
                method.setDefaultValue([2])
                method.setValue(each['interpolation'].value())
                method.setFlag(nuke.ALWAYS_SAVE)
                user.addKnob(method)
                each.knob('interpolation').setExpression(str(ctrlPanel.name()+'.'+user.name()+'.interpolation'))

                timing = nuke.Enumeration_Knob('timing2', 'Timing', ['Output Speed', 'Input Speed', 'Frame'])
                timing.setDefaultValue([0])
                timing.setValue(each['timing2'].value())
                timing.setFlag(nuke.ALWAYS_SAVE)
                user.addKnob(timing)
                each.knob('timing2').setExpression(str(ctrlPanel.name()+'.'+user.name()+'.timing2'))

                motion = nuke.Enumeration_Knob('motionEstimation', 'Motion', ['Regularized', 'Local'])
                motion.setDefaultValue([0])
                motion.setValue(each['motionEstimation'].value())
                motion.setFlag(nuke.ALWAYS_SAVE)
                user.addKnob(motion)
                each.knob('motionEstimation').setExpression(str(ctrlPanel.name()+'.'+user.name()+'.motionEstimation'))

                auto = nuke.Disable_Knob('autoShutterTime', 'Automatic Shutter Time')
                auto.setValue(each['autoShutterTime'].value())
                auto.setFlag(nuke.ALWAYS_SAVE)
                user.addKnob(auto)
                each.knob('autoShutterTime').setExpression(str(ctrlPanel.name()+'.'+user.name()+'.autoShutterTime'))

        def internalPicker(name,label):
            with ctrlPanel:
                [select.setSelected(True) for select in nuke.allNodes('NoOp')]
                for node in nuke.selectedNodes():
                    target = '{}.{}'.format(node.name(), name)
            link = nuke.Link_Knob(name, label)
            link.setLink(target)
            ctrlPanel.addKnob(link)

        internalPicker('interpolation', 'Method')
        internalPicker('timing2', 'Timing')


        # Creating Timing type knobs for knobChanged
        timingOutput = nuke.Double_Knob('timingOutputSpeed', 'Output Speed')
        timingOutput.setRange(0, 5)
        timingOutput.setDefaultValue([0.5])
        timingOutput.setFlag(nuke.ALWAYS_SAVE)
        ctrlPanel.addKnob(timingOutput)
        linkKnobs('timingOutputSpeed', float)

        timingInput = nuke.Double_Knob('timingInputSpeed', 'Input Speed')
        timingInput.setRange(0, 5)
        timingInput.setDefaultValue([0.5])
        timingInput.setFlag(nuke.ALWAYS_SAVE)
        ctrlPanel.addKnob(timingInput)
        linkKnobs('timingInputSpeed', float)

        timingFrame = nuke.Double_Knob('timingFrame2', 'Frame')
        timingFrame.setRange(0, 1000)
        timingFrame.setDefaultValue([1])
        timingFrame.setFlag(nuke.ALWAYS_SAVE)
        ctrlPanel.addKnob(timingFrame)
        linkKnobs('timingFrame2', int)
        
        
        # Creating Motion knobs and knobChanges
        internalPicker('motionEstimation', 'Motion')
        
        detailReg = nuke.Double_Knob('vectorDetailReg', 'Vector Detail')
        detailReg.setRange(0.01, 1)
        detailReg.setDefaultValue([0.3])
        detailReg.setFlag(nuke.ALWAYS_SAVE)
        ctrlPanel.addKnob(detailReg)
        linkKnobs('vectorDetailReg', float)

        strength = nuke.Double_Knob('strengthReg', 'Strength')
        strength.setRange(0, 1.5)
        strength.setDefaultValue([1.5])
        strength.setFlag(nuke.ALWAYS_SAVE)
        ctrlPanel.addKnob(strength)
        linkKnobs('strengthReg', float)

        detailLocal = nuke.Double_Knob('vectorDetailLocal', 'Vector Detail')
        detailLocal.setRange(0.01, 1)
        detailLocal.setDefaultValue([0.2])
        detailLocal.setFlag(nuke.ALWAYS_SAVE)
        ctrlPanel.addKnob(detailLocal)
        linkKnobs('vectorDetailLocal', float)

        smooth = nuke.Double_Knob('smoothnessLocal', 'Smoothness')
        smooth.setRange(0.01, 1)
        smooth.setDefaultValue([0.5])
        smooth.setFlag(nuke.ALWAYS_SAVE)
        ctrlPanel.addKnob(smooth)
        linkKnobs('smoothnessLocal', float)
        
        
        # Filter knob
        filter = nuke.Enumeration_Knob('resampleType', 'Filter', ['Bilinear', 'Lanczos4', 'Lanczos6'])
        filter.setDefaultValue([0])
        filter.setFlag(nuke.ALWAYS_SAVE)
        ctrlPanel.addKnob(filter)
        linkKnobs('resampleType', int)
        
        
        # Begin 'Shutter' Group
        shutterBegin = nuke.Tab_Knob('shutterBegin', 'Shutter', nuke.TABBEGINCLOSEDGROUP)
        ctrlPanel.addKnob(shutterBegin)

        samples = nuke.Int_Knob('shutterSamples', 'Shutter Samples')
        samples.setDefaultValue([1])
        samples.setFlag(nuke.ALWAYS_SAVE)
        ctrlPanel.addKnob(samples)
        linkKnobs('shutterSamples', int)

        time = nuke.Double_Knob('shutterTime', 'Shutter Time')
        time.setRange(0,10)
        time.setDefaultValue([0])
        time.setFlag(nuke.ALWAYS_SAVE)
        ctrlPanel.addKnob(time)
        linkKnobs('shutterTime', float)

        # Linking 'Auto' knob
        internalPicker('autoShutterTime', 'Automatic Shutter Time')


        # End 'Shutter' group
        shutterEnd = nuke.Tab_Knob('shutterEnd', 'Shutter', nuke.TABENDGROUP)
        ctrlPanel.addKnob(shutterEnd)


        # Creating 'Output' and 'Matte' knobs
        output = nuke.Enumeration_Knob('output', 'Output', ['Result', 'Matte', 'Foreground', 'Background'])
        output.setDefaultValue([0])
        output.setFlag(nuke.ALWAYS_SAVE)
        ctrlPanel.addKnob(output)
        linkKnobs('output', int)

        matte = nuke.Enumeration_Knob('matteChannel', 'Matte', ['None', 'Source Alpha', 'Source Inverted Alpha', 'Matte Luminance', 'Matte Inverted Luminance', 'Matte Alpha', 'Matte Inverted Alpha'])
        matte.setDefaultValue([0])
        matte.setFlag(nuke.ALWAYS_SAVE)
        ctrlPanel.addKnob(matte)
        linkKnobs('matteChannel', int)


        # Begin 'Advanced' Group (CONTAINS ANOTHER GROUP)
        advBegin = nuke.Tab_Knob('advBegin', 'Advanced', nuke.TABBEGINCLOSEDGROUP)
        ctrlPanel.addKnob(advBegin)

        flicker = nuke.Disable_Knob('flickerCompensation', 'Flicker Compensation')
        flicker.setFlag(nuke.ALWAYS_SAVE)
        ctrlPanel.addKnob(flicker)
        linkKnobs('flickerCompensation', bool)


        # Begin 'Tolerances' group
        tolBegin = nuke.Tab_Knob('tolBegin', 'Tolerances', nuke.TABBEGINCLOSEDGROUP)
        ctrlPanel.addKnob(tolBegin)

        red = nuke.Double_Knob('weightRed', 'Weight Red')
        red.setRange(0,1)
        red.setDefaultValue([0.3])
        red.setFlag(nuke.ALWAYS_SAVE)
        ctrlPanel.addKnob(red)
        linkKnobs('weightRed', float)

        green = nuke.Double_Knob('weightGreen', 'Weight Green')
        green.setRange(0,1)
        green.setDefaultValue([0.6])
        green.setFlag(nuke.ALWAYS_SAVE)
        ctrlPanel.addKnob(green)
        linkKnobs('weightGreen', float)

        blue = nuke.Double_Knob('weightBlue', 'Weight Blue')
        blue.setRange(0,1)
        blue.setDefaultValue([0.1])
        blue.setFlag(nuke.ALWAYS_SAVE)
        ctrlPanel.addKnob(blue)
        linkKnobs('weightBlue', float)

        # End 'Tolerances' group
        tolEnd = nuke.Tab_Knob('tolEnd', 'Tolerances', nuke.TABENDGROUP)
        ctrlPanel.addKnob(tolEnd)


        # Creating last knobs
        spacing = nuke.Int_Knob('vectorSpacing', 'Vector Spacing')
        spacing.setDefaultValue([20])
        spacing.setFlag(nuke.ALWAYS_SAVE)
        ctrlPanel.addKnob(spacing)
        linkKnobs('vectorSpacing', int)


        with ctrlPanel:
            # Creating 'Overlay' knob separate from function to prevent starting on new line
            [select.setSelected(True) for select in nuke.allNodes('NoOp')]
            for user in nuke.selectedNodes():
                overlay = nuke.Disable_Knob('showVectors', 'Overlay Vectors')
                overlay.setValue(each['showVectors'].value())
                overlay.setFlag(nuke.ALWAYS_SAVE)
                user.addKnob(overlay)
        target = '{}.{}'.format(user.name(), 'showVectors')
        link = nuke.Link_Knob('showVectors', 'Overlay Vectors')
        link.clearFlag(nuke.STARTLINE)
        link.setLink(target)
        ctrlPanel.addKnob(link)
        each['showVectors'].setExpression(str(ctrlPanel.name()+'.'+user.name()+'.showVectors'))


        # End 'Advanced' group
        advEnd = nuke.Tab_Knob('advEnd', 'Advanced', nuke.TABENDGROUP)
        ctrlPanel.addKnob(advEnd) 
        
        
        # Setting visibility of knobs
        with ctrlPanel:
            [select.setSelected(True) for select in nuke.allNodes('NoOp')]
            node = nuke.selectedNode()
            parent = node.parent()

            # 'Motion' Knob
            for label in ['motionEstimation', 'vectorDetailReg', 'strengthReg', 'vectorDetailLocal', 'smoothnessLocal', 'resampleType', 'output', 'matteChannel', 'flickerCompensation', 'weightRed', 'weightGreen', 'weightBlue', 'showVectors']:
                if node['interpolation'].value() == 'Motion':
                    parent.knob(label).setEnabled(True)
                    if node['showVectors'].value() == 0:
                        parent['vectorSpacing'].setEnabled(False)
                elif node['interpolation'].value() == 'Frame' or 'Blend':
                    parent.knob(label).setEnabled(False)
                    parent['vectorSpacing'].setEnabled(False)
                    
            
            # 'Timing' Knob
            if node['timing2'].value() == 'Output Speed':
                parent['timingOutputSpeed'].setVisible(True)
                parent['timingInputSpeed'].setVisible(False)
                parent['timingFrame2'].setVisible(False)
            elif node['timing2'].value() == 'Input Speed':
                parent['timingOutputSpeed'].setVisible(False)
                parent['timingInputSpeed'].setVisible(True)
                parent['timingFrame2'].setVisible(False)
            elif node['timing2'].value() == 'Frame':
                parent['timingOutputSpeed'].setVisible(False)
                parent['timingInputSpeed'].setVisible(False)
                parent['timingFrame2'].setVisible(True)

            # 'Motion' Knob
            if node['motionEstimation'].value() == 'Regularized':
                parent['vectorDetailReg'].setVisible(True)
                parent['strengthReg'].setVisible(True)
                parent['vectorDetailLocal'].setVisible(False)
                parent['smoothnessLocal'].setVisible(False)
            elif node['motionEstimation'].value() == 'Local':
                parent['vectorDetailReg'].setVisible(False)
                parent['strengthReg'].setVisible(False)
                parent['vectorDetailLocal'].setVisible(True)
                parent['smoothnessLocal'].setVisible(True)

            # 'Auto' Knob
            if node['autoShutterTime'].value() == 0:
                parent['shutterTime'].setEnabled(True)
            elif node['autoShutterTime'].value() == 1:
                parent['shutterTime'].setEnabled(False)
        
        
            # Defining knobChanged
            knobChange = '''
node = nuke.thisNode()
knob = nuke.thisKnob()
parent = node.parent()

# 'Motion' Knob
for label in ['motionEstimation', 'vectorDetailReg', 'strengthReg', 'vectorDetailLocal', 'smoothnessLocal', 'resampleType', '', 'matteChannel', 'flickerCompensation', 'weightRed', 'weightGreen', 'weightBlue', 'showVectors']:
    if node['interpolation'].value() == 'Motion':
        parent.knob(label).setEnabled(True)

        if node['motionEstimation'].value() == 'Regularized':
            node['motionEstimation'].setValue('Local')
            node['motionEstimation'].setValue('Regularized')
        elif node['motionEstimation'].value () == 'Local':
            node['motionEstimation'].setValue('Regularized')
            node['motionEstimation'].setValue('Local')
        if node['showVectors'].value() == 0:
            parent['vectorSpacing'].setEnabled(False)
            node['showVectors'].setValue(1)
            node['showVectors'].setValue(0)
        elif node['showVectors'].value() == 1:
            parent['vectorSpacing'].setEnabled(True)
            node['showVectors'].setValue(0)
            node['showVectors'].setValue(1)

    elif node['interpolation'].value() == 'Frame' or 'Blend':
        parent.knob(label).setEnabled(False)
        parent['vectorSpacing'].setEnabled(False)

        if node['motionEstimation'].value() == 'Regularized':
            node['motionEstimation'].setValue('Local')
            node['motionEstimation'].setValue('Regularized')
        elif node['motionEstimation'].value () == 'Local':
            node['motionEstimation'].setValue('Regularized')
            node['motionEstimation'].setValue('Local')
        if node['showVectors'].value() == 0:         
            node['showVectors'].setValue(1)
            node['showVectors'].setValue(0)
        elif node['showVectors'].value() == 1:
            node['showVectors'].setValue(0)
            node['showVectors'].setValue(1)


# 'Timing' Knob
if knob.name()== 'timing2' and knob.value() == 'Output Speed':
    parent['timingOutputSpeed'].setVisible(True)
    parent['timingInputSpeed'].setVisible(False)
    parent['timingFrame2'].setVisible(False)
elif knob.name()== 'timing2' and knob.value() == 'Input Speed':
    parent['timingOutputSpeed'].setVisible(False)
    parent['timingInputSpeed'].setVisible(True)
    parent['timingFrame2'].setVisible(False)
elif knob.name()== 'timing2' and knob.value() == 'Frame':
    parent['timingOutputSpeed'].setVisible(False)
    parent['timingInputSpeed'].setVisible(False)
    parent['timingFrame2'].setVisible(True)

# 'Motion' Knob
if knob.name()== 'motionEstimation' and knob.value() == 'Regularized':
    parent['vectorDetailReg'].setVisible(True)
    parent['strengthReg'].setVisible(True)
    parent['vectorDetailLocal'].setVisible(False)
    parent['smoothnessLocal'].setVisible(False)
elif knob.name()== 'motionEstimation' and knob.value() == 'Local':
    parent['vectorDetailReg'].setVisible(False)
    parent['strengthReg'].setVisible(False)
    parent['vectorDetailLocal'].setVisible(True)
    parent['smoothnessLocal'].setVisible(True)

# 'Auto' Knob
if knob.name() == 'autoShutterTime' and knob.value() == 0:
    parent['shutterTime'].setEnabled(True)
elif knob.name() == 'autoShutterTime' and knob.value() == 1:
    parent['shutterTime'].setEnabled(False)

# 'Overlay' Knob
if knob.name() == 'showVectors' and knob.value() == 0:
    parent['vectorSpacing'].setEnabled(False)
elif knob.name() == 'showVectors' and knob.value() == 1:
    parent['vectorSpacing'].setEnabled(True)
'''

            node['knobChanged'].setValue(knobChange)
        

        # Control panel details
        line = nuke.Text_Knob('', '')
        ctrlPanel.addKnob(line)

        bakeScr = '''
group = nuke.thisNode()
nuke.toNode('group').end()

# Debug dependentNodes not evaluating the first time
try:
    deps = nuke.dependentNodes(nuke.EXPRESSIONS, [group])
except:
    exit()

# Get dependent nodes
deps = nuke.dependentNodes(nuke.EXPRESSIONS, [group])
linked = deps[0]

allKnobs = {
    'gpuName': 'Local GPU:',
    'useGPUIfAvailable': 'Use GPU if available',
    'input.first': 'Input Range',
    'input.last': 'Input Range',
    'interpolation': 'Method',
    'timing2': 'Timing',
    'timingOutputSpeed': 'Output Speed',
    'timingInputSpeed': 'Input Speed',
    'timingFrame2': 'Frame',
    'motionEstimation': 'Motion',
    'vectorDetailReg': 'Vector Detail',
    'strengthReg': 'Strength',
    'vectorDetailLocal': 'Vector Detail',
    'smoothnessLocal': 'Smoothness',
    'resampleType': 'Filter',
    'shutterSamples': 'Shutter Samples',
    'shutterTime': 'Shutter Time',
    'autoShutterTime': 'Automatic Shutter Time',
    'output': 'Output',
    'matteChannel': 'Matte',
    'flickerCompensation': 'Flicker Compensation',
    'weightRed': 'Weight Red',
    'weightGreen': 'Weight Green',
    'weightBlue': 'Weight Blue',
    'vectorSpacing': 'Vector Spacing',
    'showVectors': 'Overlay Vectors'
}


# Copying values
for label in list(allKnobs.keys()):
    if group.knob(label).isAnimated() == False:
        linked.knob(label).clearAnimated()
    elif group.knob(label).isAnimated() == True:
        linked.knob(label).clearAnimated()
        linked.knob(label).copyAnimation(0, group.knob(label).animation(0))        

# Forcing knobChange for native node
if group['timing2'].value() == 'Output Speed':
    linked['timingOutputSpeed'].setVisible(True)
    linked['timingInputSpeed'].setVisible(False)
    linked['timingFrame2'].setVisible(False)
elif group['timing2'].value() == 'Input Speed':
    linked['timingOutputSpeed'].setVisible(False)
    linked['timingInputSpeed'].setVisible(True)
    linked['timingFrame2'].setVisible(False)
elif group['timing2'].value() == 'Frame':
    linked['timingOutputSpeed'].setVisible(False)
    linked['timingInputSpeed'].setVisible(False)
    linked['timingFrame2'].setVisible(True)

if group['motionEstimation'].value() == 'Regularized':
    linked['vectorDetailReg'].setVisible(True)
    linked['strengthReg'].setVisible(True)
    linked['vectorDetailLocal'].setVisible(False)
    linked['smoothnessLocal'].setVisible(False)
elif group['motionEstimation'].value() == 'Local':
    linked['vectorDetailReg'].setVisible(False)
    linked['strengthReg'].setVisible(False)
    linked['vectorDetailLocal'].setVisible(True)
    linked['smoothnessLocal'].setVisible(True)
                  
nuke.delete(group)
'''
    
        bake = nuke.PyScript_Knob('bakeValues', 'Bake Values', bakeScr)
        bake.setTooltip('Copy values and animations into native node and deletes control panel.')
        ctrlPanel.addKnob(bake)
        
        space = nuke.Text_Knob('space', '')
        space.setValue('     ')
        ctrlPanel.addKnob(space)
        
        version = nuke.Text_Knob('version', '')
        version.setValue('''<font color='#7F7F7F'><font size="12">&nbsp;&nbsp;&nbsp;&nbsp;<font size="3">Ctrl Panel<font size="1">&nbsp; v3.0''')
        version.setTooltip('last updated 22/05/2025\n\n@kl')
        ctrlPanel.addKnob(version)
        

        # Deselecting group so code can run on individual nodes
        ctrlPanel.setSelected(False)