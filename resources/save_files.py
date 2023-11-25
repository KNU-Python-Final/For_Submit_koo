import json 
import resources.images.characters as characters # resources.images.characters 를 characters 라고 할게요~
'''
json: 텍스트로 된 딕셔너리 (dict만 json 으로 변경 가능)

직렬화 : dict to json
json.dumps(딕셔너리) -> str

역직렬화 : json to dict
json.loads(str) -> dict


'''
# 인벤토리
class save_file:
    def __init__(self) -> None: # return x
        self.score = 0
        self.image_file = characters.default_str
        self.inventory = {
            characters.default_str: True,
            characters.king_str: False,
            characters.heart_king_str: False,
            characters.leaf_str: False,
            characters.heart_leaf_str: False,
            characters.angel_str: False,
            characters.heart_angel_str: False,
            characters.santa_str: False,
            characters.heart_santa_str: False,
        }
    def to_dict(self) -> dict[str, any]: # json으로 바꿔주기 위해 class를 dict로 바꿈 (class to dict)
        return {
            'score' : self.score,
            'image_file' : self.image_file,
            'inventory' : self.inventory,
        }

    def from_dict(self, dict : dict[str, any]) -> None: # json을 class로 바꾸기 위해 'dict를 class에 삽입' (dict to class)
        self.score = dict['score']
        self.image_file = dict['image_file']
        self.inventory = dict['inventory']
        

    def save(self) -> None: # return x
        data_dict = self.to_dict() # class to dict
        data_json = json.dumps(data_dict, indent = 2) # dict to json 
        with open('save_file.json', 'w') as file: # json to file
            file.write(data_json)


    def load(self) -> None: # return x
        try:
            with open("save_file.json", "r") as file:
                json_str = file.read() # file to json
                json_dict = json.loads(json_str) # json to dict
                self.from_dict(json_dict) # dict to class

        except FileNotFoundError:
            self.save()
            return None