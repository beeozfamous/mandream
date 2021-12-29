import cv2
from PIL import Image
import os, sys
from tqdm import tqdm
from run import process
import numpy

"""
main.py

 How to run:
 python3 main.py

"""

# ------------------------------------------------- main()
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
def main():

    # #Read input image
    # dress = cv2.imread("chibi2.png")
    # print(dress.shape)

    # #Process
    # watermark = process(dress)

    # # Write output image
    # cv2.imwrite("chibi2_output.png", watermark)

    # #Exit
    # sys.exit()



    # path = "sweetwater/"
    # output_path = "camoncacem/"
    # dirs = os.listdir(path)
    # for item in tqdm(dirs):
    # 	print(item)
    # 	if os.path.isfile(path+item):
    # 		dress = cv2.imread(path+item)
    # 		watermark = process(dress)
    # 		cv2.imwrite(output_path+item, watermark)
    # sys.exit()

    pil_image = Image.open("egnc/sample.jpg").convert("RGBA")
    pil_image = expand2square(pil_image, (0, 0, 0, 0))
    pil_image = pil_image.resize((512,512), Image.ANTIALIAS).convert('RGB')

    open_cv_image = numpy.array(pil_image) 
    open_cv_image = open_cv_image[:, :, ::-1].copy()

    print(open_cv_image.shape)

    watermark = process(open_cv_image)

if __name__ == '__main__':
    main()