import maya.cmds as mc
import random
import os

mySelection=[]
filePath = ""
Expression = ""

#UI LAYOUT
myWindow = mc.window(title = "Pose Export/Import", wh=(500,200), resizeToFitChildren = False)
mc. columnLayout()
mc.rowColumnLayout(numberOfColumns = 2, columnWidth = [(1, 400)])
mc.showWindow(myWindow)


Expression = mc.textFieldGrp( l = "Pose / Expression  " , editable = True)
mc.text(label="")
mc.text(label="\n Pick controllers first\n")
mc.button(label="PickObjects", command="mySelection=pickObjects()")
mc.text(label="\nSelect the library file you would like to use\n")
pickPathButton = mc.button(label="Library file",command="filePath = pickPath()")
mc.text(label="\nExport a new pose\n")
saveButton = mc.button(label= "Export", command= "exportSequence(mySelection)")

mc.text(label="\nImport an existing pose based on the name")
pickPathButton = mc.button(label="Import", align='right' , command="importSequence(mySelection)")

#Functions

def pickObjects():
    return mc.ls(sl=True)

def pickPath():
    return mc.fileDialog2(dialogStyle=2, fileMode =3)

#

def exportSequence(mySelectionT):
    
    rangeMin = mc.playbackOptions( min = True, q = True)
    rangeMax = mc.playbackOptions( max = True, q = True)
        
    for i in range( int(rangeMin), int(rangeMax)):
        mc.currentTime( i, edit=True )
        saveExpression(filePath, mySelectionT, i)


def saveExpression(pathTxtFile, selectionVar, numberFrame):
   
   exName = cmds.textFieldGrp( Expression, query=True, text=True)
   
   fileName = pathTxtFile[0] + "/" + exName + str(numberFrame) + ".txt"
   
   file(fileName, "w")
   fileHandle = open(fileName,'a')
   fileHandle.write(os.linesep + exName + os.linesep)
    
   for i in selectionVar:
        
        #Saving Attributes
        transX = mc.getAttr(i+".translateX")
        transY = mc.getAttr(i+".translateY")
        transZ = mc.getAttr(i+".translateZ")
	rotX = mc.getAttr(i+".r")[0][0]
	rotY = mc.getAttr(i+".r")[0][1]
	rotZ = mc.getAttr(i+".r")[0][2]
        
        fileHandle.write(i + ",")
        fileHandle.write(str(transX) + ",")
        fileHandle.write(str(transY) + ",")
        fileHandle.write(str(transZ) + ",")
        fileHandle.write(str(rotX) + ",")
        fileHandle.write(str(rotY) + ",")
        fileHandle.write(str(rotZ) + os.linesep)
	
   fileHandle.write("-----------------------")
   fileHandle.close()
   

def importSequence(mySelectionT):
    rangeMin = mc.playbackOptions( min = True, q = True)
    rangeMax = mc.playbackOptions( max = True, q = True)
        
    for i in range( int(rangeMin), int(rangeMax)):
        mc.currentTime( i, edit=True )
        applyExpression(filePath, mySelectionT, i)
        mc.setKeyframe()
    


def applyExpression(pathTxtFile, selectionVar, numberFrame):
   
   exName = cmds.textFieldGrp( Expression, query=True, text=True)
   
   fileName = pathTxtFile[0] + "/" + exName + str(numberFrame) + ".txt"
   
   #Deviding text into individual controller data
   fileHandle = open(fileName,'r')
   my_str = fileHandle.read()
   specificEx = filter(bool, my_str.split('-----------------------'))
   for i in specificEx:
       print "----" + i
           
   
   
   #Dividing each expression and checking which expression was asked for.
   #Due to the way notepad writes its files + the way we saved our preset,
   #the expression name somehow has unneeded empty space behind it. To fix this
   #we take the length of the asked expression name and use that to shrink the preset expression names.
   
   for d in specificEx:
       ctrlAttr = d.split("\n")
       temp = ctrlAttr[1][:len(exName)]
       print temp
       if temp == exName:
           print "yay, we have a match!"
           
           #Going over all the objects selected.
           #Dividing the controller data and checking if the controller name is the same as the selected controller.
           #If this is true, then the data behind the name will be copied.
           for i in selectionVar:
       
               for j in ctrlAttr:
                   
                   temp = j.split(",")
                   
                   print i
                   print temp[0]
                   
                   if temp[0] == i:
                       
                       #Now that we have the matching object, we still have to check on every attribute if it's locked
                       #or the transaction will give errors.
                       if mc.getAttr(i+".translateX",lock=True) != 1:
                           mc.setAttr(i+".translateX", float(temp[1]))
                       
                       if mc.getAttr(i+".translateY",lock=True) != 1:
                           mc.setAttr(i+".translateY", float(temp[2]))
                       
                       if mc.getAttr(i+".translateZ",lock=True) != 1:
                           mc.setAttr(i+".translateZ", float(temp[3]))
                       
                       if mc.getAttr(i+".rotateX",lock=True) != 1:
                           mc.setAttr(i+".rotateX", float(temp[4]))
                       
                       if mc.getAttr(i+".rotateY",lock=True) != 1:
                           mc.setAttr(i+".rotateY", float(temp[5]))
                                          
                       if mc.getAttr(i+".rotateZ",lock=True) != 1:
                           mc.setAttr(i+".rotateZ", float(temp[6]))
                                             
                    
   fileHandle.close()
   print "DONE"