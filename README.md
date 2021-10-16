# api_test

**API Spec 확인**

서버를 띄우고, 브라우저에서 다음 페이지로 접속시 docs파일이 확인 가능합니다.
```
http://localhost/docs
```

## RUN
### Docker-compose를 이용하여 수행
```
$ docker-compose up
```

### 수동 실행
```
$ pyenv shell 3.8.6
$ virtualenv -p python venv
$ source ./venv/bin/activate
$ (venv) pip install -r requirements.txt
$ (venv) ./run.sh
```

