import urllib.parse
import urllib.request
import re
from bs4 import BeautifulSoup


def url_validation(url):
    """
    Return url validation

    :param url: url
    :return: re.match(url)
    """
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    return regex.match(url)


def lookup_id(fb_url):
    """
    Return id by using lookup_id

    :param fb_url: facebook url
    :return: id
    """
    if url_validation(fb_url) is None:
        return None

    details = urllib.parse.urlencode({'fburl': fb_url, 'check': 'Lookup'})
    details = details.encode('UTF-8')
    url = urllib.request.Request('https://lookup-id.com', details)
    url.add_header("User-Agent",
                   "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.29 Safari/525.13")
    response_data = urllib.request.urlopen(url).read().decode("utf-8")

    soup = BeautifulSoup(response_data, "lxml")
    soup = soup.find(id='code')

    if soup is not None:
        return soup.get_text()

    return None
