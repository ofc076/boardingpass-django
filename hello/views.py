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