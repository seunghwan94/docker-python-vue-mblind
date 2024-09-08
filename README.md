# mlind
커뮤니티 사이트 제작
```
Server : Docker (Linux)
DB     : mriaDB
Back   : python (Flask)
Front  : vue (Bootstrap)
```
[Server Setting 가이드](https://gentle-chokeberry-d27.notion.site/Docker-centos7-python-nodejs-7f567599ee8c49418dfdf71c6c6c3d6f).


### DB 구조 load
```
mysql -u mlind -p mlind < mlind.sql
```

### Back Server 실행 
back 폴더 접속 후 
```
// 가상환경 접속
source .venv/bin/activate

// Flask 실행
python app.py

// 가상환경 나가는 방법
deactivate
```

### Front Server 실행
front 폴더 접속 후
```
// debug 모드
npm run serve 
```

localhost:8080 접속
