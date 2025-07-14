# ============================
# README.md
# ============================

# 🚗 CarFinder

Aplicação interativa de busca de veículos no terminal, com comunicação entre cliente e servidor via protocolo MCP (Model Context Protocol). Este projeto foi desenvolvido como parte do desafio técnico para a vaga de Desenvolvedor Python na C2S.

---

## 🧭 Estrutura do Projeto

```
carfinder/
├── 🧠 agent/                      # Agente virtual (chat com o usuário no terminal)
│   └── main.py                   # Lógica de perguntas e interação com o usuário final
│
├── 📡 client/                    # Cliente MCP (camada de comunicação)
│   └── client.py                 # Envia os filtros da busca ao servidor
│
├── 🖥️ server/                    # Servidor MCP (lida com a lógica de busca)
│   ├── server.py                 # Interpreta filtros e responde com dados do banco
│   └── handlers.py              # [Opcional] lógica auxiliar para futuras extensões
│
├── 🗃️ database/                  # Banco de dados local com SQLAlchemy
│   ├── models.py                # Modelo da tabela `Veiculo`
│   ├── seed.py                  # Script para gerar dados falsos (100 veículos)
│   └── db.py                    # Conexão e criação do SQLite
│
├── 🧪 tests/                     # Testes automatizados com pytest
│   └── test_agent.py            # Testa a montagem de filtros e integração básica
│
├── 📦 requirements.txt          # Lista de dependências do projeto
├── 📖 README.md                 # Documentação e instruções de uso
└── 🚀 run.py                     # Ponto de entrada da aplicação no terminal
```

---

## ⚙️ Como executar o projeto

### 1. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 2. Popular o banco com dados simulados

```bash
python database/seed.py
```

### 3. Executar a aplicação

```bash
python run.py
```

### 4. Rodar os testes

```bash
pytest
```

---

### 5. Se for usar o spaCy, não esqueça de baixar um modelo de idioma (ex: pt_core_news_sm):

```bash
python -m spacy download pt_core_news_sm
```

---

## 🧩 Fluxo da Aplicação

```
Usuário
  │
  ▼
agent/ ➝ client/ ➝ server/ ➝ database/
                ⬅         ⬅
              Resposta formatada com carros compatíveis
```

---

## ✅ Funcionalidades

- Chat com agente virtual no terminal (nada de menu fixo!)
- Filtros flexíveis: marca, modelo, ano, combustível, preço
- Banco SQLite com 100 veículos gerados via Faker
- Arquitetura cliente-servidor com protocolo MCP
- Teste automatizado básico com pytest

---

## 👨‍💻 Desenvolvido para: C2S | Vaga Python Developer

Projeto com fins de avaliação técnica, mas desenvolvido com cuidado real para ser usado e expandido como exemplo profissional.
