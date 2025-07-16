from dotenv import load_dotenv
import os
from typing import Optional
from pydantic import BaseModel, Field

from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser

# Carrega .env
load_dotenv()

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama").lower()

# === LLM selection ===
llm = None
if LLM_PROVIDER == "openai":
    from langchain_community.chat_models import ChatOpenAI
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
    # Necessário ter uma API KEY em plataform https://platform.openai.com
    # Necessário adicionar o cartão de crédito

elif LLM_PROVIDER == "ollama":
    from langchain_community.chat_models import ChatOllama
    llm = ChatOllama(model=os.getenv("OLLAMA_MODEL", "llama3"))
    # Acima de 5.9 de ram (ambiente local)

# Opção com modelos gratuitos sem a necessidade de um LLM local
elif LLM_PROVIDER == "openrouter":
    from langchain_community.chat_models import ChatOpenAI

    api_key = os.getenv("OPENROUTER_API_KEY")
    model_name = os.getenv("OPENROUTER_MODEL", "mistralai/mistral-7b-instruct:free")

    # Configure o endpoint OpenRouter
    llm = ChatOpenAI(
        temperature=0,
        model_name=model_name,
        openai_api_key=api_key,
        openai_api_base="https://openrouter.ai/api/v1",
        max_tokens=1024
    )

else:
    raise ValueError("LLM_PROVIDER inválido. Use 'openai', 'ollama' ou 'openrouter'.")

# === Schema de filtros ===
class FiltrosVeiculo(BaseModel):
    marca: Optional[str] = Field(None, description="Marca do carro")
    modelo: Optional[str] = Field(None, description="Modelo do carro")
    ano: Optional[int] = Field(None, description="Ano mínimo")
    motorizacao: Optional[float] = Field(None, description="Motorização do carro")
    combustivel: Optional[str] = Field(None, description="Tipo de combustível")
    cor: Optional[str] = Field(None, description="Cor do carro")
    quilometragem: Optional[int] = Field(None, description="Quilometragem do carro")
    portas: Optional[int] = Field(None, description="Portas do carro")
    transmissao: Optional[str] = Field(None, description="Transmissão do carro")
    preco_max: Optional[float] = Field(None, description="Preço máximo")

parser = PydanticOutputParser(pydantic_object=FiltrosVeiculo)

template = """
Você é um assistente que transforma buscas em linguagem natural em filtros estruturados para busca de carros.

Extraia os seguintes campos:
- marca (string)
- modelo (string)
- ano (inteiro, mínimo)
- motorizacao (float)
- combustivel (string: gasolina, etanol, flex, diesel, etc)
- cor (string)
- quilometragem (inteiro)
- portas (inteiro)
- transmissao (string)
- preco_max (float, em reais)

{format_instructions}

Exemplo:
Frase do usuário: "quero um sedan automático da Honda até 70 mil reais, a partir de 2020"
Resposta:
{{
  "marca": "Honda",
  "modelo": null,
  "ano": 2020,
  "motorizacao": 3.2,
  "combustivel": null,
  "cor": "Branco",
  "quilometragem": 123612,
  "portas": 4,
  "transmissao": "Automática",
  "preco_max": 70000.0
}}

Frase do usuário: {user_input}
"""

prompt = PromptTemplate(
    template=template,
    input_variables=["user_input"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

# Função principal com fallback e logs
def interpretar_filtros(user_input: str):
    try:
        _input = prompt.format_prompt(user_input=user_input)
        output = llm.invoke(_input.to_messages())
        filtros = parser.parse(output.content)

        # Loga sucesso
        log_interacao(user_input, filtros.dict(), success=True)
        return filtros

    except Exception as e:
        # Loga erro
        log_interacao(user_input, str(e), success=False)
        print("[bold red]Erro ao interpretar sua busca.[/bold red]")
        print(f"[dim]Detalhes: {e}[/dim]")
        return None

# Logger básico em arquivo
def log_interacao(entrada, saida, success=True):
    os.makedirs("logs", exist_ok=True)
    with open("logs/agent.log", "a") as f:
        status = "SUCESSO" if success else "FALHA"
        f.write(f"\n[{status}]\nEntrada: {entrada}\nSaída: {saida}\n")
