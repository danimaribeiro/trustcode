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
        cliente_atualizado = self.update_cliente(cliente_id)
        print 'Cliente atualizado: %s' % 'SIM' if cliente_atualizado else 'Nao'

    def new_connection(self):
        """
        O metodo estabalece a conexao com o Odoo.
        :return: objeto da conexao e id do usuario logado.
        :rtype: object
        """
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
        """
        O metodo cria um novo cliente.
        :return: id da tabela res_partner
        :rtype: int
        """
        vals = {'name': 'Tiago Henrique Prates', 'email': 'tiagoprates_911@hotmail.com',
                'phone': '98233-7159', 'zip': '35700-000'}
        cliente_id = self.conn.execute(self.database, self.uid, self.password,
                                       'res.partner', 'create', vals)
        return cliente_id

    def update_cliente(self, cliente_id):
        """
        O metodo atualiza os dados de um registro.
        :param cliente_id: id da tabela res_partner, identificador do cliente.
        :type cliente_id: int
        :return: Verdadeiro, caso consiga realizar a atualizacao. Senao, Falso.
        :rtype: bool
        """
        vals = {'phone': '982648882'}  # Nao encontrei o campo RG, incluido CPF
        cliante_atualizado = self.conn.execute(self.database, self.uid, self.password,
                                               'res.partner', 'write', [cliente_id], vals)
        return cliante_atualizado


ConexaoOdoo()
