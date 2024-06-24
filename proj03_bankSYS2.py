import textwrap
from time import sleep
from strings import title
from abc import ABC, abstractmethod
from datetime import datetime

# INCLUSO NESTE EXERCÍCIO: importação de módulos, variáveis locais, argumentos nomeados, POO, módulos, módulos in-build,
# listas, dicionários, estruturas de repetição, estruturas de condição, validação de dados, decoradores, associação./
# Para que todos os dados sejam permanentes, crie um arquivo para clientes e outro para contas e associe-os.

class ContaIterador:
    def __init__(self,contasIter):
        self.contas = contasIter
        self._index = 0
    # A razão pela qual __iter__ retorna self é para simplificar o uso em um loop for. Quando você itera sobre um objeto, /
    # o Python chama implicitamente o método __iter__ para obter um iterador. Nesse caso, como ContaIterador retorna self, /
    # ele pode ser usado diretamente em um loop for.
    # Em resumo, ao retornar self no método __iter__, você está transformando rapidamente um objeto iterador em um objeto /
    # iterável, permitindo que ele seja usado em um loop for. Isso evita a necessidade de criar duas classes separadas /
    # (uma para o iterador e outra para o iterável) e simplifica o código.
    def __iter__(self):
        # return iter(self)     Caso não tenha o next.
        return self
    # embora seja comum implementar __iter__ e __next__ juntos para criar um iterador completo, você pode usar apenas /
    # __iter__ ou aproveitar a função iter() para obter um iterador a partir de um objeto iterável.
    def __next__(self):
        try:
            conta = self.contas[self._index]
            return f"""
            Agência: {conta.agencia}
            Número: {conta.numero}
            Titular: {conta.cliente.nome}
            Saldo: R${conta.saldo:.2f}
                    """
        except IndexError:
            print('Indexação interrompida.')
        finally:
            self._index += 1

class Cliente:
    def __init__(self,endereco):
        self.endereco = endereco
        self.contas = []

    def realiza_transacao(self,conta,transacao):
        if len(conta.historico.transacoes_do_dia()) >= 3:
            print('O limite de transações diárias foi atingido.')
            return
        transacao.registrar(conta)
    def add_conta(self,conta):
        self.contas.append(conta)
class PessoaFisica(Cliente):
    def __init__(self,nome,data_nasc,cpf,endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nasc = data_nasc
        self.cpf = cpf

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}: ({self.nome}, {self.cpf})>'

class Conta:
    def __init__(self,numero,cliente):
        self._numero = numero
        self._cliente = cliente
        self._saldo = 0
        self._agencia = '0001'
        self._historico = Historico()

    @classmethod
    def nova_conta(cls,cliente,numero):
        return cls(numero,cliente)
    @property
    def numero(self):
        return self._numero
    @property
    def cliente(self):
        return self._cliente
    @property
    def saldo(self):
        return self._saldo
    @property
    def agencia(self):
        return self._agencia
    @property
    def historico(self):
        return self._historico

    def sacar(self,valor):
        saldo = self.saldo
        if valor > saldo:
            print('Falha ao sacar! Saldo insuficiente.')
        elif valor>0:
            self._saldo -= valor
            print('Saque realizado com sucesso!')
        else:
            print('Falha ao sacar! Valor inválido.')

    def depositar(self,valor):
        if valor>0:
            self._saldo += valor
            print('Depósito realizado ocm sucesso!')
        else:
            print('Falha ao depositar! Valor inválido.')

class ContaCorrente(Conta):
    def __init__(self,numero,cliente,limite=500,limite_saques=3):
        super().__init__(numero,cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self,valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes
                             if transacao["tipo"]==Saque.__name__])
        if valor>self.limite:
            print(f'Falha ao sacar! Valor do saque é muito alto. Limite: {self.limite}')
        elif numero_saques>self.limite_saques:
            print(f'Falha ao sacar! Número de saques excedido. Limite: {self.limite_saques}')
        else:
            super().sacar(valor)

    def __repr__(self):
        return f'<{self.__class__.__name__}: ({self.agencia}\t {self.numero}\t {self.cliente.nome}>'

    def __str__(self):
        return f"""
        Agência: {self.agencia}
        C/C: {self.numero}
        Titular: {self.cliente.nome}
        """

class Historico:
    def __init__(self):
        self._transacoes = []
    @property
    def transacoes(self):
        return self._transacoes
    def add_transacao(self,transacao):
        self.transacoes.append(
            {"tipo": transacao.__class__.__name__,
             "valor": transacao.valor,
             # Usando o "strftime()" do módulo datetime para formatar a data e horário atual.
             "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s"),
             }
        )

    def gerar_log(self,tipo_transacao=None):
        for transacao in self._transacoes:
            if tipo_transacao is None or transacao["tipo"].lower()==tipo_transacao.lower():
                yield transacao
    def transacoes_do_dia(self):
        data_atual = datetime.now().date()
        transacoes = []
        for transacao in self._transacoes:
            data_transacao = datetime.strftime(transacao["data"],"%d-%m-%Y %H:%M:%s").date()
            if data_atual==data_transacao:
                transacoes.append(transacao)
        return transacoes

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass
    @classmethod
    @abstractmethod
    def registrar(cls,conta):
        pass

class Saque(Transacao):
    def __init__(self,valor):
        self._valor= valor
    @property
    def valor(self):
        return self._valor

    def registrar(self,conta):
        transfer_success = conta.sacar(self.valor)
        if transfer_success:
            conta.historico.add_transacao(self)

class Deposito(Transacao):
    def __init__(self,valor):
        self._valor= valor
    @property
    def valor(self):
        return self._valor

    def registrar(self,conta):
        transfer_success = conta.depositar(self.valor)
        if transfer_success:
            conta.historico.add_transacao(self)


title("SISTEMA BANCÁRIO")
print("""
[1] - Depositar
[2] - Sacar
[3] - Ver extrato

[4] - Novo usuário
[5] - Nova conta
[6] - Listar contas

[7] - Sair
    """)
print('-' * 50)

def log_transacao(func):
    def envelope(*args,**kwargs):
        resultado = func(*args,**kwargs)
        data_hora = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        # O arquivo de log corresponde ao que está dentro do with. Perceba que usamos a letra "a" pois não queremos sobrescrever.
        with open('log.txt','a',encoding='utf8') as file:
            file.write(
                f'[{data_hora}] Função {func.__name__} executada com argumentos {args} e {kwargs}, retornou {resultado}\n'
            )
        print(f'{data_hora}: {func.__name__.upper()}')
        return resultado
    return envelope

def filter_client(cpf,filtro_clientes):
    clientes_filtrados = [
        i for i in filtro_clientes
        if i.cpf==cpf
    ]
    return clientes_filtrados[0] if clientes_filtrados else None
def recover_client(cliente):
    if not cliente.contas:
        print('Este cliente não possui uma conta.')
        return
    return cliente.contas[0]

@log_transacao
def depositar(lista,valor):
    cpf = int(input('Informe o CPF do cliente (apenas números): '))
    cliente = filter_client(cpf,clientes)
    if not cliente:
        print('Cliente não encontrado.')
        return
    valor = float(input('Informe o valor do depósito: '))
    transacao = Deposito(valor)
    conta = recover_client(cliente)
    if not conta: return
    cliente.realizar_transacao(conta,transacao)

@log_transacao
def sacar(lista):
    cpf = int(input('Informe o CPF do cliente (apenas números): '))
    cliente = filter_client(cpf,clientes)
    if not cliente:
        print('Cliente não encontrado.')
        return
    valor = float(input('Informe o valor do saque: '))
    transacao = Saque(valor)
    conta = recover_client(cliente)
    if not conta: return
    cliente.realizar_transacao(conta,transacao)

@log_transacao
def exibir_extrato(lista):
    cpf = int(input('Informe o CPF do cliente (apenas números): '))
    cliente = filter_client(cpf, clientes)
    if not cliente:
        print('Cliente não encontrado.')
    conta = recover_client(cliente)
    if not conta: return
    print('='*15,' EXTRATO ','='*15)
    extrato = ''
    tem_transacao = False
    for transacao in conta.historico.gerar_log():
        tem_transacao=True
        extrato += f"\n{transacao["data"]}\n{transacao['tipo']}: \nR$ {transacao['valor']:.2f}"
    if not tem_transacao:
        extrato = 'Não foram realizadas transações.'
    print(extrato)
    sleep(0.5)
    print(f"\nSaldo: R${conta.saldo:.2f}")
    print('='*30)

@log_transacao
def criar_cliente(lista):
    cpf = int(input('Informe o CPF do cliente (apenas números): '))
    cliente = filter_client(cpf, clientes)
    if cliente:
        print('Já existe um cliente com esse CPF.')
        return
    nome = input('Informe o nome completo: ')
    data_nasc = input('informe a data de nascimento (dd-mm-aaaa): ')
    endereco = input('Informe o endereco (logadouro, nro - bairro - cidade/ estado): ')
    cliente = PessoaFisica(nome=nome,data_nasc=data_nasc,cpf=cpf,endereco=endereco)
    clientes.append(cliente)
    sleep(1)
    print('Cliente criado com sucesso!')

@log_transacao
def criar_conta(num,cliente,lista):
    cpf = int(input('Informe o CPF do cliente (apenas números): '))
    cliente = filter_client(cpf, clientes)
    if not cliente:
        print('Cliente não encontrado. Fluxo de criação de conta encerrado.')
        return
    conta = ContaCorrente.nova_conta(cliente=cliente,numero=num)
    contas.append(conta)
    cliente.contas.append(conta)
    sleep(1)
    print('Conta criada com sucesso!')

def listar_contas(lista):
    if not lista:
        print('Não há contas.')
        return
    else:
        for conta in contas:
            print('='*50)
            print(textwrap.dedent(str(conta)))


clientes = []
contas = []

def menu():

    while True:
        comando = int(input('Digite o número correspondente de acesso: '))

        if comando==1:
            print('Depositar valor...')
            sleep(0.5)
            depositar(clientes)
        elif comando==2:
            print('Sacar valor...')
            sleep(0.5)
            sacar(clientes)
        elif comando==3:
            exibir_extrato(clientes)
        elif comando==4:
            criar_cliente(clientes)
        elif comando==5:
            numero_conta = len(contas)+1
            criar_conta(numero_conta,clientes,contas)
        elif comando==6:
            listar_contas(contas)
        elif comando==7:
            print('Volte sempre!')
            break
        else:
            print('Valor inválido. Digite um número entre 1 e 7! ')
            continue

menu()
