### 사용자 관련
- /etc/login.defs vim 으로 수정. (기본 설정 파일)

- useradd, adduser [user]
    - 사용자 계정 생성
    - 새로운 계정의 홈디렉토리는 /home/계정명
    - 계정정보는 /etc/passwd, /etc/shadow, /etc/group
    - 옵션, -s, -d, -e, -f, -c, -G, -p ... 등
        - -m 옵션 추가시 /home 디렉토리 같이 생성


- passwd
    - 계정의 패스워드 생성 및 변경
    - /etc/shadow 에 기록
    - 옵션
        - -h help
        - -l 비밀번호 잠금
        - -S status
        - -u unlock
        
- su 
    - 현재 사용자 계정에서 로그아웃하지 않고 다른 사용자 계정으로 로그인하여 해당 사용자 권한 획득 (switch user)

- whoami
    - 현재 내 계정 print

<br>

### 계정 관리 관련
- usermod
    - /home 에 위치한 사용자들의 정보 변경
    - 홈디렉토리변경, 그룹변경, 유효기간 변경,
    - root 만 가능
    - usermod -d [/home/temp2] -m [temp1] : 유저 temp1 홈디렉토리를 temp2 로 변경 
    - usermod -l [newuser] [기존user] : 유저 이름 변경

- userdel [user]
    - 유저 삭제
    - userdel -r [user] 로 해야 home 디렉토리까지 같이 삭제.

- change
    - 패스워드 만료 정보 변경
    - root 만 가능



### 그룹 관리 관련
- groupadd
    - /etc/group 에서 그룹명 확인
    - 그룹명:암호:GID:멤버들

- groupdel

- groupmod
    - 그롭 설정을 변경
    - -n 그룹명 변경
    - -g 그룹 GID 변경