# Car IA Terminal

Este projeto é um desafio técnico para a vaga de Desenvolvedor Python na C2S.

## Funcionalidades

- Busca de veículos com filtros personalizados
- Comunicação cliente-servidor via protocolo MCP
- Interação via agente virtual no terminal (sem menus)
- Dados fictícios com SQLAlchemy + Faker
- Testes automatizados

## Como executar

```bash
# Instale as dependências
pip install -r requirements.txt

# Popule o banco com dados simulados
python database/seed.py

# Execute a aplicação no terminal
python run.py

# Se for usar o spaCy, não esqueça de baixar um modelo de idioma (ex: pt_core_news_sm):
python -m spacy download pt_core_news_sm
