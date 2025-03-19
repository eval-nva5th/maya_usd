#!/bin/bash
set -e

# -------------------- `su` 모드로 변경 (사용자에게 비밀번호 입력 요청) --------------------
if [ "$(id -u)" -ne 0 ]; then
    echo "이 스크립트는 root 권한이 필요합니다. 'su' 명령어를 사용하여 root 권한을 얻은 후 다시 실행됩니다."
    exec sudo bash "$0" "$@"
fi

echo "Python 패키지 설치 시작"

# -------------------- Python 패키지 설치 --------------------
pip install --upgrade pip

pip install Flask
pip install python-socketio requests websocket-client
pip install shotgun-api3
pip install eventlet
pip install opencv_python
pip install Requests

echo "Python 패키지 설치 완료"

# -------------------- FFmpeg 및 GStreamer 설치 --------------------
echo "FFmpeg 및 GStreamer 설치 시작"

# FFmpeg 설치 시도
echo "FFmpeg 설치 중..."
yum install -y ffmpeg || echo "FFmpeg 설치 실패: 추가적인 repo가 필요할 수 있음."

# EPEL 및 RPMFusion 저장소 추가
echo "EPEL 및 RPMFusion 저장소 추가..."
yum install -y epel-release
yum install -y https://download1.rpmfusion.org/free/el/rpmfusion-free-release-$(rpm -E %rhel).noarch.rpm
yum install -y https://download1.rpmfusion.org/nonfree/el/rpmfusion-nonfree-release-$(rpm -E %rhel).noarch.rpm

# RPMFusion 수동 설치 (필요할 경우)
if ! yum list installed | grep -q rpmfusion-free-release; then
    echo "RPMFusion 수동 설치..."
    wget -O /tmp/rpmfusion-free-release-8.noarch.rpm https://mirrors.rpmfusion.org/free/el/rpmfusion-free-release-8.noarch.rpm
    yum install -y --nogpgcheck /tmp/rpmfusion-free-release-8.noarch.rpm
fi

# FFmpeg 다시 설치 (저장소 추가 후)
echo "FFmpeg 다시 설치..."
yum install -y ffmpeg

# GStreamer 패키지 설치
echo "GStreamer 패키지 설치 중..."
dnf install -y gstreamer1-libav gstreamer1-plugins-ugly

# 설치 확인
echo "설치 확인..."
ffmpeg -version && echo "FFmpeg 설치 완료"
gst-inspect-1.0 libav && echo "GStreamer 설치 완료"

echo "모든 패키지 설치 완료"
