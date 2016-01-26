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
from charts.models import Host, MemUsageSample


class CallbackModule(CallbackBase):

    def runner_on_ok(self, host, result):
        # this method is called on every successful module, filter here

        logged_modules = ['debug']
        if type(result) == dict:
            invocation = result.get('invocation')
            if invocation.get('module_name') not in logged_modules:
                return
            else:
                var_name = invocation.get('module_args').get('var')
                if var_name == 'ansible_memory_mb.real':
                    real_mem = result.get(var_name)
                    print('will write in the datbase table ', var_name)
                    print('host:', host)
                    print('value:', real_mem)

                    h = Host.objects.get(name__exact=host)

                    mem_sample = MemUsageSample()
                    mem_sample.host = h
                    mem_sample.num_mb = int(real_mem.get('free'))
                    mem_sample.datetime = timezone.now()

                    mem_sample.save()
                elif invocation.get('module_args').get('var') == 'slash_usage':
                    # disk usage
                    pass
                else:
                    pass