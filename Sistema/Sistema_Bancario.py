import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

class SistemaBancarioGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Bancário")

        self.contas, self.proximo_numero_conta = self.carregar_dados()

        # Interface para Novo Cliente
        self.label_nome = tk.Label(root, text="Nome:")
        self.label_nome.grid(row=0, column=0, padx=10, pady=10)
        self.entry_nome = tk.Entry(root)
        self.entry_nome.grid(row=0, column=1, padx=10, pady=10)

        self.label_cpf = tk.Label(root, text="CPF:")
        self.label_cpf.grid(row=1, column=0, padx=10, pady=10)
        self.entry_cpf = tk.Entry(root)
        self.entry_cpf.grid(row=1, column=1, padx=10, pady=10)

        self.label_data_nascimento = tk.Label(root, text="Data de Nascimento:")
        self.label_data_nascimento.grid(row=2, column=0, padx=10, pady=10)
        self.entry_data_nascimento = tk.Entry(root)
        self.entry_data_nascimento.grid(row=2, column=1, padx=10, pady=10)

        self.button_novo_cliente = tk.Button(root, text="Novo Cliente", command=self.novo_cliente)
        self.button_novo_cliente.grid(row=3, columnspan=2, padx=10, pady=10)

        # Interface para Nova Conta
        self.label_cpf_nova_conta = tk.Label(root, text="Insira o CPF:")
        self.label_cpf_nova_conta.grid(row=4, column=0, padx=10, pady=10)
        self.entry_cpf_nova_conta = tk.Entry(root)
        self.entry_cpf_nova_conta.grid(row=4, column=1, padx=10, pady=10)

        self.button_nova_conta = tk.Button(root, text="Nova Conta", command=self.nova_conta)
        self.button_nova_conta.grid(row=5, columnspan=2, padx=10, pady=10)

        # Botões para outras operações
        self.button_listar_contas = tk.Button(root, text="Listar Contas", command=self.listar_contas)
        self.button_listar_contas.grid(row=6, columnspan=2, padx=10, pady=10)

        self.button_depositar = tk.Button(root, text="Depositar", command=self.depositar)
        self.button_depositar.grid(row=7, columnspan=2, padx=10, pady=10)

        self.button_sacar = tk.Button(root, text="Sacar", command=self.sacar)
        self.button_sacar.grid(row=8, columnspan=2, padx=10, pady=10)

        self.button_extrato = tk.Button(root, text="Extrato", command=self.extrato)
        self.button_extrato.grid(row=9, columnspan=2, padx=10, pady=10)

    def carregar_dados(self):
        if os.path.exists("dados_banco.json"):
            with open("dados_banco.json", "r") as file:
                dados = json.load(file)
                return dados.get("contas", {}), dados.get("proximo_numero_conta", 1)
        return {}, 1

    def salvar_dados(self):
        with open("dados_banco.json", "w") as file:
            json.dump({
                "contas": self.contas,
                "proximo_numero_conta": self.proximo_numero_conta
            }, file)

    def novo_cliente(self):
        nome = self.entry_nome.get()
        cpf = self.entry_cpf.get()
        data_nascimento = self.entry_data_nascimento.get()

        if cpf in self.contas:
            messagebox.showerror("Erro", "Cliente com este CPF já existe.")
        else:
            self.contas[cpf] = {"nome": nome, "data_nascimento": data_nascimento, "contas": []}
            self.salvar_dados()
            messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")

    def nova_conta(self):
        cpf = self.entry_cpf_nova_conta.get()

        if cpf in self.contas:
            numero_conta = f"{self.proximo_numero_conta:04d}"
            senha = simpledialog.askstring("Senha", "Digite uma senha para a nova conta:")
            self.contas[cpf]["contas"].append({"numero": numero_conta, "saldo": 0, "senha": senha, "transacoes": []})
            self.proximo_numero_conta += 1
            self.salvar_dados()
            messagebox.showinfo("Sucesso", f"Conta {numero_conta} criada com sucesso!")
        else:
            messagebox.showerror("Erro", "CPF não encontrado.")

    def listar_contas(self):
        cpf = self.entry_cpf_nova_conta.get()
        if cpf in self.contas:
            contas = self.contas[cpf]["contas"]
            contas_str = "\n".join([f"Conta {conta['numero']}: Saldo R${conta['saldo']:.2f}" for conta in contas])
            messagebox.showinfo("Contas", contas_str)
        else:
            messagebox.showerror("Erro", "CPF não encontrado.")

    def depositar(self):
        cpf = self.entry_cpf_nova_conta.get()
        if cpf in self.contas:
            contas = self.contas[cpf]["contas"]
            if contas:
                numero_conta = simpledialog.askstring("Depósito", "Digite o número da conta para depósito:")
                valor = float(simpledialog.askstring("Depósito", "Digite o valor do depósito:"))
                for conta in contas:
                    if conta["numero"] == numero_conta:
                        conta["saldo"] += valor
                        conta["transacoes"].append({"tipo": "Depósito", "valor": valor})
                        self.salvar_dados()
                        messagebox.showinfo("Sucesso", "Depósito realizado com sucesso!")
                        return
                messagebox.showerror("Erro", "Número da conta não encontrado.")
            else:
                messagebox.showerror("Erro", "Este CPF não possui contas.")
        else:
            messagebox.showerror("Erro", "CPF não encontrado.")

    def sacar(self):
        cpf = self.entry_cpf_nova_conta.get()
        if cpf in self.contas:
            contas = self.contas[cpf]["contas"]
            if contas:
                numero_conta = simpledialog.askstring("Saque", "Digite o número da conta para saque:")
                valor = float(simpledialog.askstring("Saque", "Digite o valor do saque:"))
                for conta in contas:
                    if conta["numero"] == numero_conta:
                        senha = simpledialog.askstring("Senha", "Digite a senha da conta:")
                        if conta["senha"] == senha:
                            if conta["saldo"] >= valor:
                                conta["saldo"] -= valor
                                conta["transacoes"].append({"tipo": "Saque", "valor": valor})
                                self.salvar_dados()
                                messagebox.showinfo("Sucesso", "Saque realizado com sucesso!")
                            else:
                                messagebox.showerror("Erro", "Saldo insuficiente.")
                        else:
                            messagebox.showerror("Erro", "Senha incorreta.")
                        return
                messagebox.showerror("Erro", "Número da conta não encontrado.")
            else:
                messagebox.showerror("Erro", "Este CPF não possui contas.")
        else:
            messagebox.showerror("Erro", "CPF não encontrado.")

    def extrato(self):
        cpf = self.entry_cpf_nova_conta.get()
        if cpf in self.contas:
            contas = self.contas[cpf]["contas"]
            if contas:
                numero_conta = simpledialog.askstring("Extrato", "Digite o número da conta para extrato:")
                for conta in contas:
                    if conta["numero"] == numero_conta:
                        saldo = conta["saldo"]
                        extrato_str = "\n".join([f"{transacao['tipo']}: R${transacao['valor']:.2f}" for transacao in conta["transacoes"]])
                        extrato_completo = f"Saldo atual: R${saldo:.2f}\n{extrato_str if extrato_str else 'Nenhuma transação realizada.'}"
                        messagebox.showinfo(f"Extrato da Conta {numero_conta}", extrato_completo)
                        return
                messagebox.showerror("Erro", "Número da conta não encontrado.")
            else:
                messagebox.showerror("Erro", "Este CPF não possui contas.")
        else:
            messagebox.showerror("Erro", "CPF não encontrado.")

if __name__ == "__main__":
    root = tk.Tk()
    sistema = SistemaBancarioGUI(root)
    root.mainloop()
