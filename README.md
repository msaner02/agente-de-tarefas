# 🗂️ Agente Gerenciador de Tarefas com Trello

Este projeto implementa um **agente inteligente de gerenciamento de tarefas**, integrado diretamente à **API do Trello**, utilizando Python e o **Agent Development Kit (ADK)** com modelos Gemini.

O agente permite **criar, listar e atualizar o status de tarefas** de forma automatizada, mantendo a organização do quadro Trello de maneira simples e eficiente.

***

## 🚀 Funcionalidades

O agente suporta as seguintes operações:

*   ➕ **Adicionar tarefas**
    *   Cria cards no Trello com nome, descrição e data de vencimento.
    *   As tarefas são adicionadas automaticamente à lista *A Fazer / To Do*.

*   📋 **Listar tarefas**
    *   Lista todas as tarefas do board.
    *   Permite filtrar por status:
        *   A Fazer
        *   Em Andamento
        *   Concluído

*   🔄 **Mudar status de tarefas**
    *   Move um card entre listas do Trello, por exemplo:
        *   *A Fazer → Em Andamento*
        *   *Em Andamento → Concluído*

*   🕒 **Contexto temporal**
    *   Retorna data e hora atual quando solicitado, auxiliando na organização diária.

***

## 🧠 Como o agente funciona

*   O agente interpreta comandos do usuário e decide **quando utilizar as funções (tools)**.
*   As funções são responsáveis por interagir diretamente com o Trello via API.
*   O prompt do agente foi otimizado para:
    *   Reduzir consumo de tokens
    *   Evitar perguntas ou ações automáticas desnecessárias
    *   Executar apenas ações explicitamente solicitadas pelo usuário

***

## 🛠️ Tecnologias utilizadas

*   **Python 3**
*   **Trello API**
*   **Agent Development Kit (ADK)**
*   **Google Gemini (flash / pro)**
*   **python-trello**
*   **dotenv**

***

## 📌 Estrutura do projeto

*   Funções principais:
    *   `get_temporal_context`
    *   `adicionar_tarefa`
    *   `listar_tarefas`
    *   `mudar_status_tarefa`
*   Um agente (`Agent`) que orquestra chamadas ao modelo e às tools
*   Integração segura via variáveis de ambiente (`.env`)

***

## ✅ Benefícios

*   Automatiza o gerenciamento de tarefas no Trello
*   Evita trabalho manual repetitivo
*   Fácil de expandir (ex: remover tarefa, múltiplos boards, API REST)
*   Código modular e organizado
*   Prompt otimizado para economia de tokens e menor custo

***

## 📂 Exemplo de uso

```text
Usuário: adicionar tarefa Estudar Python hoje
Usuário: listar tarefas a fazer
Usuário: mover Estudar Python para concluído
```

***

## 🧩 Possíveis evoluções

*   Remover tarefas
*   Suporte a múltiplos boards
*   Interface Web ou API com FastAPI
*   Suporte a outros provedores de LLM (Azure OpenAI, OpenAI)

***

