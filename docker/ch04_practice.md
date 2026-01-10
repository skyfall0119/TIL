### 도커파일 최적화
#### 문제
```
FROM diamol/golang 

WORKDIR web
COPY index.html .
COPY main.go .

RUN go build -o /web/server
RUN chmod +x /web/server

CMD ["/web/server"]
ENV USER=sixeyed
EXPOSE 80
```

- 멀티 스테이지로 빌드 부분 분리
- CMD 웹실행, ENV, EXPOSE 는 이미지 캐시 사용 가능. 위로 올려도 됨.

#### 해결
```
FROM diamol/golang as builder

COPY main.go .
RUN go build -o /web/server
RUN chmod +x /web/server

# app
FROM diamol/base

CMD ["/web/server"]
ENV USER=sixeyed
EXPOSE 80

WORKDIR web
COPY --from=builder /server .
COPY index.html .



```