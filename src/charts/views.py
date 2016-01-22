from charts.models import Host
from django.http import HttpResponse
from django.template import loader, RequestContext


def index(request):
    all_hosts_l = Host.objects.all()

    template = loader.get_template('charts/index.html')
    context = RequestContext(request, {'host_l': all_hosts_l})
    return HttpResponse(template.render(context))


def host(request, host_id):
    return HttpResponse("show charts for host %s" % host_id)
