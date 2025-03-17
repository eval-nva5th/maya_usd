from shotgun_api3 import Shotgun

class ShotgridAPI :
    _instance = None
    
    sg_url = "https://5thacademy.shotgrid.autodesk.com/"
    script_name = "sy_key"
    api_key = "vkcuovEbxhdoaqp9juqodux^x"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ShotgridAPI, cls).__new__(cls)
            cls._instance.shotgrid_connector()  # Initialize Shotgun connector
        return cls._instance
    
    @staticmethod
    def shotgrid_connector():
        sg = Shotgun(
            ShotgridAPI.sg_url,
            ShotgridAPI.script_name,
            ShotgridAPI.api_key
        )
        return sg