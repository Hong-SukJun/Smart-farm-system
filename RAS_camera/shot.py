from picamera import PiCamera
import time
from datetime import datetime, timedelta
import os
from ftplib import FTP_TLS
import websockets
import base64
import asyncio
from PIL import Image
import io
import shutil

server = 'farm.sc-lab.kr'
port = '8082'
RAS_NUM = 'pi2'

# 현재 시간 측정
def measuring_time():
    print("measuring time start")
    current_date = datetime.today()
    current_year = current_date.year
    current_month = current_date.month
    current_day = current_date.day
    current_hour = current_date.hour
    current_min = current_date.minute
    print("measuring time finish")
    return current_year, current_month, current_day, current_hour, current_min


# 이미지 캡처/현재 날짜, 시간으로 저장
def save_image(current_year, current_month, current_day, current_hour):
    print("save image start")
    # 저장 경로에 폴더가 있는지 확인합니다.
    if not os.path.exists('/home/{}/share/picture/{}/{}/{}'.format(RAS_NUM, current_year, current_month, current_day)):
        os.makedirs('/home/{}/share/picture/{}/{}/{}'.format(RAS_NUM, current_year, current_month, current_day))

    camera = PiCamera()
    camera.start_preview()
    camera.capture('/home/{}/share/picture/{}/{}/{}/{}_{}_{}_{}.jpg'.format(RAS_NUM, current_year, current_month, current_day, current_year, current_month, current_day, current_hour))
    camera.stop_preview()
    camera.close()  # 카메라 종료
    print("save image finish")
    

    # 7일 전 폴더 삭제
    # 7일 전의 날짜를 계산
    seven_days_ago = datetime(current_year, current_month, current_day, current_hour, current_min) - timedelta(days=7)
    # 폴더 경로에 사용되는 형식으로 변환
    seven_days_ago_year = seven_days_ago.year
    seven_days_ago_month = seven_days_ago.month
    seven_days_ago_day = seven_days_ago.day
    # 폴더가 존재한다면 삭제
    folder_path = '/home/{}/share/picture/{}/{}/{}'.format(RAS_NUM, seven_days_ago_year, seven_days_ago_month, seven_days_ago_day)
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
        print("Delete Folder :", folder_path)


# 이미지 웹소켓 전송
async def send_image_via_websocket(current_year, current_month, current_day, current_hour):
    print("websocket start")
    # 웹소켓 URL
    websocket_url = 'ws://{}:{}'.format(server, port)
    local_file = '/home/{}/share/picture/{}/{}/{}/{}_{}_{}_{}.jpg'.format(RAS_NUM, current_year, current_month, current_day, current_year, current_month, current_day, current_hour)

        # 이미지 압축
    compressed_image_base64 = compress_image(local_file, quality=50)

    # 웹소켓 연결
    async with websockets.connect(websocket_url) as ws:
        # 이미지 데이터 압축 후 전송
        await ws.send(compressed_image_base64)

    print("websocket finish")
    
# 이미지 압축 함수
def compress_image(image_path, quality):
    # 이미지 로드
    image = Image.open(image_path)

    # 이미지를 메모리 파일로 압축하여 저장
    with io.BytesIO() as output:
        image.save(output, format='JPEG', quality=quality)
        compressed_image_data = output.getvalue()

    # 압축된 이미지를 base64로 인코딩
    compressed_image_base64 = base64.b64encode(compressed_image_data).decode('utf-8')

    return compressed_image_base64

if __name__ == '__main__':
    while True:
        current_year, current_month, current_day, current_hour, current_min = measuring_time()
        # 0, 8, 16 시에 이미지 저장하도록
        if current_hour in [0, 8, 16]:
            if current_min == 52:
                save_image(current_year, current_month, current_day, current_hour)
                asyncio.get_event_loop().run_until_complete(send_image_via_websocket(current_year, current_month, current_day, current_hour))
            else:
                print('minute is not now... please wait')
        else:
            print('hour is not now... please wait')
        time.sleep(60)
