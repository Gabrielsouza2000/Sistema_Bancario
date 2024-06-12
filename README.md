# Gabriel Souza

## Conecte-se comigo

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/gabriel-souza-10421621b/)

[![Instagram](https://img.shields.io/badge/-Instagram-%23E4405F?style=for-the-badge&logo=instagram&logoColor=white)](https://www.instagram.com/gabrielssanx/)

[![Gmail](https://img.shields.io/badge/Gmail-333333?style=for-the-badge&logo=gmail&logoColor=red)](mailto:gabrielsouza3641@gmail.com)

## Futuras Atualizações

- interface grafica
- Salva o Saldo da conta




Atualmente, há 1 desafio:

# Sistema Bancário em Python

Este projeto implementa um sistema básico de banco em Python. A aplicação permite a criação de clientes, contas bancárias e oferece funcionalidades como depósitos, saques e visualização de extratos. O sistema é baseado em orientação a objetos e inclui as principais classes: `Cliente`, `PessoaFisica`, `Conta`, `ContaCorrente`, `Historico` e `Transacao`.

## Principais Funcionalidades

1. **Criação de Clientes e Contas Bancárias**
   - Cadastro de clientes do tipo pessoa física.
   - Criação de contas correntes associadas aos clientes.

2. **Operações Bancárias**
   - Depósitos em conta.
   - Saques de conta com verificação de limite e número de saques permitidos.
   - Visualização de extrato de transações.

3. **Histórico de Transações**
   - Registro e consulta de transações realizadas em cada conta.

4. **Persistência de Dados**
   - Salvamento e carregamento de dados de clientes e contas em um arquivo de log.

## Estrutura das Classes

- **Cliente**: Classe base para representar um cliente. Contém métodos para adicionar contas e realizar transações.
- **PessoaFisica**: Subclasse de Cliente que representa um cliente pessoa física. Adiciona atributos como nome, data de nascimento e CPF.
- **Conta**: Classe base para representar uma conta bancária. Contém métodos para operações básicas como depósito e saque.
- **ContaCorrente**: Subclasse de Conta que representa uma conta corrente. Adiciona atributos como limite de saque e número máximo de saques permitidos.
- **Historico**: Classe para armazenar e gerenciar o histórico de transações de uma conta.
- **Transacao**: Classe abstrata que define a interface para diferentes tipos de transações.
- **Deposito** e **Saque**: Subclasses de Transacao que implementam as operações de depósito e saque.

## Ferramentas de Desenvolvimento

- **Black**: Utilizado para formatação automática do código.
- **Flake8**: Utilizado para verificação de estilo e erros no código.
- **isort**: Utilizado para ordenar automaticamente as importações no código.


### Como Usar

- **Iniciar o Programa:** Execute a função `main()` para iniciar o programa e acessar o menu principal.
- **Interagir com o Menu:** O menu apresenta opções para depositar, sacar, exibir extrato, criar nova conta, listar contas, criar novo usuário e sair.

![Captura de tela 2024-05-31 210317](https://github.com/Gabrielsouza2000/Desafios-Python/assets/157544303/7eb774b2-c2b9-4b72-9757-3778129c6e75)

## Futuras Atualizações

### Interface Gráfica

Implementação de uma interface gráfica para melhorar a usabilidade do sistema e tornar as operações mais intuitivas para o usuário.

### Persistência de Saldo

Melhorar a persistência de dados para incluir o saldo de cada conta no arquivo de log, permitindo que o saldo atual de cada usuário seja salvo e carregado corretamente ao reiniciar a aplicação.


## Sobre-mim

Sou um estudante de desenvolvimento web que adora programar, resolver problemas e ajudar pessoas. também gosto de músicas, videogame e da minha família.
