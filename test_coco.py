import os
import shutil
import json

import cv2

from coco_trans import coco_trans

def load_json(path):
    _dict={}
    try:
        with open(path,encoding="utf-8") as f:
            _dict = json.load(f)
        return True, _dict
    except:
        return False, _dict

def load_label(path, size):
    labels = []
    with open(path, encoding="utf-8") as f:
        temp_list = f.readlines()
    for text in temp_list:
        c, cx, cy, w, h = text.rstrip().split(" ")
        cx = float(cx) * size[1]
        w = float(w) * size[1]
        cy = float(cy) * size[0]
        h = float(h) * size[0]
        labels.append((int(c), cx, cy, w, h))
    return labels

coco = coco_trans()
rootDir = './data/'
images_dir = os.path.join(rootDir, "images")
txt_dir = os.path.join(rootDir, "labels")

classes = []
class_path = os.path.join(rootDir, "classes.txt")
with open(class_path,encoding="utf-8") as f:
    classes = f.readlines()

for _file in os.listdir(images_dir):
    if _file.split('.')[-1] in ['png', 'jpg', 'jpeg']:
        txt_path = os.path.join(txt_dir, _file.replace(_file.split('.')[-1], "txt"))
        if not os.path.isfile(txt_path): 
            continue
        image = cv2.imread(os.path.join(images_dir, _file))
        labels = load_label(txt_path, image.shape[:2])
        coco.add_img(_file)
        for c, cx, cy, w, h in labels:
            points = []
            x1 = cx - w/2
            x2 = x1 + w
            y1 = cy - h/2
            y2 = y1 + h
            points.extend([x1,y1])
            points.extend([x2,y1])
            points.extend([x2,y2])
            points.extend([x1,y2])
            coco.add_annotation(_file, points, classes[c])
os.makedirs("./coco",exist_ok=True)
coco.save('./coco/annotations.json')