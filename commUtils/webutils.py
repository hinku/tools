

import requests
from requests_ntlm import HttpNtlmAuth
from lxml import etree
from urllib import parse
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import os


class IWeb:
    name = None
    password = None

    def __init__(self, name=None, password=None):
        self.name = name
        self.password = password

    def get(self, url, xpath_match=None, **kwargs):
        """
        获取指定url页面内容，如果有xpath_match，则判断是否有匹配内容，如果没有匹配结果，则返回空
        :param url: url路径
        :param xpath_match: 需要匹配的xpath
        :param kwargs: 暂无使用
        :return: 页面内容/None
        """
        print('IWeb get impl')

    def download(self, url, filename, **kwargs):
        print('IWeb download impl')

    def set_auth_info(self, name, password):
        self.name = name
        self.password = password


class WebRequest(IWeb):
    def __init__(self):
        self.sessions = {}

    def get_response(self, url, timeout=20):
        base_url = get_base_url(url)
        session = self.sessions.get(base_url)
        # session没有有保存，需要先新建一个
        if not session:
            session = requests.Session()
            # 如果有用户名密码，则先构造鉴权信息，暂时只支持HttpNtlmAuth
            if self.name and self.password:
                session.auth = HttpNtlmAuth(self.name, self.password)

        response = session.get(url, timeout=timeout)
        if response.status_code == 200:
            self.sessions[base_url] = session

        return response

    def get(self, url, xpath_match=None, **kwargs):
        """
        获取指定url页面内容，如果有xpath_match，则判断是否有匹配内容，如果没有匹配结果，则返回空
        :param url: url路径
        :param xpath_match: 需要匹配的xpath
        :param kwargs: 暂无使用
        :return: 页面内容/None
        """
        rsp = self.get_response(url)
        # 有指定xpath时，要确认是否能匹配
        if xpath_match:
            selector = etree.HTML(rsp.text)
            el = selector.xpath(xpath_match)
            # 无匹配结果返回空
            if not el:
                return None

        return rsp.text

    def download(self, url, filename, **kwargs):
        rsp = self.get_response(url)
        try:
            rsp.raise_for_status()
            file = open(filename, 'wb')
            i = 0
            for chunk in rsp.iter_content(100000):
                file.write(chunk)
                print(i)
                i = i + 1

            file.close()
            return True
        except Exception as e:
            print(e)
            return False


class WebBrowser(IWeb):
    """

    """
    def __init__(self, show=False, drive_path=None):
        self.show = show
        if drive_path:
            self.drive_path = drive_path
        else:
            self.drive_path = os.path.join(os.getcwd(), 'chromedriver.exe')

        self.browser = self.get_browser()

    def get(self, url, xpath_match=None, **kwargs):
        self.browser.get(url)
        # 有xpath，判断是否匹配
        if xpath_match:
            elements = self.browser.find_elements_by_xpath(xpath_match)
            # 没有匹配项，则直接返回空
            if not elements:
                return None

        return self.browser.page_source

    def get_browser(self):
        options = Options()
        prefs = {
            'profile.default_content_setting.popups': 0,
            'download.default_directory': os.getcwd()
            }

        if not self.show:
            options.add_argument('headless')
            options.add_argument('--disable-gpu')

        options.add_experimental_option('prefs', prefs)
        browser = webdriver.Chrome(executable_path=self.drive_path, chrome_options=options)
        browser.implicitly_wait(10)
        return browser


class WebContent:
    page_source = None
    selector = None

    def __init__(self, content):
        self.page_source = content
        self.selector = etree.HTML(content)

    def get_xpath_text(self, xpath, first_text=True, encoding='utf-8'):
        lst = self.selector.xpath(xpath)
        if not lst:
            return None

        if first_text:
            return etree.tostring(lst[0], encoding=encoding, method='text').decode(encoding)

        texts = []
        for i in lst:
            texts.append(etree.tostring(i, encoding=encoding, method='text').decode('utf-8').decode(encoding))

        return texts


def get_url_content(url, xpath_match=None, web=None, **kwargs):
    # 如果没有指定web接口，默认使用WebRequest
    if not web:
        web = WebRequest()

    return web.get(url, xpath_match, **kwargs)


def get_base_url(url):
    """
    :param url: 原始url
    :return: 最顶层路径
    """
    url_paras = parse.urlparse(url)
    return url_paras.scheme + '://' + url_paras.netloc

