import asyncio
import websockets
import base64
import os
import time
import shutil
import subprocess
from PIL import Image
import io
import zipfile

RAS_NUM = 'A'
port = 8081

async def handle_websocket(websocket, path):
    # 이미지 파일 받기
    while True:
        message = await websocket.recv()
        image_base64 = message
        image_data = bytes(base64.b64decode(image_base64))
        
        # 이미지 회전
        image = Image.open(io.BytesIO(image_data))
        rotated_image = image.rotate(90, expand=True)  # 이미지 회전, expand=True로 설정하여 이미지 크기 조정 가능
        
        # 이미지 크기 조정
        resized_image = rotated_image.resize((480, 720))
        
        # 날짜 별 이미지 저장
        current_time = time.strftime("%Y/%m/%d")
        yesterday = time.strftime("/%Y/%m/%d", time.localtime(time.time() - 86400))
        tomorrow = time.strftime("/%Y/%m/%d", time.localtime(time.time() + 86400))
        directory = os.path.join('/var/www/html/', current_time)
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        image_name_day = time.strftime("%Y_%m_%d")
        image_name_time = time.strftime("%Y_%m_%d_%H")
        
        with open(os.path.join(directory, '{}_{}.jpg'.format(RAS_NUM, image_name_time)), 'wb') as file:
            resized_image.save(file, 'JPEG')
        
        # 모든 이미지 저장
        ALL_Backup = os.path.join('/var/www/html/picture/', current_time)
        if not os.path.exists(ALL_Backup):
            os.makedirs(ALL_Backup)
        
        image_name_time2 = time.strftime("%Y_%m_%d_%H")
        with open(os.path.join(ALL_Backup, '{}_{}.jpg'.format(RAS_NUM, image_name_time2)), 'wb') as file:
            resized_image.save(file, 'JPEG')
        
        print('finish save')
        make_webcode(directory, image_name_time, yesterday, tomorrow, image_name_day, current_time)
        print('waiting client ... ')
        return directory, image_name_time, yesterday, tomorrow, image_name_day, current_time



def make_webcode(directory, image_name_time, yesterday, tomorrow, image_name_day, current_time):
    print('path : ' + directory)
    print('image name : ' + image_name_time)
    print("Make Today's DB Page")
    
    # conn.php 파일이 존재하지 않을 경우에만 복사 실행
    if not os.path.exists("{}/conn.php".format(directory)):
        zip_file = "copy.zip" 
        # zip 파일 복사
        shutil.copy(zip_file, "{}/{}".format(directory, zip_file))

        # 압축 풀기
        with zipfile.ZipFile("{}/{}".format(directory, zip_file), "r") as zip_ref:
            zip_ref.extractall(directory)

        # zip 파일 삭제
        os.remove("{}/{}".format(directory, zip_file))

    # index.php 코드 추가 . 저장된 이미지 불러오기
    if not os.path.exists("{}/index.html".format(directory)):
        print("directory : ", directory)
        print("image_name_time : ", image_name_time)
        print("image_name_day : ", image_name_day)
        print("current_time : ", current_time)
        shutil.copy("index.html", "{}/index.html".format(directory))
        with open("{}/index.html".format(directory), "a") as f:
            f.write('    <div class="btn_section layout_padding pt-0">\n')
            f.write('        <div class="container">\n')
            f.write('            <table id="image-table">\n')
            f.write('                <tr> <td colspan="3" class="p-1">&nbsp; A</td> </tr>\n')
            f.write('                <tr> <td> <img class="table-img"    src="https://farm.sc-lab.kr/{}/A_{}_08.jpg" alt="Image 1" onerror="this.src=\'error.jpg\'"> </td> \n'.format(current_time, image_name_day))
            f.write('                    <td> <img class="table-img"     src="https://farm.sc-lab.kr/{}/A_{}_12.jpg" alt="Image 2" onerror="this.src=\'error.jpg\'"> </td> \n'.format(current_time, image_name_day))
            f.write('                    <td> <img class="table-img"     src="https://farm.sc-lab.kr/{}/A_{}_16.jpg" alt="Image 3" onerror="this.src=\'error.jpg\'"> </td></tr>\n'.format(current_time, image_name_day))
            f.write('                <tr> <td colspan="3" class="p-1">&nbsp; B</td> </tr>\n')
            f.write('                <tr> <td> <img class="table-img"    src="https://farm.sc-lab.kr/{}/B_{}_08.jpg" alt="Image 1" onerror="this.src=\'error.jpg\'"> </td> \n'.format(current_time, image_name_day))
            f.write('                    <td> <img class="table-img"     src="https://farm.sc-lab.kr/{}/B_{}_12.jpg" alt="Image 2" onerror="this.src=\'error.jpg\'"> </td> \n'.format(current_time, image_name_day))
            f.write('                    <td> <img class="table-img"     src="https://farm.sc-lab.kr/{}/B_{}_16.jpg" alt="Image 3" onerror="this.src=\'error.jpg\'"> </td></tr>\n'.format(current_time, image_name_day))
            f.write('                <tr> <td colspan="3" class="p-1">&nbsp; C</td> </tr>\n')
            f.write('                <tr> <td> <img class="table-img"    src="https://farm.sc-lab.kr/{}/C_{}_08.jpg" alt="Image 1" onerror="this.src=\'error.jpg\'"> </td> \n'.format(current_time, image_name_day))
            f.write('                    <td> <img class="table-img"     src="https://farm.sc-lab.kr/{}/C_{}_12.jpg" alt="Image 2" onerror="this.src=\'error.jpg\'"> </td> \n'.format(current_time, image_name_day))
            f.write('                    <td> <img class="table-img"     src="https://farm.sc-lab.kr/{}/C_{}_16.jpg" alt="Image 3" onerror="this.src=\'error.jpg\'"> </td></tr>\n'.format(current_time, image_name_day))
            f.write('                <tr> <td colspan="3" class="p-1">&nbsp; D</td> </tr>\n')
            f.write('                <tr> <td> <img class="table-img"    src="https://farm.sc-lab.kr/{}/D_{}_08.jpg" alt="Image 1" onerror="this.src=\'error.jpg\'"> </td> \n'.format(current_time, image_name_day))
            f.write('                    <td> <img class="table-img"     src="https://farm.sc-lab.kr/{}/D_{}_12.jpg" alt="Image 2" onerror="this.src=\'error.jpg\'"> </td> \n'.format(current_time, image_name_day))
            f.write('                    <td> <img class="table-img"     src="https://farm.sc-lab.kr/{}/D_{}_16.jpg" alt="Image 3" onerror="this.src=\'error.jpg\'"> </td></tr>\n'.format(current_time, image_name_day))
            f.write('            </table>\n')
            f.write('        </div>\n')
            f.write('    </div>\n')
            f.write('</body>\n')
            f.write('</html>\n')
                    
    
    #DB 권한 777 부여
    subprocess.run(["chmod", "777", "-R", "{}".format(directory)])

async def main():
    # 웹 소켓 서버 시작
    server = await websockets.serve(handle_websocket, '', port)
    # 서버 대기
    await server.wait_closed()
    

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())