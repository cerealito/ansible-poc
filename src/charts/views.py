import pygal
from charts.models import Host, MemUsageSample, FSUsageSample
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

    mem_sample_l = MemUsageSample.objects.filter(host_id=host_id)
    fsu_sample_l = FSUsageSample.objects.filter(host_id=host_id)

    mem_chart = pygal.Line(title='Hardware resources in ' + current_host.name,
                           x_label_rotation=30,
                           range=(0, 100),
                           legend_box_size=20)
    mem_times = []
    mem_values = []
    for s in mem_sample_l:
        assert isinstance(s, MemUsageSample)
        mem_times.append(s.datetime)
        mem_values.append(s.percent)

    mem_chart.x_labels = mem_times
    mem_chart.add('Used memory (%)', mem_values)

    fs_times = []
    fs_values = []
    for s in fsu_sample_l:
        assert isinstance(s, FSUsageSample)
        fs_times.append(s.datetime)
        fs_values.append(s.percent)

    mem_chart.x_labels = fs_times
    mem_chart.add('Disk Usage (%)', fs_values)


    return render(request, 'charts/graphs.html', {'chart_rendition': mem_chart.render()})
