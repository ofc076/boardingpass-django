from datetime import datetime

from django.shortcuts import redirect, render
from django.views.generic import ListView

from hello.forms import LogMessageForm
from hello.models import LogMessage
from hello.func import *

def about(request):
    """Renders the about page."""
    return render(request, "hello/about.html")

def status(request):
    """Renders the about page."""
    content = {}
    boot = boot_time()
#    boot = 1546048398

    content['uptime'] = uptime_str(boot)
    content['boottime'] = boottime_str(boot)
    content['curdate'] = datetime.now()
    return render(request, "hello/status.html", context=content)

def detail(request, barcode):
    """Renders the about page."""
    content = {}

    info = get_detail(barcode)
    content['barcode'] = barcode
    content['name'] = info.get('name', 'n/a')
    content['pdate'] = info.get('pdate', 'n/a')
    content['ptime'] = info.get('ptime', 'n/a')
    content['rtime'] = info.get('rtime', 'n/a')
    content['rdate'] = info.get('rdate', 'n/a')
    content['copies'] = info.get('copies', 'n/a')
    return render(request, "hello/detail.html", context=content)


def last30d(request):
    """Renders the about page."""
    content = {}
    try:
        content['arr'] = barcodes_total()[:30]
    except:
        content['arr'] = barcodes_total()
    return render(request, "hello/last30d.html", context=content)


def last50t(request):
    """Renders the about page."""
    content = {}
    try:
        content['arr'] = barcodes_list()[:50]
    except:
        content['arr'] = barcodes_list()[:50]
    return render(request, "hello/last50t.html", context=content)