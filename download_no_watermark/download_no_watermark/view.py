import json
import re

from django.http import StreamingHttpResponse
from django.shortcuts import render
from django.utils.encoding import escape_uri_path
from download_no_watermark.douyin_download import DouyinDownloader

from download_no_watermark.wenku_download import WenkuDownloader


def douyin(request):
    context = {}
    if request.POST:
        input = request.POST['search']
        # 匹配url
        share_url = re.search(r'(https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]', input)
        if share_url:
            share_url = share_url.group()
            downloader = DouyinDownloader()
            # 解析出下载地址和视频描述
            download_url, desc = downloader.run(share_url)
            if download_url:
                # 这里要用json.dumps传递参数，html的js里才能用{{download_url|safe}}引用该变量
                context['download_url'] = json.dumps(download_url)
                context['desc'] = json.dumps(desc)
                # return HttpResponseRedirect(download_url)
            else:
                context['result_code'] = json.dumps(-2)
        else:
            context['result_code'] = json.dumps(-1)
    return render(request, 'douyin.html', context)


def readFile(filename, chunk_size=512):
    with open(filename, 'rb') as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break


def wenku(request):
    context = {}
    if request.POST:
        input = request.POST['search']
        # 匹配url
        share_url = re.search(r'(https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]', input)
        if share_url:
            share_url = share_url.group()
            downloader = WenkuDownloader()
            file_name,path = downloader.run(share_url)
            if file_name:
                # the_file_name = '11.png'  # 显示在弹出对话框中的默认的下载文件名
                # filename = 'media/uploads/11.png'  # 要下载的文件路径
                response = StreamingHttpResponse(readFile(path))
                response['Content-Type'] = 'application/octet-stream'
                response['Content-Disposition'] = "attachment; filename*=utf-8''{}".format(escape_uri_path(file_name))
                return response
            else:
                context['result_code'] = json.dumps(-2)
        else:
            context['result_code'] = json.dumps(-1)
    return render(request, 'wenku.html', context)
