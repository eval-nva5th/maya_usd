import maya.cmds as cmds
import os

class PlayblastManager:
    def __init__(self, output_path, mode):
        """
        플레이블라스트 관리 클래스
        :param output_path: 저장 경로
        :param mode: "asset" (턴테이블) 또는 "shot" (샷 카메라)
        """
        self.output_path = output_path
        # self.mode = self.check_scene_type()
        self.mode = mode
        self.camera_name = None
        self.camera_group = None
        self.start_frame, self.end_frame = self.get_shot_frame_range() if self.mode == "shot" else (1, 120)
    
    def run_playblast(self):
        """플레이블라스트 실행"""

        self.setup()
        cmds.lookThru(self.camera_name) # 선택된 카메라 활성화
        cmds.select(clear=True) # 오브젝트 선택 해제

        # 해상도 설정
        scale_factor = 0.7
        cmds.setAttr("defaultResolution.width", 1920)
        cmds.setAttr("defaultResolution.height", 1080)
        cmds.setAttr("defaultResolution.deviceAspectRatio", 1.777)

        # 저장 경로 확인 및 생성
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)

        # 에셋네임, 모델.... 이런식으로 저장하기로 했었는데..
        filename = f"{self.output_path}/{self.mode}.mov"

        if self.camera_name:
            cmds.lookThru(self.camera_name)
        else:
            raise RuntimeError("카메라를 찾을 수 없어 플레이블라스트를 실행할 수 없습니다.")

        # 플레이블라스트 실행
        cmds.playblast(
            startTime=self.start_frame,
            endTime=self.end_frame,
            format="qt",
            compression="jpeg",
            quality=100,
            filename=filename,
            clearCache=True,
            offScreen=True,
            viewer=False,
            showOrnaments=False,
            forceOverwrite=True,
            widthHeight=(
                int(cmds.getAttr("defaultResolution.width") * scale_factor),
                int(cmds.getAttr("defaultResolution.height") * scale_factor),
            )
        )

        self.capture_frame(self.start_frame)
        print(f"플레이블라스트 완료: {filename}")

        if self.mode == "asset":
                self.delete_turntable_camera()

    def capture_frame(self, frame_number):
        """특정 프레임을 이미지 1장으로 저장"""
        filename = f"{self.output_path}/frame_{frame_number}.jpg"
        cmds.playblast(
            startTime=frame_number,
            endTime=frame_number,
            format="image",
            completeFilename=filename,
            viewer=False
        )
        print(f"프레임 {frame_number} 저장 완료: {filename}")

    def setup(self):
        """초기 설정을 적용하는 메서드"""
        self.apply_scene_settings()
        if self.mode == "asset":
            if self.camera_group:  # 카메라 그룹이 존재하는 경우에만 애니메이션 적용
                # self.add_lighting()
                self.apply_turntable_animation()
            else:
                print("카메라 그룹 x,턴테이블 적용 못함")

    def check_scene_type(self):
        """현재 씬이 '에셋'인지 '샷'인지 판별"""
        return "shot" if cmds.ls(type="camera", long=True) else "asset"

    def apply_scene_settings(self):
        """에셋/샷별로 다른 설정 적용"""
        if self.mode == "asset":
            self.camera_group, self.camera_name = self.create_turntable_camera()
        elif self.mode == "shot":
            self.camera_name = self.find_shot_camera()

        if not self.camera_name:
            raise RuntimeError("카메라를 찾을 수 없어 플레이블라스트를 실행할 수 없습니다.")

    def delete_turntable_camera(self):
        """생성된 턴테이블 카메라와 그룹을 삭제"""
        if self.camera_group and cmds.objExists(self.camera_group):
            cmds.delete(self.camera_group)
            print(f"카메라 그룹 삭제 완료: {self.camera_group}")

        if self.camera_name and cmds.objExists(self.camera_name):
            cmds.delete(self.camera_name)
            print(f"카메라 삭제 완료: {self.camera_name}")

    def find_shot_camera(self):
        """샷 카메라를 찾아 반환 (없으면 기본 persp 카메라 사용)"""
        default_cameras = {"persp", "top", "front", "side"}
        all_cameras = cmds.ls(type="camera")

        # 'shot'이 포함된 카메라 찾기
        shot_cameras = [
            cmds.listRelatives(cam, parent=True)[0] for cam in all_cameras
            if cmds.listRelatives(cam, parent=True)[0] not in default_cameras and "shot" in cam.lower()
        ]

        if not shot_cameras:
            print("'shot' 카메라를 찾지 못했습니다. 기본 'persp' 카메라를 사용합니다.")
            return "persp"  # 기본 persp 카메라 사용

        print(f"선택된 샷 카메라: {shot_cameras[0]}")
        return shot_cameras[0]

    def get_shot_frame_range(self):
        """샷의 시작 및 종료 프레임 가져오기"""
        self.start_frame = int(cmds.playbackOptions(query=True, minTime=True))
        self.end_frame = int(cmds.playbackOptions(query=True, maxTime=True))
        print(f"샷 프레임 범위: {self.start_frame} ~ {self.end_frame}")
        return self.start_frame, self.end_frame

    def create_turntable_camera(self):
        """턴테이블 카메라 생성"""
        if cmds.objExists("camera_group"):
            cmds.delete("camera_group")
        if cmds.objExists("turntable_camera"):
            cmds.delete("turntable_camera")

        asset = self.find_assets()
        bbox = cmds.exactWorldBoundingBox(asset)

        center_x, center_y, center_z = (bbox[0] + bbox[3]) / 2, (bbox[1] + bbox[4]) / 2, (bbox[2] + bbox[5]) / 2
        max_size = max(bbox[3] - bbox[0], bbox[4] - bbox[1], bbox[5] - bbox[2])

        camera, camera_shape = cmds.camera(name="turntable_camera")
        camera_group = cmds.group(camera, name="camera_group")

        cmds.xform(camera_group, worldSpace=True, translation=[center_x, center_y, center_z])
        cmds.xform(camera, relative=True, translation=[0, 0, max_size * 2.5])

        cmds.setAttr(f"{camera_shape}.farClipPlane", max_size * 5)

        aim_constraint = cmds.aimConstraint(asset, camera, aimVector=[0, 0, -1], upVector=[0, 1, 0], worldUpType="scene")
        cmds.delete(aim_constraint)

        cmds.select(camera)
        cmds.viewFit(camera, fitFactor=1.2)

        print(f"카메라 생성 완료: {camera}")

        return camera_group, camera

    def apply_turntable_animation(self):
        """카메라 그룹에 턴테이블 애니메이션 적용"""
        if not cmds.objExists(self.camera_group):
            print("카메라 그룹이 없습니다! 애니메이션을 적용하지 않습니다.")
            return

        cmds.cutKey(self.camera_group, attribute="rotateY")
        cmds.setKeyframe(self.camera_group, attribute="rotateY", time=1, value=0)
        cmds.setKeyframe(self.camera_group, attribute="rotateY", time=120, value=360)
        cmds.selectKey(self.camera_group, attribute="rotateY", time=(1, 120))
        cmds.keyTangent(inTangentType="linear", outTangentType="linear")

        print(f"턴테이블 애니메이션 적용 완료: {self.camera_group}")

    def find_assets(self):
        """씬에서 에셋 찾기 (카메라, 라이트, 컨트롤러 등 불필요한 요소 제외)"""
        all_objects = cmds.ls(transforms=True)  # 모든 변환 가능한 오브젝트 가져오기
        
        # 카메라 및 부모 제거
        camera_objects = cmds.ls(cameras=True)  # 씬 내 모든 카메라 가져오기
        camera_parents = cmds.listRelatives(camera_objects, parent=True) or []  # 카메라 부모 가져오기
        
        # 라이트 및 부모 제거
        lights = cmds.ls(lights=True)  # 씬 내 모든 라이트 가져오기
        light_parents = cmds.listRelatives(lights, parent=True) or []  # 라이트 부모 가져오기

        # 기본 Maya 오브젝트 제거 (디스플레이 레이어, 렌더 레이어 등)
        default_sets = cmds.ls("default*", transforms=True) or []
        
        # 컨트롤러 및 리깅 관련 노드 제거 (보편적인 필터링 기준)
        control_rig_objects = cmds.ls("*_ctrl", "*_rig", transforms=True) or []

        # 완전한 필터링 리스트
        exclude_objects = set(camera_parents + light_parents + lights + default_sets + control_rig_objects)

        # 최종 필터링 적용
        assets = [obj for obj in all_objects if obj not in exclude_objects]

        if not assets:
            raise RuntimeError("씬에 유효한 에셋이 없음!")

        print(f"찾은 에셋 리스트: {assets}")  # 이제 모든 불필요한 요소가 제거됨!
        return assets[0]  # 첫 번째 유효한 에셋 반환