#by gloop#5445

#==User Config==#
use_set_image_path = False #drag and drop an image onto the script if this is False to select the image, otherwise image_file is used as a fallback
image_file = "coco.png" #path to image used if "use_set_image_path" is enabled
prefab_type = "Cube"
center_image = True
flip_image_vertical = False
flip_image_horizontal = True
disable_object_texture = True
enable_object_physics = False #I *really* don't recommend enabling this
image_scale = 0.1
environment_type = "None" #Options are: Barren, None, Desert, Tolbrynd, MountainTop
#===============#
prefabs = {
    "Cube": "7000",
    "Cylinder": "7001",
    "Sphere": "7002",
    "Wedge": "7003",
    "Pyramid": "9027",
    "Pyramid Corner": "9028",
    "Cone": "9040",
    "Textured Cube": "9024",
    "Textured Cylinder":"9023",
    "Textured Sphere": "9025",
    "Textured Wedge": "9026",
    "Textured Pyramid": "9029",
    "Textured Pyramid Corner": "9030",
    "Textured Cone": "9041"
}
prefab_type = prefabs[prefab_type]
import xml.etree.ElementTree as et
import sys,os
from PIL import Image,ImageOps #pip install pillow
import math
if not use_set_image_path:
    if len(sys.argv)>1:
        image_file = sys.argv[1]
output_file = image_file.split(".")
output_file[1] = "blv"
output_file = ".".join(output_file)
level = et.Element("Level")
tree = et.ElementTree(level)
level_settings = et.SubElement(level,"LevelSettings")
level_settings.attrib = {"EditorVersion": "0.8","Environment": environment_type}
et.SubElement(level_settings,"DisableBounds").attrib = {"Enabled": "False","Locked": "False"}
objects = et.SubElement(level,"Objects")

os.system("")
print("\x1b[2J\x1b[0;0H\x1b[?25l")
with Image.open(image_file) as im:
    im = im.convert("RGB")
    if flip_image_vertical:
        im = ImageOps.flip(im)
    if flip_image_horizontal:
        im = ImageOps.mirror(im)
    w,h = im.size
    px = im.load()

if center_image:
    offset = (w//2,h//2)
def euler_to_quaternion(angle):
    roll,pitch,yaw = angle
    roll,pitch,yaw = roll*math.pi/2,pitch*math.pi/2,yaw*math.pi/2
    quat_x = math.sin(roll) * math.cos(pitch) * math.cos(yaw) - math.cos(roll) * math.sin(pitch) * math.sin(yaw)
    quat_y = math.cos(roll) * math.sin(pitch) * math.cos(yaw) + math.sin(roll) * math.cos(pitch) * math.sin(yaw)
    quat_z = math.cos(roll) * math.cos(pitch) * math.sin(yaw) - math.sin(roll) * math.sin(pitch) * math.cos(yaw)
    quat_w = math.cos(roll) * math.cos(pitch) * math.cos(yaw) + math.sin(roll) * math.sin(pitch) * math.sin(yaw)
    return [quat_x, quat_y, quat_z, quat_w]

def create_prefab(type,id,transform,color,data):
    prefab = et.SubElement(objects,"Object")

    prefab_id = str(id).rjust(19,"4")
    prefab.attrib = {'ID': prefab_id,'Prefab': str(type)}

    pos,ang,scale=transform
    ang = euler_to_quaternion(ang)
    prefab_position = et.SubElement(prefab,"Position")
    prefab_position.attrib = {"x": str(pos[0]),"y": str(pos[1]),"z": str(pos[2])}
    prefab_rotation = et.SubElement(prefab,"Rotation")
    prefab_rotation.attrib = {"x": str(ang[0]),"y": str(ang[1]),"z": str(ang[2]),"w": str(ang[3])}
    prefab_scale = et.SubElement(prefab,"Scale")
    prefab_scale.attrib = {"x": str(scale[0]),"y": str(scale[1]),"z": str(scale[2])}
    prefab_data = et.SubElement(prefab,"Data")

    prefab_color = et.SubElement(prefab_data,"Color")
    prefab_color.attrib = {"key": "bmt-colour"}
    color = [i/255 for i in color]

    et.SubElement(prefab_color,"R").text = str(color[0])
    et.SubElement(prefab_color,"G").text = str(color[1])
    et.SubElement(prefab_color,"B").text = str(color[2])

    for i in data:
        type,attrib,text = i
        data_element = et.SubElement(prefab_data,type)
        if attrib != "":
            data_element.attrib = attrib
        if text != "":
            data_element.text = text

for z in range(h):
    if int(h/100) != 0 and z%int(h/100) == 0:
        print(f"{(z/h)*100:.0f}% Complete..",end="\r")
    for x in range(w):
        pixel_color = px[x,z]
        create_prefab(prefab_type,1,[(((x-offset[0])*image_scale),0,(z-offset[1])*image_scale),(0,0,0),(image_scale,image_scale,image_scale)],pixel_color,
            [
                ["Boolean",{"key":"bmt-Disable Texture"},str(disable_object_texture)],
                ["Boolean",{"key":"bmt-lel-enable-physics"},str(enable_object_physics)]
            ]
        )
print("\x1b[2J\x1b[0;0H\x1b[?25l")
print("Done!")
et.indent(tree)
tree.write(output_file, encoding = "UTF-8", xml_declaration = True)
