# Gurgel Park Desktop

## Descrição
Gurgel Park Desktop é um aplicativo de gerenciamento de estacionamento desenvolvido em Python, utilizando a arquitetura MVC (Model-View-Controller). Este sistema permite o controle eficiente de vagas de estacionamento, veículos e clientes.

## Funcionalidades
- Cadastro e gerenciamento de vagas de estacionamento
- Controle de entrada e saída de veículos
- Cadastro de clientes
- Histórico de estacionamentos
- Interface gráfica intuitiva

## Requisitos
- Python 3.8 ou superior
- Dependências listadas em `requirements.txt`

## Estrutura do Projeto
```
gurgel-park-desktop/
├── models/          # Classes de modelo e lógica de negócios
├── views/           # Interface gráfica e componentes visuais
├── controllers/     # Controladores que gerenciam a interação
└── main.py          # Ponto de entrada da aplicação
```

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/gurgel-park-desktop.git
cd gurgel-park-desktop
```

2. Crie um ambiente virtual (recomendado):
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Como Executar
```bash
python main.py
```

## Tecnologias Utilizadas
- Python
- PyQt5 (Interface gráfica)
- MySQL (Banco de dados)
- Arquitetura MVC


## Licença
Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.
