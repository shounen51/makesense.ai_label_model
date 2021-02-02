import json

class VGG_trans():
    def __init__(self):
        self.labels={}

    def add_img(self, img_name:str, path:str):
        self.labels[img_name] = {}
        self.labels[img_name]['filename'] = path
        self.labels[img_name]['regions'] = {}

    def add_label(self, img_name:str, index:int, points:list, label:str):
        if points[0] != points[-1]:
            points.append(points[0])
        xs = []
        ys = []
        for x,y in points:
            xs.append(x)
            ys.append(y)
        self.labels[img_name]['regions'][str(index)] = {
            'shape_attributes':{
                "name": "polygon",
                "all_points_x": xs,
                "all_points_y": ys
            },
            "region_attributes": {
                "label": label
            }
        }

    def save(self, path:str):
        try:
            with open(path, "w", encoding="utf-8") as file:
                json.dump(self.labels, file, indent=4, ensure_ascii=False)
        except:
            pass
