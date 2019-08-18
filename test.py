from commUtils.webutils import WebBrowser
from commUtils.webutils import IWeb
from commUtils.webutils import WebRequest
from commUtils.webutils import WebContent
from commUtils import webutils

def get(url, web):
    """

    :param url:
    :param web:
    :return:
    """
    return web.get(url)


if __name__ == '__main__':
    print('test')
    c = webutils.get_url_content('http://www.baidu.com', web=WebBrowser())
    wc = WebContent(c)
    print(wc.get_xpath_text('//*[@id="cp"]', ))
