import os
import re
import config
import requests
import pandas as pd
import urllib.request
from bs4 import BeautifulSoup

# base url to be added as a prefix to the image src
base_url = config.url
# images dir path
image_cache_path = config.image_path
# details dir path
details_cache_path = config.ad_details_path

def get_job_ad(url_df_row):

    img_name = None

    # get hyperlink of ad
    url = url_df_row.ad_url
    # get ref number of ad
    ad_ref = url_df_row.ref_number

    response = requests.get(url)
    # soup object
    soup = BeautifulSoup(response.content, "html.parser")

    # filter div tag by class, then extract img tag
    images = soup.find('div', attrs={'class':'job-holder'}).find_all("img", {"alt":""})

    # get image src
    image_src = [image["src"] for image in images]
    
    # if no ad image is available
    if not image_src:
        img_name = "no_image"
    else:
        # image src with base url
        base_image_src = base_url + image_src[0]

        # replace space in url with "%20" (ASCII)
        mod_image_src = base_image_src.replace(" ", "%20")
        
        # create image name (ref number + image type)
        # get image type from url
        img_name = ad_ref + '.' + mod_image_src.rsplit('.', 1)[-1]

        # images directory
        image_cache_path = config.image_path
        
        # get image from url
        img_request = requests.get(mod_image_src)

        if img_request.status_code == 200:
            # checking whether cache path exists
            if os.path.exists(image_cache_path):
                # save image (wb - write binary permission)
                with open(image_cache_path + img_name, 'wb') as fimage:
                    fimage.write(img_request.content)
            # if not make non-existing intermediate directory
            else:
                os.makedirs(image_cache_path)
                with open(image_cache_path + img_name, 'wb') as fimage:
                    fimage.write(img_request.content)

    return img_name

def get_general_details():
    
    sub_base_url = config.sub_url
    # response
    sub_base_response = requests.get(sub_base_url)
    # create a soup object
    soup = BeautifulSoup(sub_base_response.content, "html.parser")

    # this <tr> tag with given attrs corresponds to ad rows
    ad_rows = soup.find_all('tr', attrs={'valign':'top'})
    
    job_details = []

    hyperlinks = []

    for row in ad_rows[:10]:
        # find all <h1> tags from soup object (row)
        company_name = [name.text for name in row.find_all('h1')]

        # job ref number <span> tag with id = 'hdnJC...'
        ref_num = [num.text for num in row.find_all('span', attrs={'id':re.compile(r'hdnJC')})]

        # find all <a> tags
        a_list = row.find_all('a', href=True) # find_all(['a', 'h1'])

        hlink, vacancy = [], []
        # select 'href' and text from <a> tag
        for a in a_list:
            if a.text:
                # hyperlink of ad
                hlink.append(a['href'])
                # job position
                vacancy.append(a.text)
        # hlink = [a['href'] for a in a_list if a.text]

        # extract required url using regex (start - "/employer", end - "jsp")
        # hlink is a list with duplicate urls
        req_url = re.search(r'(/employer.*jsp?)', hlink[0]).group(0)

        # Add url to hyperlinks
        hyperlinks.append(req_url)

        # Add information to job_details
        job_details.append({
            "company":company_name[0],
            "vacancy":vacancy[0],
            "ref_number":ref_num[0],
            "ad_url":base_url + req_url})

    job_details_df = pd.DataFrame(job_details)

    return job_details_df
    
def save_general_details(job_details_df):

    # Save ad image & add image name to df
    job_details_df['ad_img'] = job_details_df.apply(get_job_ad, axis=1)
    
    # checking whether cache path exists
    if os.path.exists(details_cache_path):
        # save dataframe
        job_details_df.to_csv(details_cache_path + 'job_details.csv', index = False)
    # if not make non-existing intermediate directory
    else:
        os.makedirs(details_cache_path)
        job_details_df.to_csv(details_cache_path + 'job_details.csv', index = False)

    return "job details cached"


def main():
    jobs_df = get_general_details()
    print(save_general_details(jobs_df))

if __name__ == "__main__":
    main()