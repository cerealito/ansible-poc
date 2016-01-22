from charts.models import Host
from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    all_hosts_l = Host.objects.all()

    context = {'host_l': all_hosts_l}
    # the render shortcut returns an HttpResponse object
    return render(request, 'charts/index.html', context)


def host(request, host_id):
    return HttpResponse("show charts for host %s" % host_id)
