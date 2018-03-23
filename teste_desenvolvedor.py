# -*- coding: utf-8 -*-

import xmlrpclib
import socket


class ConexaoOdoo():
    def __init__(self):
        self.database = str(raw_input('Nome do banco de dados: '))
        self.host = str(raw_input('Host/IP Odoo: '))
        self.user = str(raw_input('Usuario Odoo: '))
        self.password = str(raw_input('Senha Odoo: '))
        self.port = raw_input('Porta Odoo: ')
        self.conn, self.uid = self.new_connection()
        cliente_id = self.create_cliente()
        print 'ID do cliente criado: %s.\n' % cliente_id

    def new_connection(self):
        if not self.password:
            self.password = None
        if not self.port:
            self.port = 8069
        try:
            sock_common = xmlrpclib.ServerProxy('http://' + self.host + ':' + str(self.port) +
                                                '/xmlrpc/common')
            socket.setdefaulttimeout(3)
            uid = sock_common.login(self.database, self.user, self.password)
            sock = xmlrpclib.ServerProxy('http://' + self.host + ':' + str(self.port) +
                                         '/xmlrpc/object')
            return sock, uid
        except:
            print 'Nao foi possivel conectar ao Odoo!'
            exec exit()

    def create_cliente(self):
        vals = {'name': 'Tiago Henrique Prates', 'email': 'tiagoprates_911@hotmail.com',
                'phone': '98233-7159', 'zip': '35700-000'}
        cliente_id = self.conn.execute(self.database, self.uid, self.password,
                                       'res.partner', 'create', vals)
        return cliente_id


ConexaoOdoo()
