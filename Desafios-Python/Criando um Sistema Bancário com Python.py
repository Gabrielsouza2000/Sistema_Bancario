menu_principal = """

[1] Criar conta
[2] Entrar na conta
[3] Visualizar todas as contas
[9] Sair

=> """

menu_conta = """

[1] Depositar
[2] Sacar
[3] Extrato
[4] Trocar de conta
[9] Sair

=> """

usuarios = {}
contas = {}
saldos = {}
extratos = {}
LIMITE_SAQUES = 3
num_conta = 1000  # Número inicial da conta

def criar_conta():
    global num_conta
    cpf = input("Informe o CPF (11 dígitos): ")
    if len(cpf) != 11:
        print("CPF deve ter exatamente 11 dígitos.")
        return

    nome = input("Informe o nome: ")
    senha = input("Informe a senha: ")

    if cpf in usuarios:
        print("Conta com este CPF já existe!")
    else:
        num_conta += 1
        usuarios[cpf] = {'nome': nome, 'senha': senha}
        contas[cpf] = f"0001-{num_conta}"  # Agência fixa e número sequencial
        saldos[cpf] = 0
        extratos[cpf] = ""
        print("Conta criada com sucesso! Agência:", contas[cpf])

def entrar_conta():
    cpf = input("Informe o CPF: ")
    senha = input("Informe a senha: ")

    if cpf in usuarios and usuarios[cpf]['senha'] == senha:
        print(f"Bem-vindo(a), {usuarios[cpf]['nome']}!")
        return cpf
    else:
        print("CPF ou senha inválidos!")
        return None

def visualizar_todas_contas():
    print("\n===== TODAS AS CONTAS CADASTRADAS =====")
    for cpf, info in usuarios.items():
        print(f"Nome: {info ['nome']} \nConta: {contas[cpf]} \nCPF: {cpf}")
    print("=======================================")

def depositar(cpf):
    try:
        valor = float(input("Informe o valor do depósito: "))
        if valor > 0:
            saldos[cpf] += valor
            extratos[cpf] += f"Depósito: \tR$ {valor:.2f}\n"
            print("=== Depósito realizado com sucesso! ===")
        else:
            print("Operação falhou! O valor informado é inválido.")
    except ValueError:
        print("Operação falhou! O valor informado é inválido.")

# Função sacar(), extrato() e main() permanecem inalteradas

def main():
    while True:
        opcao = input(menu_principal)

        if opcao == "1":
            criar_conta()
        elif opcao == "2":
            cpf = entrar_conta()
            if cpf:
                while True:
                    opcao_conta = input(menu_conta)
                    if opcao_conta == "1":
                        depositar(cpf)
                    # Implemente as outras opções (sacar, extrato, sair) aqui
                    elif opcao_conta == "4":
                        break
                    elif opcao_conta == "9":
                        return
                    else:
                        print("Operação inválida, por favor selecione novamente a operação desejada.")
        elif opcao == "3":
            visualizar_todas_contas()
        elif opcao == "9":
            print("Saindo...")
            break
        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

if __name__ == "__main__":
    main()
