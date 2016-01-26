from __future__ import print_function
from ansible.plugins.callback import CallbackBase
from django.utils import timezone

# add our top level src file to the sys.path
# so that we can import stuff from this ansible plugin
import sys, os
import inspect
from os.path import dirname, join, realpath
src_dir = join(dirname(realpath(inspect.getfile(inspect.currentframe()))), '../')
sys.path.append(src_dir)

# inform django where our db settings are:
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "monitoring.settings")

# now we can import our django stuff:
from charts.models import Host, MemUsageSample, FSUsageSample


class CallbackModule(CallbackBase):

    def runner_on_ok(self, host, result):
        # this method is called on every successful module, filter here

        logged_modules = ['debug']
        if type(result) == dict:
            invocation = result.get('invocation')
            if invocation.get('module_name') not in logged_modules:
                return
            else:
                # information sent from ansible is suitable for our db
                # start by getting the host and the current time
                h = Host.objects.get(name__exact=host)
                dt = timezone.now()

                var_name = invocation.get('module_args').get('var')
                #######################################################################
                # process memory information
                if var_name == 'ansible_memory_mb.real':
                    real_mem_d = result.get(var_name)
                    print('will write in the datbase table ', var_name)
                    print('host:', host)

                    mem_t = int(real_mem_d.get('total'))
                    mem_u = int(real_mem_d.get('used'))

                    mem_sample = MemUsageSample()
                    mem_sample.host = h
                    mem_sample.datetime = dt
                    mem_sample.percent = 100*float(mem_u)/float(mem_t)
                    mem_sample.save()

                #######################################################################
                # process disk usage information
                elif var_name == 'ansible_mounts':
                    mount_l = result.get(var_name)
                    for m in mount_l:
                        partition_name = m.get('mount')
                        if partition_name == '/':
                            # last m is the partition that we need
                            break
                    disk_t = m.get('size_total')
                    disk_a = m.get('size_available')
                    disk_u = disk_t - disk_a

                    disk_sample = FSUsageSample()
                    disk_sample.host = h
                    disk_sample.datetime = dt
                    disk_sample.percent = 100*float(disk_u)/float(disk_t)
                    disk_sample.save()

                else:
                    pass