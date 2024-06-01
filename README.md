# Gabriel Souza

## Conecte-se comigo

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/gabriel-souza-10421621b/)

[![Instagram](https://img.shields.io/badge/-Instagram-%23E4405F?style=for-the-badge&logo=instagram&logoColor=white)](https://www.instagram.com/gabrielssanx/)

[![Gmail](https://img.shields.io/badge/Gmail-333333?style=for-the-badge&logo=gmail&logoColor=red)](mailto:gabrielsouza3641@gmail.com)

## Desafios em Python

Estou estudando Python e, por causa disso, estou enviando alguns códigos para este repositório. Para testá-los, vocês podem utilizar alguns programas como PyCharm, Visual Studio Code ou algum outro de sua preferência.

Atualmente, há 1 desafio:

## Sistema
Este projeto implementa um sistema básico de banco em Python. A aplicação permite a criação de clientes, contas bancárias, e oferece funcionalidades como depósitos, saques e visualização de extratos. O sistema é baseado em orientação a objetos e inclui as principais classes: **Cliente**, **PessoaFisica**, **Conta**, **ContaCorrente**, **Historico**, e **Transacao**.

## Estrutura do Código

### Classes de Clientes:

- **Cliente:** Representa um cliente genérico com atributos de endereço e contas.
- **PessoaFisica:** Subclasse de Cliente que representa um cliente pessoa física, adicionando nome, data de nascimento e CPF.

### Classes de Contas:

- **Conta:** Classe base para uma conta bancária com atributos como número, saldo, agência e cliente. Inclui métodos para sacar e depositar dinheiro.
- **ContaCorrente:** Subclasse de Conta que adiciona funcionalidades específicas para contas correntes, como limite de saque e número máximo de saques por dia.

### Transações:

- **Transacao:** Classe abstrata para diferentes tipos de transações.
- **Saque:** Implementa a transação de saque.
- **Deposito:** Implementa a transação de depósito.

### Outras Classes:

- **Historico:** Mantém o histórico de transações realizadas em uma conta.

### Funções Principais:

- **menu:** Exibe o menu principal e retorna a opção selecionada pelo usuário.
- **filtrar_cliente:** Filtra clientes por CPF.
- **recuperar_conta_cliente:** Recupera uma conta de um cliente.
- **depositar:** Realiza a operação de depósito, garantindo que o valor informado seja válido.
- **sacar:** Realiza a operação de saque, garantindo que o valor informado seja válido.
- **exibir_extrato:** Exibe o extrato de uma conta.
- **criar_cliente:** Cria um novo cliente.
- **criar_conta:** Cria uma nova conta para um cliente existente.
- **listar_contas:** Lista todas as contas existentes.

### Funcionalidades Implementadas

- **Depósito:** Permite ao usuário depositar dinheiro em uma conta, com validação para garantir que o valor é numérico e positivo.
- **Saque:** Permite ao usuário sacar dinheiro de uma conta, com validação para garantir que o valor é numérico, positivo e dentro do limite permitido.
- **Extrato:** Exibe o histórico de transações e o saldo atual da conta.
- **Criação de Contas e Clientes:** Permite a criação de novos clientes e contas correntes.
- **Listagem de Contas:** Lista todas as contas com detalhes como agência, número e titular.

### Como Usar

- **Iniciar o Programa:** Execute a função `main()` para iniciar o programa e acessar o menu principal.
- **Interagir com o Menu:** O menu apresenta opções para depositar, sacar, exibir extrato, criar nova conta, listar contas, criar novo usuário e sair.

![Captura de tela 2024-05-31 210317](https://github.com/Gabrielsouza2000/Desafios-Python/assets/157544303/7eb774b2-c2b9-4b72-9757-3778129c6e75)


## Sobre-mim

Sou um estudante de desenvolvimento web que adora programar, resolver problemas e ajudar pessoas. também gosto de músicas, videogame e da minha família.
