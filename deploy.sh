#!/bin/bash

# 스크립트 실행 오류 시 즉시 종료
set -e

# GitHub Actions에서 SSM 파라미터로 전달된 값 받기
# $1: ECR 이미지 URI (예: 123456789012.dkr.ecr.ap-northeast-2.amazonaws.com/my-app:abcdef123456)
# $2: 컨테이너 이름 (예: my-app)
ECR_IMAGE_URI=$1
CONTAINER_NAME=$2

# EC2 메타데이터에서 현재 리전 가져오기
REGION=$(curl -s http://xxx.xxx.xxx.xxx/latest/meta-data/placement/availability-zone | sed 's/[a-z]$//') 

echo "--- 배포 시작 ---"
echo "배포할 이미지: ${ECR_IMAGE_URI}"
echo "컨테이너 이름: ${CONTAINER_NAME}"
echo "AWS Region: ${REGION}"

# 1. ECR 로그인 (EC2 인스턴스의 IAM 역할 권한 사용)
echo "ECR에 로그인 중..."
aws ecr get-login-password --region ${REGION} | docker login --username AWS --password-stdin $(echo ${ECR_IMAGE_URI} | cut -d'/' -f1)
echo "ECR 로그인 성공."

# 2. 최신 Docker 이미지 풀 받기
echo "최신 이미지 풀 받기: ${ECR_IMAGE_URI}"
docker pull ${ECR_IMAGE_URI}
echo "이미지 풀 받기 완료."

# 3. 기존 컨테이너 중지 및 삭제 (실행 중인 경우)
echo "기존 컨테이너 중지 및 삭제 중..."
if docker ps -a | grep -q ${CONTAINER_NAME}; then
    docker stop ${CONTAINER_NAME}
    docker rm ${CONTAINER_NAME}
    echo "기존 컨테이너 중지 및 삭제 완료."
else
    echo "실행 중인 컨테이너 없음. 스킵."
fi

# 4. 새로운 Docker 컨테이너 실행
echo "새로운 컨테이너 실행 중: ${CONTAINER_NAME} from ${ECR_IMAGE_URI}"

# 실제 애플리케이션의 포트 설정에 맞게 변경 (예시: 80)
docker run -d --name ${CONTAINER_NAME} -p 80:80 ${ECR_IMAGE_URI}
echo "새로운 컨테이너 실행 완료."

# 5. 사용되지 않는 이미지 정리
echo "사용되지 않는 이미지 정리 중..."
docker image prune -f
echo "이미지 정리 완료."

echo "--- 배포 완료 ---"
