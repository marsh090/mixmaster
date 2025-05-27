# MixMaster

MixMaster é uma plataforma inovadora que utiliza IA para ajudar usuários a descobrir, experimentar, modificar e criar receitas de drinks, tanto alcoólicos quanto não alcoólicos.

## Tecnologias Principais

- Django REST Framework
- MongoDB
- Google Gemini AI
- Celery
- Redis
- Poetry

## Configuração do Ambiente de Desenvolvimento

1. Clone o repositório
```bash
git clone https://github.com/marsh090/mixmaster.git
cd mixmaster
```

2. Configure o ambiente virtual e instale as dependências
```bash
poetry install
```

3. Configure as variáveis de ambiente
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

4. Execute o projeto
```bash
docker-compose up -d
```

## Estrutura do Projeto

```
mixmaster/
├── apps/
│   ├── users/               # Autenticação e perfil de usuário
│   ├── drinks/             # Modelos e lógica de drinks
│   ├── chats/              # Gestão de conversas com IA
│   └── ai/                 # Tudo relacionado à integração com Gemini e RAG
├── config/
│   ├── __init__.py
│   ├── settings/
│   │   ├── base.py         # Configurações comuns
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py             # Rotas principais
│   └── asgi.py
├── .env                    # Variáveis de ambiente
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```


## Documentação da API

[Ainda a ser escrita]