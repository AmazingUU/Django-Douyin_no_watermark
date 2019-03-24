import requests
import re
import json
import os


class WenkuDownloader(object):
    def __init__(self):
        self.session = requests.session()

    def fetch_url(self, url):
        return self.session.get(url).content.decode('gbk')

    def get_doc_id(self, url):
        return re.findall('view/(.*).html', url)[0]

    def parse_type(self, content):
        return re.findall(r"docType.*?\:.*?\'(.*?)\'\,", content)[0]

    def parse_title(self, content):
        return re.findall(r"title.*?\:.*?\'(.*?)\'\,", content)[0]

    def parse_doc(self, content):
        result = ''
        url_list = re.findall('(https.*?0.json.*?)\\\\x22}', content)
        url_list = [addr.replace("\\\\\\/", "/") for addr in url_list]
        for url in url_list[:-5]:
            content = self.fetch_url(url)
            y = 0
            txtlists = re.findall('"c":"(.*?)".*?"y":(.*?),', content)
            for item in txtlists:
                if not y == item[1]:
                    y = item[1]
                    n = '\n'
                else:
                    n = ''
                result += n
                result += item[0].encode('utf-8').decode('unicode_escape', 'ignore')
        return result

    def parse_txt(self, doc_id):
        content_url = 'https://wenku.baidu.com/api/doc/getdocinfo?callback=cb&doc_id=' + doc_id
        content = self.fetch_url(content_url)
        md5 = re.findall('"md5sum":"(.*?)"', content)[0]
        pn = re.findall('"totalPageNum":"(.*?)"', content)[0]
        rsign = re.findall('"rsign":"(.*?)"', content)[0]
        content_url = 'https://wkretype.bdimg.com/retype/text/' + doc_id + '?rn=' + pn + '&type=txt' + md5 + '&rsign=' + rsign
        content = json.loads(self.fetch_url(content_url))
        result = ''
        for item in content:
            for i in item['parags']:
                result += i['c'].replace('\\r', '\r').replace('\\n', '\n')
        return result

    # def parse_other(self,doc_id):
    #     content_url = "https://wenku.baidu.com/browse/getbcsurl?doc_id=" + doc_id + "&pn=1&rn=99999&type=ppt"
    #     content = self.fetch_url(content_url)
    #     url_list = re.findall('{"zoom":"(.*?)","page"', content)
    #     url_list = [item.replace("\\", '') for item in url_list]
    #     if not os.path.exists(doc_id):
    #         os.mkdir(doc_id)
    #     for index, url in enumerate(url_list):
    #         content = self.session.get(url).content
    #         path = os.path.join(doc_id, str(index) + '.jpg')
    #         with open(path, 'wb') as f:
    #             f.write(content)
    #     print("图片保存在" + doc_id + "文件夹")

    def save_file(self, filename, content):
        base_dir = os.getcwd()
        if not os.path.exists(os.path.join(base_dir, 'download')):
            os.mkdir(os.path.join(base_dir, 'download'))
        download_dir = os.path.join(base_dir, 'download')
        with open(os.path.join(download_dir, filename), 'w', encoding='utf8') as f:
            f.write(content)
            print('已保存为:' + filename)
        return os.path.join(download_dir, filename)

    # test_txt_url = 'https://wenku.baidu.com/view/cbb4af8b783e0912a3162a89.html?from=search'
    # test_ppt_url = 'https://wenku.baidu.com/view/2b7046e3f78a6529657d5376.html?from=search'
    # test_pdf_url = 'https://wenku.baidu.com/view/dd6e15c1227916888586d795.html?from=search'
    # test_xls_url = 'https://wenku.baidu.com/view/eb4a5bb7312b3169a551a481.html?from=search'
    def run(self, url):
        try:
            # url = input('请输入要下载的文库URL地址')
            content = self.fetch_url(url)
            doc_id = self.get_doc_id(url)
            type = self.parse_type(content)
            title = self.parse_title(content)
            if type == 'doc':
                result = self.parse_doc(content)
                path = self.save_file(title + '.txt', result)
                return title + '.txt', path
            elif type == 'txt':
                result = self.parse_txt(doc_id)
                path = self.save_file(title + '.txt', result)
                return title + '.txt', path
            # else:
            #     self.parse_other(doc_id)
            #     return 0
        except Exception as e:
            print('run() error:', str(e))
            return None


# if __name__ == "__main__":
#     download = Downloader()
#     download.run()
