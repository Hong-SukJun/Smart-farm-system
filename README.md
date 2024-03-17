# 스마트팜 시스템 구축
스마트팜 시스템 구축을 위하여 클라우드 서버(AWS EC2), IoT(아두이노, 라즈베리파이 카메라)를 연동하였습니다. 

IoT 센서와 클라우드 서버간 데이터 통신 및 데이터베이스 저장 시스템을 구축하였습니다. 

웹 기반의 실시간 모니터링 페이지를 제작하였습니다.

주요 기능

1. IoT 현장 센서 데이터 전송 : 현장에 설치된 IoT 기기의 센서 데이터를 클라우드 서버로 전송
- 현장에 설치된 IoT(아두이노)의 센서 데이터를 클라우드 서버로 전송합니다. 특정 시간마다 센서값을 읽고 전송합니다. 
2. 라즈베리파이 이미지 전송 : 현장에 설치된 라즈베리파이 카메라로 촬영된 이미지를 클라우드 서버로 전송 
- 라즈베리파이에 유선으로 연결된 카메라를 사용하여 현장의 작물 이미지를 특정 시간마다 촬영하여 클라우드 서버로 전송합니다. Python의 Websocket을 사용하여 클라우드 서버로 이미지를 전송합니다.
3. 클라우드 서버 : 현장 데이터 획득 서버 구현. 웹 서버 및 UI 구현
- 매일 날짜에 맞는 새로운 페이지를 생성하고, 센서 데이터와 현장 이미지를 받기 위한 서버를 구축합니다. 또한 사용자의 접속을 위한 웹 서버와 페이지 UI를 제작하였습니다.
  
---------------------------------------------

개발 과정 - [스마트팜.pptx](https://github.com/Hong-SukJun/Smart-farm-system/files/14628940/default.pptx)


---------------------------------------------

![image](https://github.com/Hong-SukJun/Smart-farm-system/assets/163775403/417c568a-6f86-4870-a985-4f12cd828024)
