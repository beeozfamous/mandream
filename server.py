import firebase_admin
from firebase_admin import db
from firebase_admin import credentials
from firebase_admin import storage
import cv2
from PIL import Image
from run import process
import datetime
import requests
import numpy


def expand2square(pil_img, background_color):
    width, height = pil_img.size
    if width == height:
        return pil_img
    elif width > height:
        result = Image.new(pil_img.mode, (width, width), background_color)
        result.paste(pil_img, (0, (width - height) // 2))
        return result
    else:
        result = Image.new(pil_img.mode, (height, height), background_color)
        result.paste(pil_img, ((height - width) // 2, 0))
        return result

def listener(event):
    #time.sleep(1)
    if ("wanna_nude_queue" in event.path and event.data['process_Flag']==False):
        print(event.data)
        an_unnude=str(event.path).rsplit('/', 1)[-1]
        new_unnude_path="unnude/"+an_unnude
        #blob = bucket.blob(new_unnude_path)
        #download_path=blob.generate_signed_url(datetime.timedelta(seconds=300), method='GET')

        download_path=event.data['image_url']


        img_data = requests.get(download_path).content
        print("Download: ",new_unnude_path)
        with open(new_unnude_path, 'wb') as handler:
            handler.write(img_data)
        print("Download finished: ",new_unnude_path)

        print("Start undressing my baby: ",new_unnude_path)

        pil_image = Image.open(new_unnude_path).convert("RGBA")
        pil_image = expand2square(pil_image, (0, 0, 0, 0))
        pil_image = pil_image.resize((512,512), Image.ANTIALIAS).convert('RGB')

        open_cv_image = numpy.array(pil_image) 
        open_cv_image = open_cv_image[:, :, ::-1].copy() 

        watermark = process(open_cv_image)

        print("Seeing you naked for the last time: ",new_unnude_path)

        new_nude_path="nude/"+an_unnude+".png"
        im_ready=cv2.imwrite(new_nude_path, watermark)

        print("And now let her go: ",new_nude_path)

        if  im_ready:
            im_ready=False
            blob = bucket.blob(new_nude_path)
            with open(new_nude_path, 'rb') as my_file:
                blob.upload_from_file(my_file)
            im_ready=True


            if im_ready:
                blob = bucket.blob(new_nude_path)
                download_path = blob.generate_signed_url(datetime.timedelta(seconds=500), method='GET')

                db.reference().child(str("wanna_nude_queue")).child(str(an_unnude)).update({
                    'process_Flag': 'true',
                    'image_url': str(download_path),
                })
                print("Bye bye: ",new_nude_path)

cred_object = credentials.Certificate("/home/dev-fti/khang/nguyen/deepnude_official/everyonewillbenaked-firebase-adminsdk-mftjs-2eb3221f56.json")
default_app = firebase_admin.initialize_app(cred_object, {
    'databaseURL': 'https://everyonewillbenaked-default-rtdb.asia-southeast1.firebasedatabase.app/',
     'storageBucket': 'everyonewillbenaked.appspot.com'
})
bucket = storage.bucket()

firebase_admin.db.reference('/').listen(listener)