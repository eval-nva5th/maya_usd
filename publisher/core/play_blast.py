import maya.cmds as cmds
import os, re, shutil, subprocess, time
from publisher.core.encoding import EncodeProcess
try :
    from PySide2.QtCore import QTimer
except Exception:
    from PySide6.QtCore import QTimer

class PlayblastManager:
    def __init__(self, file_path, filename_input):
        """
        플레이블라스트 관리 클래스
        :param file_path: 저장 경로
        :param mode: "asset" (턴테이블) 또는 "seq" (샷 카메라)
        """
        print ("플레이 블라스트 실행")
        self.file_path = file_path # 현재 파일 경로
        self.version_filename = filename_input # 버전 파일 이름
        self.new_path = self.convert_to_save_path() # playblast 저장되는 경로
        self.asset_name = self.extract_asset_name()  # 파일에서 에셋 이름 추출
        self.filename = self.extract_folders_from_path() # 파일이름
        self.mode = self.check_scene_type(self.file_path) # asset/seq 판별
        self.camera_name = None
        self.camera_group = None
        self.start_frame, self.end_frame = self.get_seq_frame_range() if self.mode == "seq" else (1, 120)

    def run_playblast(self):
        """플레이블라스트 실행"""
        self.setup()
        output_file = f"{self.new_path}/playblast.mov"

        print ("플레이 블라스트 시작~~~~~~~~~~~~~.")
        cmds.lookThru(self.camera_name) # 선택된 카메라 활성화
        cmds.select(clear=True) # 오브젝트 선택 해제

        # 해상도 설정
        scale_factor = 0.7
        cmds.setAttr("defaultResolution.width", 1920)
        cmds.setAttr("defaultResolution.height", 1080)
        cmds.setAttr("defaultResolution.deviceAspectRatio", 1.777)

        print(f"저장될 파일 이름: {self.filename}")

        if self.camera_name:
            cmds.lookThru(self.camera_name)
        else:
            raise RuntimeError("카메라를 찾을 수 없어 플레이블라스트를 실행할 수 없습니다.")

        # 플레이블라스트 실행
        result = cmds.playblast(
            startTime=self.start_frame,
            endTime=self.end_frame,
            format="qt",
            compression="jpeg",
            quality=100,
            filename=output_file,
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

        if not result or result == []:
            raise RuntimeError("플레이블라스트 실행 실패!")

        print(f"플레이블라스트 완료! 저장된 파일: {output_file}")

        # 스크린샷 캡쳐 1개
        master_jpg = f"{self.new_path}/{self.filename}.jpg"
        self.capture_frame(self.start_frame, master_jpg)

        if self.mode == "asset":
                self.delete_turntable_camera()

        return output_file

    def capture_frame(self, frame_number, path):
        """특정 프레임을 이미지 1장으로 저장""" 
        cmds.grid(toggle=False)
        cmds.playblast(
            startTime=frame_number,
            endTime=frame_number,
            format="image",
            completeFilename=path,
            viewer=False,
            clearCache=True,
            offScreen=True,
            forceOverwrite=True,
            widthHeight=[1920, 1080]
        )
        cmds.grid(toggle=True)
        print(f"프레임 {frame_number} 저장 완료: {self.filename}")

    def setup(self):
        """초기 설정을 적용하는 메서드"""
        self.apply_scene_settings()
        if self.mode == "asset":
            if self.camera_group:  # 카메라 그룹이 존재하는 경우에만 애니메이션 적용
                self.apply_turntable_animation()
            else:
                print("카메라 그룹 x,턴테이블 적용 못함")

    def convert_to_save_path(self):
        """새로 저장할 경로"""
        directory_path = os.path.dirname(self.file_path)  
        path_parts = directory_path.strip("/").split("/")  

        if "work" in path_parts:
            work_index = path_parts.index("work")
            path_parts[work_index] = "pub"
        
        if "scenes" in path_parts:
            scenes_index = path_parts.index("scenes")
            path_parts[scenes_index] = "data"

        new_path = "/" + "/".join(path_parts)
        return new_path

    def extract_folders_from_path(self) :
        """파일 이름"""
        path_parts = self.new_path.strip("/").split("/")
        if len(path_parts) >= 8:  
            self.project_name = path_parts[3]
            self.entity_name = path_parts[6]  # 원래 리스트로 가져와야 오류 방지됨
            self.task_name = path_parts[7]
            return f"{self.entity_name}_{self.task_name}"
        return "unknown_filename"
    
    def extract_asset_name(self):
        """파일명에서 에셋 이름을 추출 (_v001, _geo, _rig 등의 접미사를 제거)"""
        filename = os.path.basename(self.file_path)  # 파일명만 가져오기
        filename = os.path.splitext(filename)[0]  # 확장자 제거

        version_match = re.search(r'(_v\d{3})$', filename)
        self.version = version_match.group(1) if version_match else ""  # 버전 정보만 저장
        self.clean_version = self.version.lstrip("_")

        # 버전 정보 제거
        filename = re.sub(r'_v\d{3}$', '', filename)
        # `_geo`, `_grp`, `_rig`, `_model` 제거
        filename = re.sub(r'_(geo|grp|rig|model)$', '', filename)

        print(f"추출된 에셋 이름: {filename}")
        return filename

    def check_scene_type(self, path: str):
        """
        파일 경로에서 'assets' 또는 'seq' 여부를 판별하는 함수.
        """
        path_parts = path.lower().split("/")  # 경로를 소문자로 변환 후 '/' 기준으로 나누기
        
        if "assets" in path_parts:
            return "asset"
        elif "seq" in path_parts:
            return "seq"
        else:
            return "unknown"

    def apply_scene_settings(self):
        """에셋/샷별로 다른 설정 적용"""
        if self.mode == "asset":
            self.camera_group, self.camera_name = self.create_turntable_camera()
        elif self.mode == "seq":
            self.camera_name = self.find_seq_camera()

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

    def find_seq_camera(self):
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

    def get_seq_frame_range(self): # 셀프 빼도 상관이 없을까?
        """샷의 시작 및 종료 프레임 가져오기"""
        print("get_seq_frame_range() 실행")
        start_frame = int(cmds.playbackOptions(query=True, minTime=True))
        end_frame = int(cmds.playbackOptions(query=True, maxTime=True))
        print(f"샷 프레임 범위: {start_frame} ~ {end_frame}")
        return start_frame, end_frame

    def create_turntable_camera(self):
        """턴테이블 카메라 생성"""
        if cmds.objExists("camera_group"):
            cmds.delete("camera_group")
        if cmds.objExists("turntable_camera"):
            cmds.delete("turntable_camera")

        asset = self.find_assets()
        print("asset:", asset)

        if not asset:
            raise RuntimeError("유효한 에셋이 없어 카메라를 생성할 수 없습니다.")

        bbox = cmds.exactWorldBoundingBox(asset)
        print(f"Bounding Box: {bbox}")

        # 중심 좌표 계산
        center_x = (bbox[0] + bbox[3]) / 2
        center_y = (bbox[1] + bbox[4]) / 2
        center_z = (bbox[2] + bbox[5]) / 2
        print(f"Center Position: {center_x}, {center_y}, {center_z}")

        # 카메라 거리 계산 (최소 거리 보장)
        max_size = max(bbox[3] - bbox[0], bbox[4] - bbox[1], bbox[5] - bbox[2])
        if max_size < 1:
            max_size = 10

        distance = max_size * 3.0

        # 카메라 생성
        camera, camera_shape = cmds.camera(name="turntable_camera")
        camera_group = cmds.group(camera, name="camera_group")

        # 카메라 위치 조정
        cmds.xform(camera_group, worldSpace=True, translation=[center_x, center_y, center_z])
        cmds.xform(camera, relative=True, translation=[0, 0, distance * 1.1])

        # Near/Far Clipping Plane 조정 : 16:57 추가
        cmds.setAttr(f"{camera_shape}.farClipPlane", max_size * 10)  # 기존 5에서 10으로 확대
        cmds.setAttr(f"{camera_shape}.nearClipPlane", 0.01)  # 작은 오브젝트가 잘리지 않도록 설정

        cmds.setAttr(f"{camera_shape}.farClipPlane", max_size * 5)

        # Aim Constraint 추가 (삭제하지 않음)
        cmds.aimConstraint(asset, camera, aimVector=[0, 0, -1], upVector=[0, 1, 0], worldUpType="scene")

        # human만 viewFit 적용
        cmds.select(asset)
        cmds.xform(asset, cp=True)
        cmds.viewFit(camera, fitFactor=1.6)

        # 디버깅: 카메라 위치 & 방향 확인
        camera_pos = cmds.xform(camera, query=True, worldSpace=True, translation=True)
        camera_rotation = cmds.xform(camera, query=True, worldSpace=True, rotation=True)
        print(f"Camera Position: {camera_pos}")
        print(f"Camera Rotation: {camera_rotation}")

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
        # 컨트롤러 및 리깅 관련 노드 제거
        control_rig_objects = cmds.ls("*_ctrl", "*_rig", transforms=True) or []
        # 완전한 필터링 리스트
        exclude_objects = set(camera_parents + light_parents + lights + default_sets + control_rig_objects)
        valid_suffixes = ["", "_geo", "_grp", "_model", "_rig"]  # 자주 쓰이는 접미사 리스트
        possible_names = [f"{self.asset_name}{suffix}" for suffix in valid_suffixes]

        matched_assets = [
            obj for obj in all_objects
            if any(name.lower() == obj.lower() for name in possible_names) and obj not in exclude_objects
        ]

        if not matched_assets:
            raise RuntimeError(f"씬에서 '{self.asset_name}'과 관련된 에셋을 찾을 수 없음!")
        
        print(f"찾은 에셋 리스트: {matched_assets}")
        return matched_assets[0]  # 첫 번째 에셋 반환

    def save_playblast_files(self, version):
        """플레이블라스트 파일 저장 (MOV버전 포함)"""
        # 저장할 파일명 정리
        playblast_mov = f"{self.new_path}/playblast.mov"
        versioned_mov = f"{self.new_path}/{self.entity_name}_{self.task_name}_{version}.mov"
        master_mov = f"{self.new_path}/{self.filename}.mov"
        codec = playblast_mov[-3:]

        print ("versioned_mov 저장경로오오오오오오오오오 ",versioned_mov)

        # 마스터 MOV 파일 저장
        encoder = EncodeProcess()
        encoder.run(playblast_mov, master_mov, codec, self.entity_name, self.project_name, self.task_name, version, self.start_frame, self.end_frame)
        #버전 포함 MOV 파일 저장 (슬레이트 추가)
        encoder.run(playblast_mov, versioned_mov, codec, self.entity_name, self.project_name, self.task_name, version, self.start_frame, self.end_frame)

        versioned_jpg = f"{self.new_path}/{self.entity_name}_{self.task_name}_{version}.jpg"
        self.capture_frame(self.start_frame, versioned_jpg)
        print(f"저장 완료: {master_mov}, {versioned_mov}")

    def check_playblast_file(self, file_path):
        """파일이 존재할 때까지 반복 확인 (비동기 방식)"""
        if os.path.exists(file_path):
            if not self.file_checked: # 중복 실행 방지
                self.file_checked = True
                print(f"플레이블라스트 파일 확인됨! {file_path}")
                self.save_playblast_files()
            return
        else:
            print(f"플레이블라스트 파일 대기 중... {file_path}")
            QTimer.singleShot(500, lambda: self.check_playblast_file(file_path))  # 500ms 후 다시 체크