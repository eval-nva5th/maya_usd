import platform

class SystemPath:
    _instance = None
    
    sg_url = "https://5thacademy.shotgrid.autodesk.com/"
    script_name = "sy_key"
    api_key = "vkcuovEbxhdoaqp9juqodux^x"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SystemPath, cls).__new__(cls)
            cls._instance._init_paths()
        return cls._instance

    def _init_paths(self):
        system = platform.system()

        if system == 'Linux':  # 리눅스
            self.root_path = "nas/eval"
            self.file_root_path = ""
        elif system == 'Darwin':  # 맥
            self.root_path = '/Volumes/TD_VFX/eval'
            self.file_root_path = ""
        else:
            self.root_path = ""
            self.file_root_path = ""
            
    def get_root_path(self):
        return self.root_path
    
    # def get_file_root_path(self):
    #     return self.file_root_path
    
    
