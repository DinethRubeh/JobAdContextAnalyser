import os
import re
import json
import config
import pytesseract
import pandas as pd
from PIL import Image
from glob import glob

# tesseract.exe path
pytesseract.pytesseract.tesseract_cmd = config.tess_path

# load job_details csv
job_details_df = pd.read_csv(config.ad_details_path + 'job_details.csv')

# create ref_number to vacancy dict from job_details_df
vacancy_dict = dict(zip(job_details_df['ref_number'].astype(str), job_details_df['vacancy']))

# image pre-processing to improve accuracy
def image_prep(img_obj):
    ''' To-do: test and apply suitable pre-processing techniques using cv2
        noise removal, thresholding, dilation, erosion, opening, canny_edge etc.
        https://nanonets.com/blog/ocr-with-tesseract/#preprocessingfortesseract?&utm_source=nanonets.com/blog/&utm_medium=blog&utm_content=%5BTutorial%5D%20OCR%20in%20Python%20with%20Tesseract,%20OpenCV%20and%20Pytesseract
    '''
    # converts to grayscale image
    return img_obj.convert('L') 

# image to text using pytesseract
def image2text(path):

    image = Image.open(path)
    # pre-processed image
    prep_image = image_prep(image)
    # convert prep image to text
    # page segmentation mode 6 -> single uniform block of text (row by row)
    text = pytesseract.image_to_string(prep_image, config='--psm 6')
    
    return text

# get text of all ads
def ads2text():

    all_images = []

    # load all images
    for e in ['*.png', '*.jpg', '*.gif']:
        all_images.extend(glob(config.image_path + e)[:5])
    
    text_dict = []
    # iterate and convert image to text 
    for image_path in all_images:
        # get ref number from image_path string (\d -> digits)
        ref_num = re.findall(r'(\d+)',image_path)[0]
        # remove 0000 part
        refn = re.sub("0000","",ref_num)

        # get job position
        vacancy = vacancy_dict[refn]

        # add to text_dict
        text_dict.append({
            "position": vacancy,
            "description": image2text(image_path)
        })

    # text details cache path
    details_cache_path = config.ad_details_path

    # checking whether cache path exists
    if os.path.exists(details_cache_path):
        # jsonify and save json
        with open(details_cache_path + 'details.json', 'w', encoding='utf-8') as f:
            json.dump(text_dict, f, ensure_ascii=False, indent=4)
    else:
        # make non-existing intermediate directory
        os.makedirs(details_cache_path)
        with open(details_cache_path + 'details.json', 'w', encoding='utf-8') as f:
            json.dump(text_dict, f, ensure_ascii=False, indent=4)

    return "text details saved"

def main():
    print(ads2text())

if __name__ == "__main__":
    main()

# import time
# start_time = time.time()
# print(ads2text())
# print((time.time() - start_time))
