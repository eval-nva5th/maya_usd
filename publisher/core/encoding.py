import subprocess
# 영상 슬레이트 인코딩 프로그램입니다. 실행 전 ffmpeg 설치 필수.

class LastFramecount() :
    # ffprobe 사용해서 영상정보 속 마지막 프레임값 뽑아오기
    def get_last_framecount(self, input_file) :
        command =f'ffprobe -v error -select_streams v:0 -show_entries stream=nb_frames -of default=noprint_wrappers=1:nokey=1 "{input_file}"'
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
        last_frame_count = int(result.stdout.strip())

        return last_frame_count
    
class EncodeProcess:
    
    def __init__(self):
        pass

    def input_command(self, input_file):
        #input_file 파일주소
        # 시작 커맨드
        command = f'ffmpeg -y -i "{input_file}"'
        return command

    def output_codec_command(self, output_file):
        command = f'-c:a copy "{output_file}"'
        return command

    def padding_command(self):
        
        # 위 아래 레터박스 추가하는 커맨드
        command = 'drawbox=x=0:y=0:w=iw:h=ih*0.1:color=black@1.0:t=fill,\
            drawbox=x=0:y=ih*0.9:w=iw:h=ih*0.1:color=black@1.0:t=fill'
        return command

    def slate_command(self, text1, text2, text3, text4, start_num, last_num):
        # 파라미터로 받아온 각 문자들을 drawtext 하는 커맨드 
        command = (
            f'drawtext=text=\'{text1}\':fontcolor=white:fontsize=15:x=20:y=(h*0.1-text_h)/2,'  # 상단 좌측
            f'drawtext=text=\'{text2}\':fontcolor=white:fontsize=15:x=(w-text_w)/2:y=(h*0.1-text_h)/2,'  # 상단 중앙
            'drawtext=text=\'%{localtime\:%Y-%m-%d}\':fontcolor=white:fontsize=15:x=w-text_w-20:y=(h*0.1-text_h)/2,'  # 상단 우측
            f'drawtext=text=\'{text3}\':fontcolor=white:fontsize=15:x=20:y=h*0.9+((h*0.1-text_h)/2),'  # 하단 좌측
            f'drawtext=text=\'{text4}\':fontcolor=white:fontsize=15:x=(w-text_w)/2:y=h*0.9+((h*0.1-text_h)/2),'  # 하단 중앙
            'drawtext=text=\'TC %{pts\\:hms}\':fontcolor=white:fontsize=10:x=w-text_w-20:y=h*0.94-text_h,'  # 하단 우측 첫번째줄 - 타임코드
            f'drawtext=text=\'%{{eif\\:n+{start_num}\\:d}} /     \':fontcolor=white:fontsize=10:x=w-(text_w*3):y=h*0.95,'  # 하단 우측 두번째줄 - 실시간 프레임카운트
            f'drawtext=text=\'{start_num}-{last_num}\':fontcolor=white:fontsize=10:x=w-text_w-20:y=h*0.95'  # 하단 우측 두번째줄 - 첫프레임 마지막프레임
        )
        return command
    def run(self, input_file, output_file, codec, shot_num, project_name, task_name, comp_version, start_frame, last_frame):
        
        # 받아온 프레임카운트에 시작프레임 더하기 연산
        last_frame = last_frame + start_frame - 1 
        
        # 파라미터로 커맨드 순차대로 받아오기
        command1 = self.input_command(input_file)
        command2 = self.padding_command()
        command3 = self.slate_command(shot_num, project_name, task_name, comp_version, start_frame, last_frame)
        command4 = self.output_codec_command(output_file, codec)

        # 필터 연결하고 전체 커맨드 생성
        filter_complex = f'-vf "{command2},{command3}"'

        #전체 커맨드 문자열로
        full_command = f'{command1} {filter_complex} {command4}'

        subprocess.run(full_command, shell=True, check= True)

# input_file = "/home/rapa/my_eval/pb_test/asset/shot.mov" #input path
# output_file = "/home/rapa/my_eval/pb_test/asset/shot.mov" #output path
# codec = input_file[-3:] #input path의 마지막 세 문자열을 슬라이싱하여 코덱 value로 사용 (mov or mp4)

# shot_num = "OPN_0010"
# project_name = "OPN"
# task_name = "task"
# comp_version = "v001"
# start_frame = 1000

# #
# lfc = LastFramecount()
# last_frame = lfc.get_last_framecount(input_file)
# encoder = EncodeProcess()
# encoder.run(input_file, output_file, codec, shot_num, project_name, task_name, comp_version, start_frame, last_frame)
