import json
import re

from django.http import HttpResponse
from django.shortcuts import render
from download_no_watermark.download_no_watermark import Downloader

def douyin(request):
    context = {}
    if request.POST:
        input = request.POST['search']
        share_url = re.search(r'(https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]',input).group()
        downloader = Downloader()
        download_url,desc = downloader.run(share_url)
        if download_url:
            context['download_url'] = json.dumps(download_url)
            context['desc'] = json.dumps(desc)
            # return HttpResponseRedirect(download_url)
        else:
            context['download_url'] = '下载失败'
    return render(request, 'douyin.html',context)
