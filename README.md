# Maya Pose Importer/Exporter
Simple pose importer/exporter for maya.
This was a simple script only made for exporting and importing poses/facial expressions.

# How it works  
An export creates a txt file with all the selected controller's values.
A name can be given to the pose like Happy, angry, walking,... to then call back at the import.

# UI  
First select the controllers you want have included in the export of the pose.
![Animation extractor](https://user-images.githubusercontent.com/12221965/113020015-79ca2900-9182-11eb-905e-5051c09fc566.png)

Confirm the selection by clicking on "pick objects.
"Library file" will select the folder where all the txt files will be saved. And where you can import the poses back from.

# Animations  
The script is not very optimized for exporting and importing animation, since it was not one of initally planned features.
It is possible but it will create a txt file for every frame and the import is much slower than export.
