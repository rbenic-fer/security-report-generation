import os
import scrapy

from bs4 import BeautifulSoup

SAVE_ROOT = 'data/articles/'
EXTRACT_TEXT_FILE = SAVE_ROOT + 'content.txt'
HEADERS = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'Referer':'None'
}

BASE_URLS = [
    'https://krebsonsecurity.com/',
    'https://www.mcafee.com/blogs/internet-security/',
    'https://www.mcafee.com/blogs/mobile-security/',
    'https://www.mcafee.com/blogs/family-safety/',
    'https://www.mcafee.com/blogs/privacy-identity-protection/',
    'https://www.mcafee.com/blogs/security-news/',
    'https://www.mcafee.com/blogs/tips-tricks/',
    'https://www.mcafee.com/blogs/mcafee-news/',
    'https://www.mcafee.com/blogs/other-blogs/executive-perspectives/',
    'https://www.mcafee.com/blogs/other-blogs/mcafee-labs/',
    'https://www.microsoft.com/security/blog/',
    'https://msrc-blog.microsoft.com/',
    'https://www.schneier.com/',
    'https://news.sophos.com/en-us/',
    'https://ai.sophos.com/blog/',
    'https://nakedsecurity.sophos.com/'
]
ARTICLE_SELECTOR = 'div.entry-content,div.article,div.the_content'
PARAGRAPH_SELECTOR = 'p'
READ_MORE_SELECTOR = 'a.more-link,a[data-bi-ct=\"more link\"],a[rel=bookmark],p.read-more,div.homepage-topics a'
E404_SELECTOR = 'section.no-results.not-found,div.homepage-topics:empty'


def strip_url(url):
    if url.startswith('http:'):
        url = url[5:]
    elif url.startswith('https:'):
        url = url[6:]
    return url.strip('/')

def get_root(path):
    return path.split('/')[0]

def get_domain(url):
    return get_root(strip_url(url))


class ArticlesSpider(scrapy.Spider):
    name = 'articles'
    handle_httpstatus_list = [404, 429]

    def start_requests(self):
        self.page_urls = [[] for url in BASE_URLS]
        self.is_last_page = [False for url in BASE_URLS]
        self.e429_domains = []

        for i in range(len(BASE_URLS)):
            domain = get_domain(BASE_URLS[i])
            page = 1
            while not (self.is_last_page[i] or domain in self.e429_domains):
                self.page_urls[i].append(BASE_URLS[i] + 'page/' + str(page) + '/')
                page += 1
                yield scrapy.Request(self.page_urls[i][-1], headers=HEADERS)


    def parse(self, response):
        if response.status == 429:
            self.e429_domains.append(get_domain(response.url))
            return
        elif response.status == 404 or len(response.css(E404_SELECTOR)) > 0 or len(response.css(E404_SELECTOR)) > 0:
            for i in range(len(BASE_URLS)):
                if response.url in self.page_urls[i]:
                    self.is_last_page[i] = True
            return

        path = strip_url(response.url)
        domain = get_root(path)
        if '/' not in path:
            path += '.html'

        save_file, save_file_ext = os.path.splitext(SAVE_ROOT + path)
        if save_file_ext == '':
            save_file_ext = '.html'
        while os.path.exists(save_file + save_file_ext):
            save_file_ext = '.new' + save_file_ext

        save_file += save_file_ext
        os.makedirs(os.path.dirname(save_file), exist_ok=True)
        with open(save_file, 'wb') as f:
            f.write(response.body)

        os.makedirs(os.path.dirname(EXTRACT_TEXT_FILE), exist_ok=True)
        with open(EXTRACT_TEXT_FILE, 'a') as f:
            for article in response.css(ARTICLE_SELECTOR):
                if len(article.css(READ_MORE_SELECTOR)) == 0 or domain in self.e429_domains:
                    for paragraph in article.css(PARAGRAPH_SELECTOR).getall():
                        soup = BeautifulSoup(paragraph, features='lxml')

                        text = soup.get_text()
                        if text == None:
                            continue
                        text = text.strip()
                        if len(text) == 0:
                            continue

                        print(text, end='\n\n', file=f)

                    print(file=f)

        if domain not in self.e429_domains:
            yield from response.follow_all(css=READ_MORE_SELECTOR + '::attr(href)', headers=HEADERS, callback=self.parse)
