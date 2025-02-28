import os, sys

def make_dir() :
    root_path = '/nas/eval/show'
    project_name = input(str("project name : "))

    set_type = input(str("work type (asset = 1 seq = 2) : "))
    if set_type == "1" :
        set_type_str = "asset"
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
        task_types = ["model", "rig", "lookdev"]
        work_types = ["work", "pub"]
        for work_type in work_types :
            if work_type == "work" : 
                for task_type in task_types :
                    path = f"{root_path}/{project_name}/{set_type_str}/{asset_type}/{asset_name}/{task_type}/{work_type}/maya/scenes/"
                    if not os.path.exists(path):
                        os.makedirs(path)

            elif work_type == "pub" :
                inner_dirs = ["scenes", "alembic", "data"]
                for task_type in task_types :
                    for inner_dir in inner_dirs :
                        path = f"{root_path}/{project_name}/{set_type_str}/{asset_type}/{asset_name}/{task_type}/{work_type}/maya/{inner_dir}"
                        if not os.path.exists(path):
                            os.makedirs(path)

    elif set_type == "2" :
        set_type_str = "seq"
        seq_name = input(str("seq name : "))
        shot_name = input(str("shot name :"))
        task_types = ["matchmove", "layout", "animation", "lighting", "comp"]
        work_types = ["work", "pub"]
        for work_type in work_types :
            if work_type == "work" :
                for task_type in task_types :
                    path = f"{root_path}/{project_name}/{set_type_str}/{seq_name}/{shot_name}/{task_type}/{work_type}/maya/scenes/"
                    print(path)
                    if not os.path.exists(path):
                        os.makedirs(path)
            elif work_type == "pub" :
                inner_dirs = ["scenes", "alembic", "data"]
                for task_type in task_types :
                    for inner_dir in inner_dirs :
                        path = f"{root_path}/{project_name}/{set_type_str}/{seq_name}/{shot_name}/{task_type}/{work_type}/maya/{inner_dir}"
                        print(path)
                        if not os.path.exists(path):
                            os.makedirs(path)
if __name__ == "__main__":
    make_dir()