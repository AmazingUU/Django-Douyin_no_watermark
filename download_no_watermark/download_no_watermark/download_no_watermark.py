"""
感谢AppSign提供加签服务
github地址：https://github.com/AppSign/douyin
"""
import re

import requests


class Downloader(object):
    def __init__(self):
        self.headers = {
            "User-Agent": "Aweme/2.8.0 (iPhone; iOS 11.0; Scale/2.00)"
        }

    def run(self, share_url):
        try:
            post_data = {}
            # share_url = input('请输入分享链接:').strip()
            # post_data['aweme_id'] = get_aweme_id('http://v.douyin.com/RW45XF/')
            post_data['aweme_id'] = self.get_aweme_id(share_url.strip())
            device_info = self.get_device('https://api.appsign.vip:2688/douyin/device/new/version/2.7.0')
            token = self.get_token('https://api.appsign.vip:2688/token/douyin/version/2.7.0')
            app_info = self.get_app_info()
            params = self.get_params(device_info, app_info)
            query = self.params2str(params)
            sign = self.get_sign(token, query)
            params.update(sign)  # url参数中拼接签名

            resp = requests.post("https://aweme.snssdk.com/aweme/v1/aweme/detail/", params=params, data=post_data,
                                 headers=self.headers).json()
            download_url = resp['aweme_detail']['video']['play_addr']['url_list'][0]
            desc = resp['aweme_detail']['desc']
            # r = requests.get(download_url)
            # with open('test.mp4', 'wb') as f:
            #     f.write(r.content)
            return download_url, desc
        except Exception as e:
            print('download Expection:', e)
            return None

    def get_device(self, url):  # 获取设备信息
        r = requests.get(url).json()
        device_info = r['data']
        return device_info

    def get_token(self, url):  # 获取token信息
        r = requests.get(url).json()
        token = r['token']
        return token

    def get_app_info(self):  # 初始化app信息
        app_info = {
            'version_code': '2.7.0',
            'aid': '1128',
            'app_name': 'aweme',
            'build_number': '27014',
            'app_version': '2.7.0',
            'channel': 'App%20Stroe',
        }
        return app_info

    def get_params(self, device_info, app_info):  # 拼接接口url中需要的参数
        params = {
            'iid': device_info['iid'],
            'idfa': device_info['idfa'],
            'device_type': device_info['device_type'],
            'version_code': app_info['version_code'],
            'aid': app_info['aid'],
            'os_version': device_info['os_version'],
            'screen_width': device_info['screen_width'],
            'pass-region': 1,
            'vid': device_info['vid'],
            'device_id': device_info['device_id'],
            'os_api': device_info['os_api'],
            'app_name': app_info['app_name'],
            'build_number': app_info['build_number'],
            'device_platform': device_info['device_platform'],
            'js_sdk_version': '2.7.0.1',
            'app_version': app_info['app_version'],
            'ac': 'mobile',
            'openudid': device_info['openudid'],
            'channel': app_info['channel']
        }
        return params

    def params2str(self, params):  # 参数转化成url中需要拼接的字符串
        query = ''
        for k, v in params.items():
            query += '%s=%s&' % (k, v)
        query = query.strip('&')
        return query

    def get_sign(self, token, query):  # 调用接口获取签名
        r = requests.post('https://api.appsign.vip:2688/sign', json={'token': token, 'query': query}).json()
        if r['success']:
            sign = r['data']
        else:
            sign = r['success']
        return sign

    def get_aweme_id(self, share_url):  # 调用接口，根据share_url获取aweme_id
        # 真实url为headers里的Location，禁止重定向，才能获取
        r = requests.get(share_url, headers=self.headers, allow_redirects=False)
        url = r.headers['Location']
        aweme_id = re.search(r'\d+', url).group()
        return aweme_id

# if __name__ == '__main__':
#     downloader = Downloader()
#     downloader.run('http://v.douyin.com/Rv7Jqn/')
