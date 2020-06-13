import os
import re
import config
import requests
import urllib.request
from bs4 import BeautifulSoup

# base url to be added as a prefix to the image src
base_url = config.url

def get_job_ad(url_array):

    # iterate each hyperlink
    for url_str in url_array:
        # Append base_url as prefix
        url = base_url + url_str

        response = requests.get(url)
        # soup object
        soup = BeautifulSoup(response.content, "html.parser")

        # filter div tag by class, then extract img tag
        images = soup.find('div', attrs={'class':'job-holder'}).find_all("img", {"alt":""})

        # iterate each image tag
        for image in images:
            # Append base_url as prefix
            image_src = base_url + image["src"]

            # replace space in url with "%20" (ASCII)
            mod_image_src = image_src.replace(" ", "%20")
            print(mod_image_src)

            # Save image
            image_cache_path = config.image_path
            
            # checking whether cache path exists, if not make non-existing intermediate directory
            if os.path.exists(image_cache_path):
                urllib.request.urlretrieve(mod_image_src,os.path.basename(image_cache_path + mod_image_src))
            else:
                os.makedirs(image_cache_path)
                urllib.request.urlretrieve(mod_image_src,os.path.basename(image_cache_path + mod_image_src))

            urllib.request.urlretrieve(mod_image_src,os.path.basename(mod_image_src))

    return "Ads saved"

def get_all_links():
    
    sub_base_url = config.sub_url

    sub_base_response = requests.get(sub_base_url)

    soup = BeautifulSoup(sub_base_response.content, "html.parser")

    # filter header containing hyperlink, then get hyperlink
    # table = soup.find('table', attrs={'class':'tbldata_2 vbfa-table'})

    ad_rows = soup.find_all('tr', attrs={'valign':'top'})
    # print(ad_rows)
    
    hyperlinks = []

    for row in ad_rows[:50]:
        # find all <a> tags from soup object (row)
        a_list = row.find_all('a', href=True)

        # select 'href from <a> tag
        hlink = [a['href'] for a in a_list if a.text]

        # extract required url using regex (start - "/employer", end - "jsp")
        # hlink is a list with duplicate urls
        req_url = re.search(r'(/employer.*jsp?)', hlink[0]).group(0)

        # Add url to hyperlinks
        hyperlinks.append(req_url)
        
    # mod_hyperlinks = [link.replace(' ', '%20') for link in words]
    return hyperlinks
    

def main():
    # print(get_job_ad("34af5f05-7e46-46d1-b7bd-53a4ec1d1c3b"))
    hyperlink_array = get_all_links()
    print(get_job_ad(hyperlink_array))

if __name__ == "__main__":
    main()