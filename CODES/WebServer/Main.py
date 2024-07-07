import requests
import time



from PIL import Image
from io import BytesIO


main_url='http://192.168.121.163/'
route_image='saved_photo'
route_status="availablity"

esp32_url='http://192.168.121.132/'
route_integers = 'data'
route_status_tell='status_tell'

def do():
    response = requests.get(main_url+route_image)
    if response.status_code == 200:
        image_data = response.content
        image = Image.open(BytesIO(image_data))

        with open("pen_img.jpg", 'wb') as file:
            file.write(image_data)

    else:
        print("Failed to retrieve the image")

def do2():
    integers_response=requests.get(esp32_url+route_integers)
    integers_data = integers_response.content
    integers_data=str(integers_data)
    integers_data=integers_data.strip('b')
    integers_data=integers_data.strip("'")
    integers_data=integers_data.split("-")
    print((integers_data))
    integers_data=[item for item in integers_data if item!=""]
    if len(integers_data) ==2:
        integer1 = float(integers_data[0])
        integer2 = int(integers_data[1])-8
        print("Received integers:", integer1, integer2)
        print("Processing image")

        import cropping
        cropping.crop(integer1,integer2/100)
        cropping.cv()
    else:
        print("Invalid data format for integers")

while True:
    check = requests.get(main_url + route_status)
    if check.status_code == 200:
        data = check.content
        if data == b'1':  
            do()
            esp_response=requests.get(esp32_url+route_status_tell)
            if esp_response.status_code == 200:
                data2= esp_response.content
                if data2 == b'2':
                    do2()


    else:
        print("Failed to retrieve server status")

    time.sleep(2)