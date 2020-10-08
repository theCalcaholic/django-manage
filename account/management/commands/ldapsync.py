# coding: utf-8

from django_auth_ldap.backend import LDAPBackend
from django.core.management.base import BaseCommand, CommandError
from account.models import *
import evh.settings_local as config
from pathlib import Path
from account.signals import *
from datetime import datetime
from account.mailman import Mailman
import os

import logging
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Sync Account/Group Information with outside world'
    def add_arguments(self, parser):
        parser.add_argument("--user", '-u', default=None,
                            help="Update only User")

        parser.add_argument("--group", '-g', default=None,
                            help="Update only Groyp")

    def handle(self, *args, **options):
        users = ldap_users()

        for username, user in users.items():
            if (options['user'] or options['group']) and \
               (options['user'] != "all" and username != options['user']):
                continue
            user_changed.send(sender=self.__class__, username=username)

        m = Mailman()
        for group in LDAP().groups():
            if (options['user'] or options['group']) and \
               (options['group'] != "all" and group != options['group']):
                continue
            if group.startswith('ag-') and group != 'ag-gastgeber':
                news = group + "-news"
                print(news)
            #    m.domain.create_list(news)

            group_changed.send(sender=self.__class__, group=group)
