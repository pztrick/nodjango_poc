# from django.conf import settings
from django.core.management.base import BaseCommand
# from django.core.management import call_command

import logging
logging.basicConfig(level=logging.DEBUG)

from socketIO_client import SocketIO, BaseNamespace

from django.core import serializers
from django.db.models import get_model

from subprocess import Popen
import signal
import sys
import os

nodjango_root = os.path.join(os.path.dirname(__file__), '../..')
nodjango_indexjs = os.path.join(nodjango_root, 'index.js')

class DjangoNamespace(BaseNamespace):
    def on_orm(self, data):
        instance = [get_model(data['app'], data['model']).objects.get(**data['kwargs'])]
        response = {
            'payload': serializers.serialize('json', instance),
            'callback': data['callback'],
            'socket_id': data['socket_id']
        }
        print 'django inside on_orm, socket_id: %s' % (data['socket_id'])
        self.emit('callback', response)


class Command(BaseCommand):
    args = '<hostname> <public port> <runserver port> <socket port>'
    help = 'Listens over socket.io websocket'

    def handle(self, *args, **options):
        if len(args) != 4:
            raise Exception("Arguments needed: %s" % self.args)

        # parse arguments
        runserver_host = "%s:%s" % (args[0], args[2])
        runserver_cmd = "python manage.py runserver %s" % runserver_host
        nodejs_cmd = "node %s %s %s %s" % (nodjango_indexjs, args[1], args[2], args[3])

        try:
            # start django runserver
            proc1 = Popen(runserver_cmd, shell=True, preexec_fn=os.setsid, stdout=sys.stdout, stderr=sys.stderr)
            
            # start nodejs proxy
            proc2 = Popen(nodejs_cmd, shell=True, preexec_fn=os.setsid, stdout=sys.stdout, stderr=sys.stderr)

            # start django private socketio
            self.socket = SocketIO('127.0.0.1', int(args[3]), Namespace=DjangoNamespace)
            print '* * *\t django socket started'
            self.socket.wait()

        finally:
            print 'killing...'
            os.killpg(proc1.pid, signal.SIGTERM)
            os.killpg(proc2.pid, signal.SIGTERM)
            print 'killed!'