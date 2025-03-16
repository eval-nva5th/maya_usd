import platform
from shotgun_api3 import Shotgun

class DefaultConfig:
    _instance = None
    
    sg_url = "https://5thacademy.shotgrid.autodesk.com/"
    script_name = "sy_key"
    api_key = "vkcuovEbxhdoaqp9juqodux^x"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DefaultConfig, cls).__new__(cls)
            cls._instance._init_paths()
            cls._instance.shotgrid_connector()  # Initialize Shotgun connector
        return cls._instance

    def _init_paths(self):
        system = platform.system()

        if system == 'Linux':  # 리눅스
            self.root_path = "nas/eval"
            self.file_root_path = ""  # this is for syspath
        elif system == 'Darwin':  # 맥
            self.root_path = '/Users/user/myfolder'  ## must be modified. show 파트 이전까지임
            self.file_root_path = ""
        else:
            self.root_path = ""
            self.file_root_path = ""
    
    def shotgrid_connector(self):
        self.sg = Shotgun(
            DefaultConfig.sg_url,
            DefaultConfig.script_name,
            DefaultConfig.api_key
        )
        return self.sg

    def get_root_path(self):
        return self.root_path
    
    def get_file_root_path(self):
        return self.file_root_path
