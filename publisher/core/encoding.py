import subprocess
import os
# 영상 슬레이트 인코딩 프로그램입니다. 실행 전 ffmpeg 설치 필수.

class EncodeProcess:
    
    def __init__(self, ffmpeg_path = None):
        self.ffmpeg_path = ffmpeg_path
        pass

    def input_command(self, input_file):
        return [self.ffmpeg_path, "-y", "-i", input_file]

    def output_codec_command(self, output_file):
        return ["-c:a", "copy", output_file]

    def padding_command(self):
        return 'drawbox=x=0:y=0:w=iw:h=ih*0.1:color=black@1.0:t=fill,drawbox=x=0:y=ih*0.9:w=iw:h=ih*0.1:color=black@1.0:t=fill'

    def slate_command(self, text1, text2, text3, text4, start_num, last_num):
        return (
            f'drawtext=text=\'{text1}\':fontcolor=white:fontsize=15:x=20:y=(h*0.1-text_h)/2,'
            f'drawtext=text=\'{text2}\':fontcolor=white:fontsize=15:x=(w-text_w)/2:y=(h*0.1-text_h)/2,'
            'drawtext=text=\'%{localtime\:%Y-%m-%d}\':fontcolor=white:fontsize=15:x=w-text_w-20:y=(h*0.1-text_h)/2,'
            f'drawtext=text=\'{text3}\':fontcolor=white:fontsize=15:x=20:y=h*0.9+((h*0.1-text_h)/2),'
            f'drawtext=text=\'{text4}\':fontcolor=white:fontsize=15:x=(w-text_w)/2:y=h*0.9+((h*0.1-text_h)/2),'
            'drawtext=text=\'TC %{pts\\:hms}\':fontcolor=white:fontsize=10:x=w-text_w-20:y=h*0.94-text_h,'
            f'drawtext=text=\'%{{eif\\:n+{start_num}\\:d}} /    \':fontcolor=white:fontsize=10:x=w-80:y=h*0.95,'
            f'drawtext=text=\'{start_num}-{last_num}\':fontcolor=white:fontsize=10:x=w-text_w-20:y=h*0.95'
        )
    
    def run(self, input_file, output_file, shot_num, project_name, task_name, comp_version, start_frame, last_frame):
        
        last_frame = last_frame + start_frame - 1 
        
        command1 = self.input_command(input_file)
        command2 = self.padding_command()
        command3 = self.slate_command(shot_num, project_name, task_name, comp_version, start_frame, last_frame)
        command4 = self.output_codec_command(output_file)

        filter_complex = f"-vf \"{command2},{command3}\""
        full_command = command1 + [filter_complex] + command4

        print("Executing command:", " ".join(full_command))

        env = os.environ.copy()
        env["PATH"] += os.pathsep + os.path.dirname(self.ffmpeg_path)

        p = subprocess.run(" ".join(full_command), shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
