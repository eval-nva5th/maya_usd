import subprocess

def create_mov_and_extract_jpg(text, mov_output_path, jpg_output_path):
    # MOV 파일 생성
    ffmpeg_mov_cmd = [
        'ffmpeg',
        '-y',  # 기존 파일 덮어쓰기
        '-f', 'lavfi',  # 필터 사용
        '-i', 'color=c=black:s=640x360:d=10',  # 1280x720 크기의 검은 배경, 길이 10초
        '-vf', (
             f"drawtext=text='{text}':fontcolor=white:fontsize=100:line_spacing=10:"
            "x=(w-text_w)/2:y=(h-text_h)/2:"
            "alpha='1-(t/10)'"  # 5초 후에 텍스트가 점차 사라짐
        ),
        '-c:v', 'libx264',  # 인코딩 코덱
        '-pix_fmt', 'yuv420p',  # 픽셀 형식
        '-movflags', '+faststart',  # 헤더 정보를 파일의 시작 부분에 배치
        mov_output_path
    ]

    # FFmpeg 명령 실행 (MOV 생성)
    subprocess.run(ffmpeg_mov_cmd, check=True)

    # 첫 프레임 JPG로 추출
    ffmpeg_jpg_cmd = [
        'ffmpeg',
        '-i', mov_output_path,
        '-vf', 'select=eq(n\\,0)',  # 첫 번째 프레임 선택
        '-vsync', 'vfr',
        '-q:v', '2',  # 높은 품질
        jpg_output_path
    ]

    # FFmpeg 명령 실행 (JPG 추출)
    subprocess.run(ffmpeg_jpg_cmd, check=True)

# 변수 설정
text = "bike_vehicle\nrig_v001"
mov_output_path = "/nas/sy_test_folder/encoding_trial/bike_vehicle_rig_v001.mov"
jpg_output_path = "/nas/sy_test_folder/encoding_trial/bike_vehicle_rig_v001.jpg"

# 함수 실행
create_mov_and_extract_jpg(text, mov_output_path, jpg_output_path)
