import json

class coco_trans():
    def __init__(self):
        self.images = []
        self.annotations = []
        self.categories = []
        self.image_id = {}
        self.cat_id = {}

    def add_img(self, file_name:str):
        iid = len(self.images)
        self.images.append(
            {
                "id":iid,
                "file_name":file_name
            }
        )
        self.image_id[file_name] = iid
        return iid

    def add_annotation(self, file_name:str, points:list, label:str):
        """[summary]

        Args:
            file_name (str): 圖片名稱
            points (list): [x1,y1,x2,y2,...]
            label (str): class
        """
        aid = len(self.annotations)
        
        if file_name in list(self.image_id.keys()):
            iid = self.image_id[file_name]
        else:
            iid = self.add_img(file_name)
            
        if label in list(self.cat_id.keys()):
            cid = self.cat_id[label]
        else:
            cid = self.add_category(label)
            
        segmentation = points
        
        self.annotations.append(
            {
                "id": aid,
                "iscrowd": 0,
                "image_id": iid,
                "category_id": cid,
                "segmentation":[segmentation]
            }
        )

    def add_category(self, name:str):
        cid = len(self.categories)
        self.categories.append(
            {
                "id": cid,
                "name": name
            }
        )
        self.cat_id[name] = cid
        return cid

    def save(self, path:str):
        d = {
            "images":self.images,
            "annotations":self.annotations,
            "categories":self.categories
        }
        try:
            with open(path, "w", encoding="utf-8") as file:
                json.dump(d, file, indent=4, ensure_ascii=False)
        except:
            pass
