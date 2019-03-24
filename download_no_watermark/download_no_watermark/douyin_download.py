"""
感谢AppSign提供加签服务
github地址：https://github.com/AppSign/douyin
"""
import os
import re
import sys

import requests


class DouyinDownloader(object):
    def __init__(self):
        self.headers = {
            "User-Agent": "Aweme/2.8.0 (iPhone; iOS 11.0; Scale/2.00)"
        }

    def run(self, share_url):
        try:
            # post_data = {}
            # share_url = input('请输入分享链接:').strip()
            # post_data['aweme_id'] = get_aweme_id('http://v.douyin.com/RW45XF/')

            # post_data['aweme_id'] = self.get_aweme_id(share_url.strip())
            aweme_id = self.get_aweme_id(share_url.strip())

            # 20190324
            # 以下注释部分为原抖音加签服务代码，现已不可用
            # 故换了另一个加签服务，现网站已恢复正常
            # device_info = self.get_device('https://api.appsign.vip:2688/douyin/device/new/version/2.7.0')
            # token = self.get_token('https://api.appsign.vip:2688/token/douyin/version/2.7.0')
            # app_info = self.get_app_info()
            # params = self.get_params(device_info, app_info)
            # query = self.params2str(params)
            # sign = self.get_sign(token, query)
            # params.update(sign)  # url参数中拼接签名

            # 'url': 'https://aweme.snssdk.com/aweme/v1/aweme/detail/?aweme_id=6671138623359814916&' + params2str(feed_params)

            feed_params = self.get_feed_params()
            form_data = {
                # 'url': 'https://aweme.snssdk.com/aweme/v1/feed/?' + self.params2str(feed_params)
                'url': 'https://aweme.snssdk.com/aweme/v1/aweme/detail/?aweme_id=' + aweme_id + '&' + self.params2str(feed_params)
            }
            print('未带加密参数url:', form_data)
            detail_url = self.get_sign_url(form_data)
            if not detail_url:
                print('get sign fail')
                sys.exit()
            print('带有加密参数的完整url:', detail_url)

            # resp = requests.post("https://aweme.snssdk.com/aweme/v1/aweme/detail/", params=params, data=post_data,
            #                      headers=self.headers).json()
            resp = requests.get(detail_url,headers=self.headers).json()
            download_url = resp['aweme_detail']['video']['play_addr']['url_list'][0]
            desc = resp['aweme_detail']['desc']
            # r = requests.get(download_url)
            # with open('test.mp4', 'wb') as f:
            #     f.write(r.content)
            return self.download(desc,download_url)
            # return download_url, desc
        except Exception as e:
            print('download Expection:', e)
            return None

    def get_feed_params(self):
        params = {
            'app_type': 'normal',
            'manifest_version_code': '321',
            '_rticket': '1541682949911',
            'ac': 'wifi',
            'device_id': '59121099964',
            # 'device_id':device_info['device_id'],
            'iid': '50416179430',
            # 'iid':device_info['iid'],
            'os_version': '8.1.0',
            'channel': 'gray_3306',
            'version_code': '330',
            'device_type': 'ONEPLUS%20A5000',
            'language': 'zh',
            # 'uuid':device_info['uuid'],
            'resolution': '1080*1920',
            # 'openudid':device_info['openudid'],
            # 'vid':'C2DD3A72-18E8-490e-B58A-86AD20BB8035',
            'openudid': '27b34f50ff0ba8e26c5747b59bd6d160fbdff384',
            'update_version_code': '3216',
            'app_name': 'aweme',
            'version_name': '3.3.0',
            'os_api': '27',
            'device_brand': 'OnePlus',
            'ssmix': 'a',
            'device_platform': 'android',
            'dpi': '420',
            'aid': '1128',
            'count': '6',
            'type': '0',
            'max_cursor': '0',
            'min_cursor': '-1',
            # 'volume':'0.06',
            'pull_type': '2',
        }
        return params

    def params2str(self,params):  # 参数转化成url中需要拼接的字符串
        query = ''
        for k, v in params.items():
            query += '%s=%s&' % (k, v)
        query = query.strip('&')
        return query


    def get_sign_url(self,form_data): # 获取带有加密参数的url
        headers = {
            "User-Agent": "Aweme/2.8.0 (iPhone; iOS 11.0; Scale/2.00)",
        }
        # proxies = {
        #     'http': 'http://123.160.227.54:23328'
        # }
        try:
            # sign_url = requests.post('http://jokeai.zongcaihao.com/douyin/v292/sign',proxies=proxies,data=form_data,headers=headers).json()['url']
            # 根据开源项目获取加密参数，要求提供加密之前的url
            sign_url = \
                requests.post('http://jokeai.zongcaihao.com/douyin/v292/sign',data=form_data, headers=headers).json()[
                    'url']
        except Exception as e:
            sign_url = None
            print('get_sign_url() error:', str(e))
        return sign_url

    def download(self,filename, url):  # 下载视频
        headers = {
            "User-Agent": "Aweme/2.8.0 (iPhone; iOS 11.0; Scale/2.00)"
        }
        # 请求视频播放地址，二进制流保存到本地
        response = requests.get(url, headers=headers)
        chunk_size = 1024  # 切分视频流，一次保存视频流大小为1M，当读取到1M时保存到文件一次
        content_size = int(response.headers['content-length'])  # 视频流总大小
        if response.status_code == 200:
            print(filename + '\n文件大小:%0.2f MB' % (content_size / chunk_size / 1024))
            base_dir = os.getcwd()
            download_dir = os.path.join(base_dir, 'download')
            if not os.path.exists(download_dir):
                os.mkdir(download_dir)
            file_path = os.path.join(download_dir, filename)
            size = 0
            if not os.path.exists(file_path):
                with open(file_path + '.mp4', 'wb') as f:
                    for stream in response.iter_content(chunk_size=chunk_size):  # 切分视频流
                        f.write(stream)
                        size += len(stream)
                        f.flush()  # 一次write后需要flush
                        # '\r'使每一次print会覆盖前一个print信息，end=''使print不换行，如果全部保存完，print再换行
                        # 实现下载进度实时刷新，当保存到100%时，打印下一行
                        print('下载进度:%.2f%%' % float(size / content_size * 100) + '\r',
                              end='' if (size / content_size) != 1 else '\n')
                return filename + '.mp4',file_path + '.mp4'

    # 以下注释部分为原抖音加签服务代码，现已不可用

    # def get_device(self, url):  # 获取设备信息
    #     r = requests.get(url).json()
    #     device_info = r['data']
    #     return device_info
    #
    # def get_token(self, url):  # 获取token信息
    #     r = requests.get(url).json()
    #     token = r['token']
    #     return token
    #
    # def get_app_info(self):  # 初始化app信息
    #     app_info = {
    #         'version_code': '2.7.0',
    #         'aid': '1128',
    #         'app_name': 'aweme',
    #         'build_number': '27014',
    #         'app_version': '2.7.0',
    #         'channel': 'App%20Stroe',
    #     }
    #     return app_info
    #
    # def get_params(self, device_info, app_info):  # 拼接接口url中需要的参数
    #     params = {
    #         'iid': device_info['iid'],
    #         'idfa': device_info['idfa'],
    #         'device_type': device_info['device_type'],
    #         'version_code': app_info['version_code'],
    #         'aid': app_info['aid'],
    #         'os_version': device_info['os_version'],
    #         'screen_width': device_info['screen_width'],
    #         'pass-region': 1,
    #         'vid': device_info['vid'],
    #         'device_id': device_info['device_id'],
    #         'os_api': device_info['os_api'],
    #         'app_name': app_info['app_name'],
    #         'build_number': app_info['build_number'],
    #         'device_platform': device_info['device_platform'],
    #         'js_sdk_version': '2.7.0.1',
    #         'app_version': app_info['app_version'],
    #         'ac': 'mobile',
    #         'openudid': device_info['openudid'],
    #         'channel': app_info['channel']
    #     }
    #     return params
    #
    # def params2str(self, params):  # 参数转化成url中需要拼接的字符串
    #     query = ''
    #     for k, v in params.items():
    #         query += '%s=%s&' % (k, v)
    #     query = query.strip('&')
    #     return query
    #
    # def get_sign(self, token, query):  # 调用接口获取签名
    #     r = requests.post('https://api.appsign.vip:2688/sign', json={'token': token, 'query': query}).json()
    #     if r['success']:
    #         sign = r['data']
    #     else:
    #         sign = r['success']
    #     return sign
    #
    def get_aweme_id(self, share_url):  # 调用接口，根据share_url获取aweme_id
        # 真实url为headers里的Location，禁止重定向，才能获取
        r = requests.get(share_url, headers=self.headers, allow_redirects=False)
        url = r.headers['Location']
        aweme_id = re.search(r'\d+', url).group()
        return aweme_id

# if __name__ == '__main__':
#     downloader = DouyinDownloader()
#     download_url, desc = downloader.run('http://v.douyin.com/Rv7Jqn/')
#     print(desc)
#     print(download_url)
