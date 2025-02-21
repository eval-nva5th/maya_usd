'''

Maya Scene
work path
/nas/show/{PROJECT}/assets/{ASSET_TYPE}/{ASSET_NAME}/{TASK}/work/maya/scenes/{ASSET_NAME}_{TASK}_v001.{EXT}
publish path
/nas/show/{PROJECT}/assets/{ASSET_TYPE}/{ASSET_NAME}/{TASK}/pub/maya/scenes/{ASSET_NAME}_{TASK}_v001.{EXT}
Alembic Cache
publish path
/nas/show/{PROJECT}/assets/{ASSET_TYPE}/{ASSET_NAME}/{TASK}/pub/maya/alembic/{ASSET_NAME}_{TASK}_v001.abc
MOV
publish path
/nas/show/{PROJECT}/assets/{ASSET_TYPE}/{ASSET_NAME}/{TASK}/pub/maya/data/{ASSET_NAME}_{TASK}_v001.mov
/nas/show/{PROJECT}/product/{2025-0217}/assets/{ASSET_NAME}_{TASK}_v001.mov

Shot Publish Path
Maya Scene
work path
/nas/show/{PROJECT}/seq/{SEQ}/{SHOT}/{TASK}/work/maya/scenes/{SHOT}_{TASK}_v001.{EXT}
publish path
/nas/show/{PROJECT}/seq/{SEQ}/{SHOT}/{TASK}/pub/maya/scenes/{SHOT}_{TASK}_v001.{EXT}
Alembic Cache
publish path
/nas/show/{PROJECT}/seq/{SEQ}/{SHOT}/{TASK}/pub/maya/alembic/{ASSET_NAME}_{TASK}_v001.abc
MOV
publish path
/nas/show/{PROJECT}/seq/{SEQ}/{SHOT}/{TASK}/pub/maya/data/{SHOT}_{TASK}_v001.mov
/nas/show/{PROJECT}/product/{2025-0217}/seq/{SHOT}_{TASK}_v001.mov
'''
import os, sys
import pandas as pd

# root_path = '/nas/eval/show'
# project_name = 'sample'
# work_type = 'assets' # or seq
# if work_type == 'assets' :
#     asset_type = "prop" # vehicle characeter environment
#     asset_name = "sample"
#     task_type = "modelling" # rigging lookdev
#     work_type = "work" #"pub"
#     if work_type == "work" : 
#         ext = ["usd","ma"]
#     if work_type == "pub" :
#         inner_dir = ["scenes", "alembic", "data"]
#         for item in inner_dir :
#             if item == "scenes" :
#                 ext = "usd"
#             elif item == "alembic" :
#                 ext = "abc"
#             elif item == "data" :
#                 ext = "mov"

#     file_name = f"{asset_name}_{task_type}_v001.{ext}"


root_path = '/nas/eval/show'
project_name = input(str("project name : "))

set_type = input(str("work type (assets = 1 seq = 2) : "))
if set_type == "1" :
    set_type_str = "assets"
    asset_type = input("asset type (prop : 1 vehicle 2 character 3 environment 4) : ")
    if asset_type == "1" :
        asset_type = "prop"
    elif asset_type == "2" :
        asset_type = "vehicle"
    elif asset_type == "3" :
        asset_type = "character" 
    elif asset_type == "4" :
        asset_type = "environment"
    asset_name = input(str("asset name (space with _): "))       
    task_types = ["modelling", "rigging", "lookdev"]
    work_types = ["work", "pub"]
    for work_type in work_types :
        if work_type == "work" : 
            for task_type in task_types :
                print(f"{root_path}/{project_name}/{set_type_str}/{asset_type}/{asset_name}/{task_type}/{work_type}/maya/scenes/")
        elif work_type == "pub" :
            inner_dirs = ["scenes", "alembic", "data"]
            for task_type in task_types :
                for inner_dir in inner_dirs :
                    print(f"{root_path}/{project_name}/{set_type_str}/{asset_type}/{asset_name}/{task_type}/{work_type}/maya/{inner_dir}")

elif set_type == "2" :
    set_type_str = "seq"
    shot_name = input(str("shot name :"))



'''
work path
/nas/show/{PROJECT}/seq/{SEQ}/{SHOT}/{TASK}/work/maya/scenes/{SHOT}_{TASK}_v001.{EXT}
publish path
/nas/show/{PROJECT}/seq/{SEQ}/{SHOT}/{TASK}/pub/maya/scenes/{SHOT}_{TASK}_v001.{EXT}
Alembic Cache
publish path
/nas/show/{PROJECT}/seq/{SEQ}/{SHOT}/{TASK}/pub/maya/alembic/{ASSET_NAME}_{TASK}_v001.abc
MOV
publish path
/nas/show/{PROJECT}/seq/{SEQ}/{SHOT}/{TASK}/pub/maya/data/{SHOT}_{TASK}_v001.mov
/nas/show/{PROJECT}/product/{2025-0217}/seq/{SHOT}_{TASK}_v001.mov
'''



