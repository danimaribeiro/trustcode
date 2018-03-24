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
        print 'Cliente atualizado: %s.\n' % 'SIM' if cliente_atualizado else 'Nao'
        quantidade_cliente = self.get_quantidade_cliente()
        print 'Numero de clientes cadastrados: %s.\n' % quantidade_cliente
        cliente_dados = self.get_cliente_dados()
        print '10 primeiros clientes por ordem alfebetica: \n%s' % cliente_dados
        maior_venda_dados = self.get_maior_venda_dados()
        print 'Maior venda feita:\n %s.' % maior_venda_dados

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

    def get_quantidade_cliente(self):
        """
        O metodo realiza a busca de registros.
        :return: Numero da quantidade total de clientes.
        :rtype: list
        """
        cliente_ids = self.conn.execute(self.database, self.uid, self.password, 'res.partner',
                                        'search', [])
        return len(cliente_ids)

    def get_cliente_dados(self):
        """
        O metodo encontra dados dos 10 primeiros clientes.
        :return: Descricao do nome, em ordem alfabetica, e da cidade dos clientes.
        :rtype: str
        """
        cliente_ids = self.conn.execute(self.database, self.uid, self.password, 'res.partner',
                                        'search', [], 0, 10, 'id')
        cliente_dados = self.conn.execute(self.database, self.uid, self.password, 'res.partner',
                                          'read', cliente_ids, ['name', 'city_id'])
        cliente_dados = sorted(cliente_dados, key=lambda n: n.get('name').lower())
        list_dados = list()
        map(lambda d: list_dados.append(
            '%s / %s' % (d.get('name'), d.get('city_id')[1] or 'Nao cadastrado')), cliente_dados)
        return ' \n'.join(list_dados)

    def get_maior_venda_dados(self):
        """
        O metodo encontra os dados da maior venda realizada.
        :return: Descricao do nome do cliente e do valor total da venda.
        :rtype: str
        """
        sale_order_ids = self.conn.execute(self.database, self.uid, self.password, 'sale.order',
                                           'search', [], 0, 1, 'amount_total DESC')
        sale_order_dados = self.conn.execute(self.database, self.uid, self.password, 'sale.order',
                                             'read', sale_order_ids, ['partner_id', 'amount_total'])
        if not sale_order_dados:
            return ''
        if isinstance(sale_order_dados, (list, tuple)):
            sale_order_dados = sale_order_dados[0]
        return 'Cliente: %s / Total: %s\n' % (sale_order_dados.get('partner_id')[1],
                                              sale_order_dados.get('amount_total'))


ConexaoOdoo()
