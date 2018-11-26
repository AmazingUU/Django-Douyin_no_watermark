import json
import re

from django.http import HttpResponse
from django.shortcuts import render
from download_no_watermark.download_no_watermark import Downloader


def douyin(request):
    context = {}
    if request.POST:
        input = request.POST['search']
        # 匹配url
        share_url = re.search(r'(https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]', input)
        if share_url:
            share_url = share_url.group()
            downloader = Downloader()
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
