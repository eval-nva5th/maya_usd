import os

class PlayblastManager():
    def __init__(self):
        # 저장 경로 설정
        rootpath = "/home/rapa/my_eval/pbtest"
        scene_type = ""
        mov_file = f"{rootpath}/{scene_type}/playblast_output.mov"

        # 해상도 설정
        cmds.setAttr("defaultResolution.width", 1920) 
        cmds.setAttr("defaultResolution.height", 1080)
        cmds.setAttr("defaultResolution.deviceAspectRatio", 1.777)  # 16:9 비율

        # # 방법1
        cmds.playbackOptions(minTime=100, maxTime=100) # 프레임 1-100프레임
        start_frame = 1
        end_frame = 120

        # 파일사이즈 줄이기
        scale_factor = 0.7 

        # 특정 카메라 설정
        cmds.lookThru("persp")  # 사용할 카메라 이름 (예: persp, shotCam 등)

        cmds.playblast(
            startTime=start_frame,
            endTime=end_frame,
            format="qt",
            compression="jpeg",
            quality=100,
            filename = mov_file,
            clearCache=True, # 임시 플레이블라스트 삭제
            offScreen=True,     # 오프스크린 모드 활성화
            viewer=False, # 뷰어 실행 여부
            showOrnaments=False,  # HUD 제거
            forceOverwrite=True,  # 기존 파일 덮어쓰기
            widthHeight=(
                int(cmds.getAttr("defaultResolution.width") * scale_factor), 
                int(cmds.getAttr("defaultResolution.height") * scale_factor)
            )
        )

        # print(f"✅ Playblast MOV saved at: {outputPath}")

        """
        샷 하고 에셋하고 나누기 샷은 전체 출력 에셋은 100프레임부터
        """

        # 샷
        # 현재 타임라인 범위 가져오기
        # start_frame = cmds.playbackOptions(query=True, minTime=True)  # 현재 타임라인 시작 프레임
        # end_frame = cmds.playbackOptions(query=True, maxTime=True)  # 현재 타임라인 끝 프레임