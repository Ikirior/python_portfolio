from abc import ABC, abstractmethod
from datetime import datetime

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(transacao)

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
        self.data = datetime.now()

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
        self.data = datetime.now()

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0.0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero
        
    @property
    def historico(self):
        return self._historico
    
    @property
    def cliente(self):
        return self._cliente

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    def sacar(self, valor):
        if valor <= 0 or valor > self._saldo:
            print("\n@@@ Operação falhou! Valor inválido ou saldo insuficiente. @@@")
            return False
        
        self._saldo -= valor
        print("\n=== Saque realizado com sucesso! ===")
        return True

    def depositar(self, valor):
        if valor <= 0:
            print("\n@@@ Operação falhou! O valor do depósito deve ser positivo. @@@")
            return False
        
        self._saldo += valor
        print("\n=== Depósito realizado com sucesso! ===")
        return True
    
    def __str__(self):
        return f"Agência: {self._agencia} | C/C: {self._numero} | Titular: {self._cliente.nome}"


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500.0, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        saques_realizados_hoje = len([
            t for t in self.historico.transacoes 
            if isinstance(t, Saque) and t.data.date() == datetime.now().date()
        ])

        if valor > self.limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite por transação. @@@")
            return False
        elif saques_realizados_hoje >= self.limite_saques:
            print("\n@@@ Operação falhou! Número máximo de saques diários atingido. @@@")
            return False
        else:
            return super().sacar(valor)

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, data_nascimento, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

import textwrap

def menu():
    menu_texto = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu_texto))

def buscar_cliente(cpf, clientes):
    clientes_filtrados = [c for c in clientes if c.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def buscar_conta_cliente(cliente, numero_conta):
    contas_filtradas = [c for c in cliente.contas if c.numero == numero_conta]
    return contas_filtradas[0] if contas_filtradas else None

def exibir_extrato(conta):
    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes
    
    if not transacoes:
        print("Não foram realizadas movimentações.")
    else:
        for transacao in transacoes:
            tipo_transacao = transacao.__class__.__name__
            data_formatada = transacao.data.strftime("%d/%m/%Y %H:%M:%S")
            print(f"{data_formatada}\t{tipo_transacao}:\t R$ {transacao.valor:.2f}")

    print(f"\nSaldo:\t\t R$ {conta.saldo:.2f}")
    print("==========================================")


def main():
    clientes = []
    contas = [] # Lista global para manter o número da conta único

    while True:
        opcao = menu()

        if opcao == "nu":
            cpf = input("Informe o CPF (somente números): ")
            cliente = buscar_cliente(cpf, clientes)
            if cliente:
                print("\n@@@ Já existe um cliente com este CPF! @@@")
                continue

            nome = input("Informe o nome completo: ")
            data_nascimento = input("Informe a data de nascimento (dd/mm/aaaa): ")
            endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

            novo_cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
            clientes.append(novo_cliente)
            print("\n=== Cliente criado com sucesso! ===")

        elif opcao == "nc":
            cpf = input("Informe o CPF do titular da conta: ")
            cliente = buscar_cliente(cpf, clientes)
            if not cliente:
                print("\n@@@ Cliente não encontrado! Cadastre o cliente primeiro. @@@")
                continue

            numero_conta = len(contas) + 1
            nova_conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
            contas.append(nova_conta)
            cliente.adicionar_conta(nova_conta)
            print("\n=== Conta criada com sucesso! ===")
            print(f"Agência: {nova_conta._agencia}, C/C: {nova_conta.numero}")

        elif opcao == "lc":
            if not contas:
                print("\n@@@ Não há contas cadastradas. @@@")
            for conta in contas:
                print("-" * 40)
                print(textwrap.dedent(str(conta)))

        elif opcao == "d":
            cpf = input("Informe o CPF do cliente: ")
            cliente = buscar_cliente(cpf, clientes)
            if not cliente:
                print("\n@@@ Cliente não encontrado! @@@")
                continue

            numero_conta = int(input("Informe o número da conta: "))
            conta = buscar_conta_cliente(cliente, numero_conta)
            if not conta:
                print("\n@@@ Conta não encontrada para este cliente! @@@")
                continue
                
            valor = float(input("Informe o valor do depósito: "))
            deposito = Deposito(valor)
            cliente.realizar_transacao(conta, deposito)

        elif opcao == "s":
            cpf = input("Informe o CPF do cliente: ")
            cliente = buscar_cliente(cpf, clientes)
            if not cliente:
                print("\n@@@ Cliente não encontrado! @@@")
                continue

            numero_conta = int(input("Informe o número da conta: "))
            conta = buscar_conta_cliente(cliente, numero_conta)
            if not conta:
                print("\n@@@ Conta não encontrada para este cliente! @@@")
                continue
            
            valor = float(input("Informe o valor do saque: "))
            saque = Saque(valor)
            cliente.realizar_transacao(conta, saque)

        elif opcao == "e":
            cpf = input("Informe o CPF do cliente: ")
            cliente = buscar_cliente(cpf, clientes)
            if not cliente:
                print("\n@@@ Cliente não encontrado! @@@")
                continue

            numero_conta = int(input("Informe o número da conta para exibir o extrato: "))
            conta = buscar_conta_cliente(cliente, numero_conta)
            if conta:
                exibir_extrato(conta)
            else:
                print("\n@@@ Conta não encontrada para este cliente! @@@")

        elif opcao == "q":
            print("\nObrigado por usar nosso sistema bancário, até logo!\n")
            break

        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")

if __name__ == "__main__":
    main()