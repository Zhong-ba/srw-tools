import json

CONFIG = None


class Config:
    def __init__(self, file):
        self.IMAGE_PATH = F'{file["ImgPath"]}/assets/asbres'
        self.EXCEL_PATH = f'{file["DataPath"]}/MappedExcelOutput_EN'
        self.EXCEL_PATH_OLD = f'{file["DataPathOld"]}/MappedExcelOutput_EN'
        self.OUTPUT_PATH = file["OutputPath"]
        self.DATA_PATH = file["DataPath"]
    
    
with open('scriptconfig.json', 'r', encoding = 'utf-8') as file:
    CONFIG_FILE = json.load(file)
    CONFIG = Config(CONFIG_FILE)