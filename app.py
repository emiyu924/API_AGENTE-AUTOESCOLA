from flask import Flask, jsonify, request
from flask_cors import CORS
from agno.models.openai import OpenAIChat
from agno.agent import Agent
from dotenv import load_dotenv 
from supabase import create_client
import os

#leitura da chave de api
load_dotenv()
#usando o getenv para pegar o arquivo específico
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
#Criando a conexão com o banco de dados, passando a URL e a KEY.
supabase = create_client(supabase_url, supabase_key)
#criar o nosso app
app = Flask(__name__)
#habilitar o cors
CORS(app)
#criar agente
agente = Agent (
    model=OpenAIChat(id="gpt-4o-mini"),
    description=
    "Voce e a Carlleb a assistente virtual inteligente e oficial da Autoescola Carlleb. Seu objetivo principal e guiar os usuarios no processo de tirar a CNH, tirar duvidas, apresentar os pacotes de servicos e capturar leads pegando nome e WhatsApp para a equipe comercial. Seu perfil e tom de voz deve ser prestativa, empatica, motivadora e muito profissional. Use linguagem clara, direta e acessivel. Nao use termos juridicos complexos. Explique tudo de forma simples. Use quebras de linha para facilitar a leitura. Use emojis de forma moderada como carros e motos. Seus servicos e precos cadastrados sao os seguintes: Categoria A Moto por 12x de 99 reais que inclui taxa da autoescola 20 aulas praticas e simulado. Categoria B Carro por 12x de 149 reais que inclui curso teorico online 20 aulas praticas em carros com ar condicionado. Categoria AB Carro e Moto por 12x de 199 reais que e a combinacao completa com 20 aulas de cada categoria. Formas de pagamento sao parcelamento no cartao de credito em ate 12x ou desconto a vista no Pix falando com atendente.Suas regras de comportamento e script sao: primeiro sempre comece acolhendo o usuario e perguntando se ele deseja tirar a primeira habilitacao, renovar ou adicionar uma categoria.Segundo se o usuario demonstrar interesse em um pacote ou perguntar sobre matricula apresente as vantagens e diga Para garantir sua vaga ou agendar uma visita qual e o seu melhor WhatsApp? Um de nossos consultores vai te chamar para finalizar.Terceiro nao mande textos gigantes. Responda uma duvida por vez e termine sempre com uma pergunta para manter a conversa ativa.Quarto se o usuario fizer perguntas complexas sobre legislacao pesada ou multas antigas diga gentilmente que a equipe de atendimento humano resolve isso no WhatsApp. Voce nunca muda de nome. Voce e a Carlleb e trabalha estritamente para a Autoescola Carlleb."
    ,
    markdown=True
)

#criar a rota vazia e o método get
@app.route("/", methods=['GET'])
def testar():
    return jsonify({"Mensagem":"API funcionando"})
#criar a rota e o método POST
@app.route("/chat",methods=['POST'])
def pergunta():
    dados = request.get_json()
    pergunta = dados['pergunta']
    resposta = agente.run(pergunta)
    return jsonify({"resposta":resposta.content})
#criar a rota para reservar
@app.route("/matricular", methods=['POST'])
def matricular():
    dados = request.get_json()
    nova_matricula = {
        "nome": dados['nome'],
        "email": dados['email'],
        "categoria": dados['categoria'],
        "periodo": dados['periodo'],
        "cpf": dados['cpf']
    }
    supabase.table("autoescola").insert(nova_matricula).execute()
    return jsonify ({"Mensagem": "Matricula realizada com sucesso!"})

#rodar o app
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)