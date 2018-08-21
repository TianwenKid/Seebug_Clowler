from PIL import Image
from aip import AipOcr
import configparser


class CaptchaHandler:

    def __init__(self):
        cf = configparser.ConfigParser()
        cf.read('../seebug.cfg')

        # 百度AI平台 APPID AK SK
        APP_ID = cf.get('baidu-ai', 'APP_ID')
        API_KEY = cf.get('baidu-ai', 'API_KEY')
        SECRET_KEY = cf.get('baidu-ai', 'SECRET_KEY')
        self.client = AipOcr(APP_ID, API_KEY, SECRET_KEY)



    # 读取图片
    def __get_file_content(self, filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()

    # 获取验证码
    def get_vcode(self, broweser):
        self.__screenshot(broweser)
        image = self.__get_file_content('../code.png')
        result = self.client.basicGeneral(image)
        try:
            return result['words_result'][0]['words']
        except Exception:
            return ''

    # 截图
    def __screenshot(self, browser):
        # 获取截图
        browser.get_screenshot_as_file('../screenshot.png')

        # 获取指定元素位置
        element = browser.find_element_by_class_name('captcha')
        left = 1810
        top = 910
        right = int(left + element.size['width'] + 100)
        bottom = int(top + element.size['height'] + 30)

        # 通过Image处理图像
        im = Image.open('../screenshot.png')
        im = im.crop((left, top, right, bottom))
        im.save('../code.png')
