import pygal
from charts.models import Host, MemUsageSample
from django.http import Http404
from django.shortcuts import render


def index(request):
    all_hosts_l = Host.objects.all()

    context = {'host_l': all_hosts_l}
    # the render shortcut returns an HttpResponse object
    return render(request, 'charts/index.html', context)


def host(request, host_id):
    if not Host.objects.filter(pk=host_id).count():
        raise Http404

    current_host = Host.objects.filter(pk=host_id)[0]

    sample_l = MemUsageSample.objects.filter(host_id=host_id)

    mem_chart = pygal.Line(title=current_host.name, x_label_rotation=30, range=(10000, 32000))
    time_labels = []
    mem_values = []
    for s in sample_l:
        assert isinstance(s, MemUsageSample)
        time_labels.append(s.datetime)
        mem_values.append(s.num_mb)

    mem_chart.x_labels = time_labels
    mem_chart.add('Free memory', mem_values)

    return render(request, 'charts/graphs.html', {'chart_rendition': mem_chart.render()})
