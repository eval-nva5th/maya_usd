import os
import pandas as pd

directory = '/nas/eval/show/eval'

file_paths = []
asset_paths = []
seq_paths = []
asset_path_short = []
in_asset_path = set()
task_path = []
pub_path = []

for root, dirs, files in os.walk(directory):
    for file in files:
        file_path = os.path.join(root, file) 
        asset_roots = root.split('/')
        if "assets" in root : 
            #asset_paths.append([root, file])
            if len(asset_roots) == 12 and asset_roots[9] == "pub":
                proj_name = asset_roots[4]
                file_type = asset_roots[5]
                asset_type = asset_roots[6]
                asset_name = asset_roots[7]
                folder_type = asset_roots[8]
                program_name = asset_roots[10]
                idk = asset_roots[11]
                
                status = 'ip'
                replace = {'modelling' : 'model', 'lookdev' : 'texture', 'rigging' : 'rig'}
                new_folder_type = replace[folder_type]
                
                task_name = f"{asset_name}_{new_folder_type}"
                
                published_file_type = "Usd File"
                root_path = f"/nas/eval/show/{proj_name}"
                
                eliminated_root = root.replace(root_path, "")
                file_name, ext = file.split('.')
                version = file_name[-4:]
                
                description = f"{asset_name} {new_folder_type} {status}"
                #asset_paths.append([proj_name, asset_type, asset_name, folder_type, program_name,idk, file, f"{root}/{file}"])
                #task_path.append([task_name, asset_name, new_folder_type, status])
                #asset_path_short.append([asset_name, asset_type, folder_type])
                pub_path.append([file, published_file_type , task_name, asset_name, description, root_path ,f"{root}/{file}"])
                #in_asset_path.add((asset_name, asset_type))

        elif "seq" in root :
            seq_roots = root.split('/')
            if len(seq_roots) == 12 and seq_roots[9] == "pub" :
                #/nas/eval/show/Project_205/seq/OPN/OPN_0010/layout/pub/maya/data
                proj_name = seq_roots[4]
                file_type = seq_roots[5]
                seq_name = seq_roots[6]
                shot_name = seq_roots[7]
                task_type = seq_roots[8]
                program_name = seq_roots[10]
                idk = seq_roots[11]
                seq_paths.append([proj_name, file_type, seq_name, shot_name, task_type, program_name, idk, file, f"{root}/{file}"])
        
#df1 = pd.DataFrame(asset_paths, columns=['Project Name', 'Asset Type', 'Asset Name', 'Pipeline Step', 'Status','Name', 'File Path'])

#df2 = pd.DataFrame(seq_paths, columns=['proj name','file type', 'seq name', 'shot name', 'task type', 'program name', 'idk', 'Filename', 'full path'])
#df3 = pd.DataFrame(asset_path_short, columns = ['asset name', 'asset type', 'folder type'])
#df4 = pd.DataFrame(in_asset_path, columns = ['asset name', 'type'])
#task_path_df = pd.DataFrame(task_path, columns=['task_name', 'asset_name', 'new_folder_type', 'status'])
pub_path_df = pd.DataFrame(pub_path, columns=['Published File Name', 'Published File Type', 'Task', 'Link','Description', 'Path Cache', 'Local Path'])

# 결과를 CSV 파일로 저장
#df1.to_csv('/nas/sy_test_folder/task_asset_paths.csv', index=False)
#df2.to_csv('seq_paths.csv', index=False)
#df3.to_csv('/nas/sy_test_folder/asset_paths_brief.csv', index=False)
#df4.to_csv('/nas/sy_test_folder/initial_asset.csv', index=False)
#task_path_df.to_csv('/nas/sy_test_folder/task_asset_paths.csv', index=False)
pub_path_df.to_csv('/nas/sy_test_folder/pub_asset_path.csv', index=False)
