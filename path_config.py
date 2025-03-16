import os
import platform

class PathConfig:
    """
    운영체제에 따른 루트 패스 변경 싱글톤 클래스
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PathConfig, cls).__new__(cls)
            cls._instance._init_paths()
        return cls._instance

    def _init_paths(self):
        system = platform.system()

        if system == 'Linux':  # 리눅스
            self.root_path = "nas/eval"
            self.file_root_path = ""
        elif system == 'Darwin':  # 맥
            self.root_path = '/Users/user/myfolder' ## must be modfied
            self.file_root_path = ""
        else:
            self.root_path = ""
            self.file_root_path = ""

    def get_root_path(self):
        return self.root_path
    
    def get_file_root_path(self) :
        return self.file_root_path
    