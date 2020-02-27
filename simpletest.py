# Tested in python3
# To run on OSX:
#
#
# brew install python
# pip3 install selenium
#
#
# To run:
# python3 simpletest.py
#

import unittest
import os
import time
from PIL import Image
from io import BytesIO
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


class WebDriverPythonBasics(unittest.TestCase):
    config = []

    def setUp(self):
        self.browser = webdriver.Chrome()
        with open('config.txt', 'r') as f:
            self.config = f.read().split(',')
        directory = os.path.dirname(__file__)
        fileList = os.listdir(directory)
        for screenshot in fileList:
            if screenshot.endswith('.png'):
                os.remove(os.path.join(directory, screenshot))

    def test_saucelabs_homepage_header_displayed(self):
        self.browser.get(
            "https://www.moex.com/ru/derivatives/optionsdesk.aspx?code=SNGR-3.20&sid=2&sby=1&c1=on&c2=on&c3=on&c4=on&c5=on&c6=on&c7=on&submit=submit")
        self.browser.set_window_size(1440, 900)
        try:
            agreement = self.browser.find_element_by_xpath(
                '//*[@id="content_disclaimer"]/div/div/div/div[1]/div/a[1]')
            self.assertTrue(agreement.is_displayed())
            agreement.click()
        except Exception as e:
            print(e)

        # underline asset
        save_screenshot_byXpath(self.browser,
                                '//*[@id="mCSB_1"]',
                                'UndetlyingAsset({}).png'.format(
                                    datetime.now().strftime("%d-%m-%Y"))
                                )
        # options
        save_screenshot_byXpath(self.browser,
                                '//*[@id="mCSB_2"]',
                                'Options({})1.png'.format(
                                    datetime.now().strftime("%d-%m-%Y"))
                                )
        self.browser.execute_script(f'$("#mCSB_2").scrollLeft(15000);')
        save_screenshot_byXpath(self.browser,
                                '//*[@id="mCSB_2"]',
                                'Options({})2.png'.format(
                                    datetime.now().strftime("%d-%m-%Y"))
                                )

        for option in self.config:
            url = 'https://www.moex.com/ru/contract.aspx?code={}'.format(
                option)
            self.browser.get(url)

            screenShotName = '{}({}).png'.format(option,
                                                 datetime.now().strftime("%d-%m-%Y"))
            if os.path.exists(screenShotName):
                os.remove(screenShotName)
            # save_screenshot(self.browser, screenShotName)
            full_screenshot(self.browser, screenShotName)

            # self.browser.save_screenshot(screenShotName)

    def tearDown(self):
        self.browser.close()


def save_screenshot_byXpath(driver: webdriver.Chrome, xpath: str, path: str) -> None:
    # Ref: https://stackoverflow.com/a/52572919/
    if os.path.exists(path):
        os.remove(path)
    screenshotBytes = driver.find_element_by_xpath(xpath).screenshot_as_png
    screenshot = Image.open(BytesIO(screenshotBytes))
    screenshot.save(path)


def save_screenshot(driver: webdriver.Chrome, path: str = '/tmp/screenshot.png') -> None:
    # Ref: https://stackoverflow.com/a/52572919/
    original_size = driver.get_window_size()
    required_width = driver.execute_script(
        'return document.body.parentNode.scrollWidth')
    required_height = driver.execute_script(
        'return document.body.parentNode.scrollHeight')
    driver.set_window_size(required_width, required_height)
    # driver.save_screenshot(path)  # has scrollbar
    time.sleep(2)
    driver.find_element_by_tag_name(
        'body').screenshot(path)  # avoids scrollbar
    driver.set_window_size(original_size['width'], original_size['height'])


def full_screenshot(driver, save_path):
    # initiate value
    save_path = save_path + '.png' if save_path[-4::] != '.png' else save_path
    img_li = []  # to store image fragment
    offset = 0  # where to start

    # js to get height
    height = driver.execute_script('return Math.max('
                                   'document.documentElement.clientHeight, window.innerHeight);')

    # js to get the maximum scroll height
    # Ref--> https://stackoverflow.com/questions/17688595/finding-the-maximum-scroll-position-of-a-page
    max_window_height = driver.execute_script('return Math.max('
                                              'document.body.scrollHeight, '
                                              'document.body.offsetHeight, '
                                              'document.documentElement.clientHeight, '
                                              'document.documentElement.scrollHeight, '
                                              'document.documentElement.offsetHeight);')

    # looping from top to bottom, append to img list
    # Ref--> https://gist.github.com/fabtho/13e4a2e7cfbfde671b8fa81bbe9359fb
    while max_window_height - offset > height:

        # Scroll to height
        driver.execute_script(f'window.scrollTo(0, {offset});')
        img = Image.open(BytesIO((driver.get_screenshot_as_png())))
        img_li.append(img)
        offset += height

    # Stitch image into one
    # Set up the full screen frame
    img_frame_height = sum([img_frag.size[1] for img_frag in img_li])
    img_frame = Image.new('RGB', (img_li[0].size[0], img_frame_height))
    offset = 0
    for img_frag in img_li:
        img_frame.paste(img_frag, (0, offset))
        offset += img_frag.size[1]
    img_frame.save(save_path)


# $("#mCSB_2").scrollLeft(10000)

if __name__ == '__main__':
    unittest.main()
