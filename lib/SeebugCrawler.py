# coding=utf-8
import configparser, time, random, xlwt
from util.CaptchaHandler import CaptchaHandler
from bs4 import BeautifulSoup
from selenium import webdriver

cf = configparser.ConfigParser()
cf.read('../seebug.cfg')

browser = webdriver.Chrome(executable_path="/Users/tianwen/Downloads/chromedriver")
col_count = 0
keywords_last_ssvid = eval(cf.get('seebug', 'keywords_last_ssvid'))

# 登录
while True:
    browser.get(
        'https://sso.telnet404.com/cas/login?service=https%3A%2F%2Fwww.seebug.org%2Faccounts%2Flogin%2F%3Fnext%3D%252F')
    # 登录界面网页源代码
    con = browser.page_source
    email_input = browser.find_elements_by_name('email')[0].send_keys(cf.get('seebug', 'user'))
    passwd_input = browser.find_elements_by_name('password')[0].send_keys(cf.get('seebug', 'passwd'))

    captchaHandler = CaptchaHandler()
    code = captchaHandler.get_vcode(browser).replace(' ', '')
    print(code)
    if len(code) != 4:
        continue
    else:
        vcode_input = browser.find_elements_by_name('captcha')[0].send_keys(code)
        login_btn = browser.find_element_by_class_name('btn-lg').click()
        try:
            browser.find_element_by_class_name('form-error')
        except Exception:
            break
        else:
            continue
    break
print('登录成功')
time.sleep(5)


# 下载url
def downurl(url):
    global col_count
    print('downrul')
    browser.get(url)
    time.sleep(random.randint(8, 11))

    # 获取网页源代码
    con = browser.page_source

    # 使用beautifulsoup解析
    soup = BeautifulSoup(con, "html.parser")
    poc = soup.find('p', id='J-poc')  # poc信息
    detail = soup.find('div', id="j-md-detail")  # 漏洞详情

    if poc is not None or detail is not None:
        # 获取title
        print(soup.find("span", class_="pull-titile").text)
        sheet.write(col_count, 0, soup.find("span", class_="pull-titile").text.lstrip())

        if detail is not None:
            print(url)
            sheet.write(col_count, 1, url)
        if poc is not None:
            print(poc.text)
            # poc长度判断，长度过长无法插入到excel
            if len(poc.text) < 32767:
                sheet.write(col_count, 2, poc.text.lstrip())
            else:
                sheet.write(col_count, 2, url)
        else:
            print('do not have poc')
        col_count = col_count + 1
    else:
        print('pass')
    workbook.save('seebug.xls')




workbook = xlwt.Workbook()
keywords_list = cf.get('seebug', 'keywords_list').split(',')
for item in keywords_list:
    flag = True # 是否爬取下一页的标记
    last_vvid = ''
    col_count = 0
    sheet = workbook.add_sheet(item)
    page_num = 1
    while flag:
        # 待爬取的url
        url = 'https://www.seebug.org/search/?keywords=%s&category=&has_poc=true&page=%s&level=all' % (item, str(page_num))
        # 启动浏览器并获取网页源代码
        browser.get(url)
        time.sleep(10)
        con = browser.page_source

        # 解析网页并提取出所有的 a 标签
        soup = BeautifulSoup(con, "html.parser")
        hrefs = soup.find_all("a")

        for href in hrefs:
            try:
                if 'ssvid' in href['href']:
                    title = href['title']
                    # 记录当前组件爬取的第一个漏洞
                    print(href['href'].split('/')[-1])
                    if last_vvid == '':
                        last_vvid = href['href'].split('/')[-1]

                    # 若即将打开的url为上次爬取的最后一个url，则验证下一个组件
                    if keywords_last_ssvid[item] in href['href']:
                        keywords_last_ssvid[item] = last_vvid
                        flag = False    # 不爬取下一页
                        break   # 不爬取当前页的后续漏洞
                    crawlurl = "https://www.seebug.org%s" % (href['href'])
                    downurl(crawlurl)
            except:
                pass
        page_num = page_num + 1

    cf.set('seebug', 'keywords_last_ssvid', str(keywords_last_ssvid))
    cf.write(open('../seebug.cfg', 'w'))