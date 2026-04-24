from google.adk.agents.llm_agent import Agent
from trello import TrelloClient
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()

#suas credenciais do Trello
API_KEY = os.getenv('TRELLO_API_KEY')
API_SECRET = os.getenv('TRELLO_API_SECRET')
TOKEN = os.getenv('TRELLO_TOKEN')


def get_temporal_context():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")
   
def adicionar_tarefa(nome_da_task: str, descricao_da_task: str, due_date: str):

    client = TrelloClient(
        api_key=API_KEY,
        api_secret=API_SECRET,
        token=TOKEN
    )

    client.list_boards()
    #obter o board (você precisa do ID ou nome do board)
    boards = client.list_boards()
    meu_board = [b for b in boards if b.name == 'DIO'][0]

    #obter a lista onde adiciconar o card
    listas = meu_board.list_lists()

    minha_lista = [l for l in listas if l.name.upper() == 'TO DO' or l.name.upper() == 'A FAZER'][0]
    #adicionar o card
        #Criar o card
    minha_lista.add_card(
        name=nome_da_task,
        desc=descricao_da_task,
        due=due_date
        )

def listar_tarefas(status: str = "todas"):
    client = TrelloClient(
        api_key=API_KEY,
        api_secret=API_SECRET,
        token=TOKEN
    )
    boards = client.list_boards()
    #obter o board (você precisa do ID ou nome do board)
    meu_board = [b for b in boards if b.name == 'DIO'][0]
    #obter as listas
    listas = meu_board.list_lists()

    if status.lower() == "todas":
        listas_filtadas = listas
    elif status.lower() == "a fazer":
        listas_filtadas = [l for l in listas if l.name.upper() in ['TO DO', 'A FAZER', 'TODO']]
    elif status.lower() == "em andamento":
        listas_filtadas = [l for l in listas if l.name.upper() in ['EM ANDAMENTO', 'IN PROGRESS', 'DOING']]
    elif status.lower() == "concluído":
        listas_filtadas = [l for l in listas if l.name.upper() in ['CONCLUÍDO', 'DONE', 'COMPLETED', 'CONCLUIDO']]
    else:
        listas_filtadas = listas
    
    tarefas = []

    for lista in listas_filtadas:
        cards = lista.list_cards()
        for card in cards:
            tarefas.append({
                'nome': card.name,
                'descricao': card.desc,
                'vencimento': card.due_date,
                'status': lista.name,
                "id": card.id               
            })
    return tarefas

def mudar_status_tarefa(nome_da_task: str, novo_status: str) -> str:
    try:
        client = TrelloClient(
            api_key=API_KEY,
            api_secret=API_SECRET,
            token=TOKEN
        )
        boards = client.list_boards()
        #obter o board (você precisa do ID ou nome do board)
        meu_board = [b for b in boards if b.name == 'DIO'][0]
   
        #mudar o status para listas
        status_map= {
            "a fazer": ['TO DO', 'A FAZER', ],
            "em andamento": ['EM ANDAMENTO', 'IN PROGRESS', 'DOING'],
            "concluído": ['CONCLUÍDO', 'DONE', 'COMPLETED', 'CONCLUIDO']
        }

        nome_lista_destino = status_map.get(novo_status.lower())
        
        if not nome_lista_destino:
            return f"Status Inválido. Use: 'A Fazer', 'Em Andamento' ou 'Concluído'."

        #obter as listas
        listas = meu_board.list_lists()

        #Encontrar lista de destino
        nome_lista_destino = next(
            (l for l in listas if l.name.upper() in nome_lista_destino),
            None
        )

        #Buscar o card em todas as listas
        card_encontrado = None
        lista_origem = None
        for lista in listas:
            cards = lista.list_cards()
            card_encontrado = next(
                (c for c in cards if c.name.lower() == nome_da_task.lower), 
                None
            )
            if card_encontrado:
                lista_origem = lista
                break
        
        if not card_encontrado:
            return f"Card '{nome_da_task}' não encontrada."

        #Mover
        card_encontrado.change_list(nome_lista_destino.id)
        return f"Card '{nome_da_task}': {lista_origem.name} -> {nome_lista_destino.name}"

    except Exception as e:
        return f"Erro ao mudar status da tarefa: {str(e)}"          




root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='Você é um agente organizador de tarefas',
    instruction="""
        Você é um agente organizador de tarefas.
        Sua função é receber uma tarefa e criar um card no Trello com o nome e descrição da tarefa.
        Você deve perguntar as atividades que tenho no dia e criar um card para cara uma delas.
        Você inicia a convesa assim que for atisado, perguntandoquais são as tarefas do dia.
        Sempre inicie a conversa perguntando quais são as tarefas do dia informando a data pela tool get_temporal_context,
        e depois vá perguntando se tem mais algumas tarefas, até qye i usuário diga que não tem mais tarefas para adicionar.
        suas funções são:
        1. Adicionar novas tarefas com nome e descrição
        2. Listar todas as tarefas ou filtrar por status
        3. Marcar tarefas como concluídas
        4. Remover tarefas da lsita
        5. Mudasr o status de uma tarefa (ex: "A Fazer" para "Em Andamento" e de "Em Andamento" para "Concluído")
        6. Gerar contexto temporal (data e hora atual) para organizar as tarefas do dia
""",

    tools={get_temporal_context, adicionar_tarefa, listar_tarefas, mudar_status_tarefa}

)
