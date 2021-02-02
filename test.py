import os
import shutil
import json

from VGG_trans import VGG_trans

def load_json(path):
    _dict={}
    try:
        with open(path,encoding="utf-8") as file:
            _dict = json.load(file)
        return True, _dict
    except:
        return False, _dict

rootDir = './data/test1/'
labels = VGG_trans()
for _file in os.listdir(rootDir):
    if _file.split('.')[-1] == 'png' and _file.split('.')[-2] != 'cs':
        labels.add_img(_file, _file)
        imgPath = os.path.join(rootDir, _file)
        newPath = os.path.join('./VGG/', _file)
        shutil.copyfile(imgPath, newPath)
for _file in os.listdir(rootDir):
    if _file.split('.')[-1]=='json':
        jsonPath = os.path.join(rootDir, _file)
        OK, _json = load_json(jsonPath)
        name = _file.replace('.json', '.png')
        for index, obj in enumerate(_json['objects']):
            label = obj['class']
            x1y1 = obj['bounding_box']['top_left']
            x2y2 = obj['bounding_box']['bottom_right']
            x2y1 = [x2y2[0], x1y1[1]]
            x1y2 = [x1y1[0], x2y2[1]]
            points = [x1y1, x2y1, x2y2, x1y2]
            points = [[y,x] for x,y in points]
            labels.add_label(name, index, points, label)
labels.save('./VGG/test.json')