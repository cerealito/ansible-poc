from __future__ import print_function
import stat

import os
from ansible.cli import CLI
from ansible.errors import AnsibleError
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.inventory import Inventory

from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager

__author__ = 'Samuel FLORES'


class PBExecutorWrapper:
    """
    horrible wrapper of a playbook executor. based on ansible-playbook cli tool
    """
    def __init__(self, playbook_p, inventory_p):
        self.playbook_p = playbook_p
        self.inventory_p = inventory_p

    def run(self):
        # create parser for CLI options
        parser = CLI.base_parser(
                usage="%prog playbook.yml",
                connect_opts=True,
                meta_opts=True,
                runas_opts=True,
                subset_opts=True,
                check_opts=True,
                inventory_opts=True,
                runtask_opts=True,
                vault_opts=True,
                fork_opts=True,
                module_opts=True,
        )

        # ansible playbook specific opts
        parser.add_option('--list-tasks', dest='listtasks', action='store_true',
                          help="list all tasks that would be executed")
        parser.add_option('--list-tags', dest='listtags', action='store_true',
                          help="list all available tags")
        parser.add_option('--step', dest='step', action='store_true',
                          help="one-step-at-a-time: confirm each task before running")
        parser.add_option('--start-at-task', dest='start_at_task',
                          help="start the playbook at the task matching this name")

        options, args = parser.parse_args([])

        # Note: slightly wrong, this is written so that implicit localhost
        # Manage passwords
        sshpass = None
        becomepass = None
        vault_pass = None
        passwords = {}

        passwords = {'conn_pass': sshpass, 'become_pass': becomepass}

        loader = DataLoader()

        # initial error check, to make sure all specified playbooks are accessible
        # before we start running anything through the playbook executor
        if not os.path.exists(self.playbook_p):
            raise AnsibleError("the playbook: %s could not be found" % self.playbook_p)
        if not (os.path.isfile(self.playbook_p) or stat.S_ISFIFO(os.stat(self.playbook_p).st_mode)):
            raise AnsibleError("the playbook: %s does not appear to be a file" % self.playbook_p)

        # create the variable manager, which will be shared throughout
        # the code, ensuring a consistent view of global variables
        variable_manager = VariableManager()
        # variable_manager.extra_vars = load_extra_vars(loader=loader, options=self.options)

        # create the inventory, and filter it based on the subset specified (if any)
        inventory = Inventory(loader=loader,
                              variable_manager=variable_manager,
                              host_list=self.inventory_p)
        variable_manager.set_inventory(inventory)

        no_hosts = False
        if len(inventory.list_hosts()) == 0:
            # Empty inventory
            print("provided hosts list is empty, only localhost is available")
            no_hosts = True
        # inventory.subset(options.subset)
        if len(inventory.list_hosts()) == 0 and no_hosts is False:
            # Invalid limit
            raise AnsibleError("Specified --limit does not match any hosts")

        # create the playbook executor, which manages running the plays via a task queue manager
        pbex = PlaybookExecutor(playbooks=[self.playbook_p],
                                inventory=inventory,
                                variable_manager=variable_manager,
                                loader=loader,
                                options=options,
                                passwords=passwords)

        results = pbex.run()
        return results
