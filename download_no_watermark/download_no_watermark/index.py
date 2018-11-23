from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from download_no_watermark.download_no_watermark import Downloader


def index(request):
    context = {}
    if request.POST:
        share_url = request.POST['search']
        downloader = Downloader()
        download_url = downloader.run(share_url)
        if download_url:
            context['rlt'] = '下载地址:' + download_url
        else:
            context['rlt'] = '下载失败'
    return render(request, 'index.html',context)
