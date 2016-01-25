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
            invocation = result.pop('invocation')
            if invocation.get('module_name') not in logged_modules:
                return
            else:
                if invocation.get('module_args') == {}:
                    return

                data_s = invocation.get('module_args').get('msg')

                # TODO: find a better way to do this
                ansible_param, ansible_value = data_s.split(' = ')

                if ansible_param == 'memfree_mb':
                    print('will write in the datbase table ', ansible_param)
                    print('host:', host)
                    print('value:', ansible_value)
                    h = Host.objects.filter(name__startswith=host)[0]

                    mem_sample = MemUsageSample()
                    mem_sample.host = h
                    mem_sample.num_mb = ansible_value
                    mem_sample.datetime = timezone.now()

                    mem_sample.save()

                else:
                    print ('disk usage not implemented yet')
