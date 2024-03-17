파이썬 백그라운드 실행
sudo nohup python3 8081.py &

백그라운드 실행 목록 
ps -ef | grep py

root옆에 숫자 2개가 뜨는데, 왼쪽이 PID이다
아마 실행된 8081.py파일이 2개있는데 둘다 지워야함

sudo kill -9 {PID}



SH 백그라운드 실행 (/var/www/html에서 실행)
sudo sh loop.sh &


백그라운드에서 실행 중인 프로세스의 PID 확인
pgrep -f "sudo sh loop.sh"

sudo kill {PID}


image.html의 아마존 위치 /
index.html의 아마존 위치 /var/www/html