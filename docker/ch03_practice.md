# Dockerfile 스크립트 없이 도커 이미지 만들기

- diamol/ch03-lab 이미지
- 안에 ch03.txt 텍스트 파일 수정한 후 새로운 이미지 빌드
- Dockerfile 스크립트 쓰지 않고

```
  run         Create and run a new container from an image
docker container run -it --name ch03lab diamol/ch03-lab
## --name 태그로 ch03lab 이라고 컨테이너 이름 주고. 이미지 diamol/ch03-lab 을 실행

echo name >> ch03.txt
## 텍스트 파일에 이름 추가


  commit      Create a new image from a container's changes
Usage:  docker container commit [OPTIONS] CONTAINER [REPOSITORY[:TAG]]
docker container commit ch03lab ch03lab-sol



확인 
docker container run ch03lab-sol cat ch03.txt

```