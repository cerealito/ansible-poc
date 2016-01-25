from __future__ import print_function
from ansible.plugins.callback import CallbackBase

# add our top level src file to the sys.path
# so that we can import stuff from this ansible plugin
import sys
import inspect
from os.path import dirname, join, realpath
src_dir = join(dirname(realpath(inspect.getfile(inspect.currentframe()))), '../')
sys.path.append(src_dir)
# now we can import our django stuff:
from django.conf import settings
settings.configure()

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
                param, value = data_s.split(' = ')

                if param == 'memfree_mb':
                    print('will write in the database')
                    print('parm:', param)
                    print('value:', value)
                else:
                    print ('disk usage not implemented yet')
