# Reference : https://blog.csdn.net/qq_34687559/article/details/106340929

import os
import time
import requests
from tqdm import tqdm
from selenium import webdriver

Google_URL = \
    "https://www.google.com.hk/search?q={q}&tbm=isch"


class Kun_Crawler:
    '''
    Crawler for retriving data for the dataset use to train the Kun Classifier

    '''

    def __init__(self):
        '''
        Initliazing the class
        '''
        self.query_keyword = input('I want this image: ')
        self.num_images = input('I want these amount of images: ')
        self.url = Google_URL.format(q=self.query_keyword)

    def browser_init(self):
        '''
        Initialize the browser use to fetch the images
        :return: brower instance
        '''
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument("--headless")
        browser = webdriver.Chrome(options=chrome_options)
        browser.get(self.url)
        browser.maximize_window()
        return browser

    def download_images(self, browser, round=100, num_images=100):
        '''

        :param browser: browswer instance
        :param round: number of time to scroll the pages
        :param num_images: number of images to retrieve (the final number might be less than this depends on the image availble in google)
        '''
        if not os.path.exists(self.query_keyword):
            os.mkdir(self.query_keyword)

        unique_image_urls = list()

        pos = 0
        imgs_count = 1056
        pos_offset = 500
        url_length_bound = 200

        for i in tqdm(range(round)):

            pos += pos_offset
            js = 'var q=document.documentElement.scrollTop=' + str(pos)
            browser.execute_script(js)
            time.sleep(0.01)

            img_elements = browser.find_elements_by_tag_name('img')

            for img_element in img_elements:
                img_url = img_element.get_attribute('src')

                if isinstance(img_url, str):
                    if len(img_url) <= url_length_bound:
                        if 'images' in img_url:
                            if img_url not in unique_image_urls:
                                try:
                                    if imgs_count >= num_images:
                                        break
                                    unique_image_urls.append(img_url)
                                    filename = "./{s}/".format(s=self.query_keyword) + \
                                        str(imgs_count) + ".jpeg"
                                    r = requests.get(img_url)

                                    with open(filename, 'wb') as f:
                                        f.write(r.content)
                                    f.close()

                                    imgs_count += 1
                                    print(imgs_count)
                                    time.sleep(0.01)
                                except:
                                    continue

    def run(self):
        '''
        run the crawler
        '''
        browser = self.browser_init()
        self.download_images(browser,2000, 50000)
        browser.close()


if __name__ == '__main__':
    kun = Kun_Crawler()
    kun.run()


