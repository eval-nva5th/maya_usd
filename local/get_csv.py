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
only_shot_path = set()
only_seq_path = []

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
                #asset_paths.append([proj_name, asset_type, asset_name, folder_type, program_name,idk, file, f"{root}/{file}"])
                #task_path.append([task_name, asset_name, new_folder_type, status])
                #asset_path_short.append([asset_name, asset_type, folder_type])
                #pub_path.append([file, published_file_type , task_name, asset_name, description, root_path ,f"{root}/{file}"])
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
                task_name = f"{shot_name}_{task_type}"
                status = "ip"
                description = f"{shot_name} {task_type} {status}"
                root_path = f"/{seq_roots[1]}/{seq_roots[2]}/{seq_roots[3]}/{seq_roots[4]}"
        
                #seq_paths.append([proj_name, file_type, seq_name, shot_name, task_type, program_name, idk, file, f"{root}/{file}"])
                #only_seq_path.append([seq_name])
                pub_path.append([file, task_name, shot_name, description, root_path ,f"{root }/{file}"])
                #task_path.append([task_name, shot_name, task_type, status])
                #only_shot_path.add((seq_name, shot_name))
        
#df1 = pd.DataFrame(asset_paths, columns=['Project Name', 'Asset Type', 'Asset Name', 'Pipeline Step', 'Status','Name', 'File Path'])

#df2 = pd.DataFrame(seq_paths, columns=['proj name','file type', 'seq name', 'shot name', 'task type', 'program name', 'idk', 'Filename', 'full path'])
#df3 = pd.DataFrame(asset_path_short, columns = ['asset name', 'asset type', 'folder type'])
#df4 = pd.DataFrame(in_asset_path, columns = ['asset name', 'type'])
#task_path_df = pd.DataFrame(task_path, columns=['task_name', 'asset_name', 'new_folder_type', 'status'])
pub_path_df = pd.DataFrame(pub_path, columns=['Published File Name', 'Task', 'Link','Description', 'Path Cache', 'Local Path'])
#shot_df = pd.DataFrame(only_shot_path, columns=['Sequence', 'Shot'])
#task_df = pd.DataFrame(task_path, columns=['task_name', "shot_name", "task_type", "status"])
#seq_df = pd.DataFrame(only_seq_path, columns=['Sequence'])

# 결과를 CSV 파일로 저장
#df1.to_csv('asset_paths.csv', index=False)
#df2.to_csv('/nas/sy_test_folder/seq_trial/seq_paths.csv', index=False)
#shot_df.to_csv('/nas/sy_test_folder/seq_trial/only_shot_paths.csv', index=False)
#seq_df.to_csv('/nas/sy_test_folder/seq_trial/only_seq_paths.csv', index=False)
pub_path_df.to_csv('/nas/sy_test_folder/seq_trial/pub_paths.csv', index=False)