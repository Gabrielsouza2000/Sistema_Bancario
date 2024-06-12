from datetime import datetime
from abc import ABC, abstractmethod
import textwrap
from pathlib import Path

# Definir o caminho absoluto do diretório do script
ROOT_PATH = Path(__file__).parent

# Definir o caminho absoluto para o arquivo de log
LOG_FILE_PATH = ROOT_PATH / "log.txt"


# Classe de iterador para contas
class ContasIterador:
    def __init__(self, contas):
        self.contas = contas
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            conta = self.contas[self._index]
            return f"""\
            Agência:\t{conta.agencia}
            Número:\t\t{conta.numero}
            Titular:\t{conta.cliente.nome}
            Saldo:\t\tR$ {conta.saldo:.2f}
        """
        except IndexError:
            raise StopIteration
        finally:
            self._index += 1


# Classe de cliente
class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        if len(conta.historico.transacoes_do_dia()) >= 10:
            print("\n@@@ Você excedeu o número de transações permitidas para hoje! @@@")
            return

        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


# Classe de cliente pessoa física
class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: ('{self.nome}', '{self.cpf}')>"


# Classe de conta
class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        if valor > self._saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
            return False

        if valor <= 0:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False

        self._saldo -= valor
        print("\n=== Saque realizado com sucesso! ===")
        return True

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
            return True

        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
        return False


# Classe de conta corrente
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
            return False

        if excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
            return False

        return super().sacar(valor)

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """


# Classe de histórico de transações
class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )

    def filtrar_transacoes_por_tipo(self, tipo_transacao):
        return [transacao for transacao in self._transacoes if transacao["tipo"].lower() == tipo_transacao.lower()]

    def transacoes_do_dia(self):
        data_atual = datetime.utcnow().date()
        transacoes = []
        for transacao in self._transacoes:
            data_transacao = datetime.strptime(transacao["data"], "%d-%m-%Y %H:%M:%S").date()
            if data_atual == data_transacao:
                transacoes.append(transacao)
        return transacoes


# Classe abstrata de transação
class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass


# Classe de saque
class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


# Classe de depósito
class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


# Função para logar ações com data e hora
def log_acoes(mensagem):
    agora = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    print(f"{agora} - {mensagem}")


def log_transacao(func):
    def envelope(*args, **kwargs):
        resultado = func(*args, **kwargs)
        data_hora = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_FILE_PATH, "a") as arquivo:
            arquivo.write(
                f"[{data_hora}] Função '{func.__name__}' executada com argumentos {args} e {kwargs}. "
                f"Retornou {resultado}\n"
            )
        return resultado

    return envelope


# Função para exibir o menu
def menu():
    menu = """\n
    ================ MENU ================
    [1]\tDepositar
    [2]\tSacar
    [3]\tExtrato
    [4]\tNova conta
    [5]\tListar contas
    [6]\tNovo usuário
    [9]\tSair
    => """
    return input(textwrap.dedent(menu))


# Função para salvar dados das contas no log
def salvar_dados_conta(conta):
    with open(LOG_FILE_PATH, "a", encoding="utf-8") as arquivo:
        arquivo.write(
            f"\n[LOG] Conta Criada - Agência: {conta.agencia}, Número: {conta.numero}, "
            f"Titular: {conta.cliente.nome}, CPF: {conta.cliente.cpf}, Saldo: R$ {conta.saldo:.2f}\n"
        )


# Função para filtrar cliente por CPF
def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


# Função para recuperar conta de um cliente
def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return None

    if len(cliente.contas) == 1:
        return cliente.contas[0]

    print("\nEscolha uma das contas abaixo:")
    for i, conta in enumerate(cliente.contas):
        print(f"[{i}] Conta: {conta.numero}")

    while True:
        indice = input("Selecione o número da conta: ")
        if indice.isdigit() and int(indice) in range(len(cliente.contas)):
            return cliente.contas[int(indice)]
        else:
            print("\n@@@ Opção inválida! Por favor, escolha uma conta válida. @@@")


# Função para realizar depósito
def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    while True:
        valor_str = input("Informe o valor do depósito: ")
        try:
            valor = float(valor_str)
            if valor <= 0:
                print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            else:
                break
        except ValueError:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)
    log_acoes(f"Depósito de R$ {valor:.2f} realizado com sucesso")


# Função para realizar saque
def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    while True:
        valor_str = input("Informe o valor do saque: ")
        try:
            valor = float(valor_str)
            if valor <= 0:
                print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            else:
                break
        except ValueError:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)
    log_acoes(f"Saque de R$ {valor:.2f} realizado com sucesso")


# Função para exibir extrato
def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n=============== EXTRATO ===============")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['data']} - {transacao['tipo']}: R$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\tR$ {conta.saldo:.2f}")
    print("========================================")

    opcoes_transacao = {"1": "deposito", "2": "saque", "3": "todos"}

    while True:
        escolha = input("\nEscolha o tipo de transação a ser exibido (1-depósito / 2-saque / 3-todos): ")

        if escolha in opcoes_transacao:
            tipo_transacao = opcoes_transacao[escolha]
            break
        else:
            print("\n@@@ Opção inválida! Por favor, escolha uma opção válida. @@@")
            continue

    if tipo_transacao == "todos":
        return

    print(f"\n=============== EXTRATO DE {tipo_transacao.upper()} ===============")
    transacoes_filtradas = conta.historico.filtrar_transacoes_por_tipo(tipo_transacao)

    extrato_filtrado = ""
    if not transacoes_filtradas:
        extrato_filtrado = f"Não foram realizadas movimentações do tipo {tipo_transacao}."
    else:
        for transacao in transacoes_filtradas:
            extrato_filtrado += f"\n{transacao['data']} - {transacao['tipo']}: R$ {transacao['valor']:.2f}"

    print(extrato_filtrado)
    print("===========================================================")


# Função para criar um cliente
def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n@@@ Já existe cliente com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    log_acoes("Cliente criado com sucesso")
    print("\n=== Cliente criado com sucesso! ===")


# Função para criar uma conta
def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado! @@@")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.adicionar_conta(conta)

    log_acoes("Conta criada com sucesso")
    salvar_dados_conta(conta)
    print("\n=== Conta criada com sucesso! ===")


# Função para listar contas
def listar_contas(contas):
    iterador = ContasIterador(contas)

    print("\n=============== CONTAS ===============")
    for conta in iterador:
        print(conta)
    print("=======================================")


def carregar_dados_salvos():
    clientes = []
    contas = []

    with open(LOG_FILE_PATH, "r") as arquivo:
        linhas = arquivo.readlines()

        for linha in linhas:
            if "Conta Criada" in linha:
                detalhes_conta = linha.split(" - ")[1]
                agencia = detalhes_conta.split(",")[0].split(":")[1].strip()
                numero = detalhes_conta.split(",")[1].split(":")[1].strip()
                titular = detalhes_conta.split(",")[2].split(":")[1].strip()
                cpf = detalhes_conta.split(",")[3].split(":")[1].strip()
                saldo = float(detalhes_conta.split(",")[4].split(":")[1].strip().replace("R$ ", ""))

                # Criando uma data de nascimento fictícia para o cliente
                data_nascimento = datetime.now().strftime("%d-%m-%Y")

                # Criando instância de PessoaFisica com os dados do log
                cliente = PessoaFisica(nome=titular, data_nascimento=data_nascimento, cpf=cpf, endereco="")
                conta = ContaCorrente(numero=numero, cliente=cliente)
                conta._agencia = agencia
                conta._saldo = saldo

                # Adicionando a conta ao cliente
                cliente.adicionar_conta(conta)

                # Adicionando cliente e conta às listas
                clientes.append(cliente)
                contas.append(conta)

    return clientes, contas

    return clientes, contas


def main():
    # Carrega os dados salvos
    clientes, contas = carregar_dados_salvos()

    # Mensagem de depuração para o caminho do arquivo de log
    print(f"Arquivo de log será salvo em: {LOG_FILE_PATH}")

    while True:
        opcao = menu()

        if opcao == "1":
            depositar(clientes)

        elif opcao == "2":
            sacar(clientes)

        elif opcao == "3":
            exibir_extrato(clientes)

        elif opcao == "4":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "5":
            listar_contas(contas)

        elif opcao == "6":
            criar_cliente(clientes)

        elif opcao == "9":
            break

        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")


if __name__ == "__main__":
    main()
