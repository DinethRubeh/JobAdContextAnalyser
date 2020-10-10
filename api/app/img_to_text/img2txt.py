import os
import re
import json

import pytesseract
import pandas as pd
from PIL import Image
from glob import glob

import config
from app.text_context.job_context import text_pre_process

# tesseract.exe path
pytesseract.pytesseract.tesseract_cmd = config.tess_path

# text details cache path
details_cache_path = config.ad_details_path

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
    text_from_image = None
    try:
        image = Image.open(path)
        # pre-processed image
        prep_image = image_prep(image)
        # convert prep image to text
        # page segmentation mode 6 -> single uniform block of text (row by row)
        text = pytesseract.image_to_string(prep_image, config='--psm 6')
        text_from_image = text
    except Exception as e:
        print(e)
        text_from_image = "None"

    return text_from_image

# get text of all ads
def ads2text():

    all_images = []

    # load all images
    for e in ['*.png', '*.jpg', '*.gif']:
        all_images.extend(glob(config.image_path + e))
    
    # to add description etc. info
    text_dict = []

    # iterate and convert image to text 
    for image_path in all_images:
        # get ref number from image_path string (\d -> digits)
        ref_num = re.findall(r'(\d+)',image_path)[0]
        # remove 0000 part
        refn = re.sub("0000","",ref_num)

        # get job position
        vacancy = vacancy_dict[refn]
        # get text description from image
        desc = image2text(image_path)
        # text pre-processing
        mod_desc = text_pre_process(desc)
        print(vacancy)
        # add to text_dict
        text_dict.append({
            "ref_number":refn,
            "position": vacancy,
            "description": mod_desc
        })

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
    
    return "job description cached from images"

# add description to job details and store seperately
def job_wth_description():

    # details_json = open(details_cache_path + 'details.json', encoding="utf8")
    # load test data
    details_json = pd.read_json(details_cache_path + 'details.json', orient='records')

    merged_job_details = pd.merge(job_details_df,details_json, on='ref_number', how='left')

    merged_job_details.drop(['ad_img', 'position'], axis=1, inplace=True)

    # save dataframe
    merged_job_details.to_csv(details_cache_path + 'job_full_details.csv', index = False)

    return "job description details cached"
    

def main():
    # req_dict = ads2text()
    print(job_wth_description())

if __name__ == "__main__":
    main()

# import time
# start_time = time.time()
# print(ads2text())
# print((time.time() - start_time))
