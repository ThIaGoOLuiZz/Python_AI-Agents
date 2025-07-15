# Assistente de Viagens ✈️
Um assistente de IA especializado em planejamento de viagens, construído com LangChain e OpenAI GPT-4o-mini. O sistema fornece sugestões personalizadas de destinos, roteiros detalhados e dicas práticas para suas viagens.

## Características

- **Assistente Especializado**: IA focada exclusivamente em viagens e turismo
- **Memória de Conversa**: Mantém o histórico da conversa para um contexto contínuo
- **Sugestões Inteligentes**: Roteiros, dicas práticas e recomendações personalizadas
- **Planejamento Personalizado**: Adaptado para número de pessoas, duração e destino
- **Interface Simples**: Interação via linha de comando

## Pré-requisitos

- Python 3.8+
- Conta OpenAI com API key
- Pacotes Python listados em ´requirements.txt´

## Instalação

1. Clone o repositório:

```bash
git clone <url-do-repositorio>
cd assistente-viagens
```

2. Instale as dependências:
```bash
bashpip install -r requirements.txt
```

3. Configure as variáveis de ambiente:


```bash
# Crie um arquivo .env na raiz do projeto
echo "OPENAI_API_KEY=sua_api_key_aqui" > .env
```

## Dependências
```txt
langchain-openai
langchain-core
langchain-community
python-dotenv
```

## Uso
Execute o assistente:
```bash
bashpython main.py
```

O assistente iniciará uma conversa perguntando sobre:

- Destino da viagem
- Número de pessoas
- Duração da viagem

Exemplo de Uso
Bem-vindo ao Assistente de Viagens!
Você: Quero viajar para Paris
Assistente: Que ótimo! Paris é um destino maravilhoso. Para te ajudar melhor, preciso saber:
- Com quantas pessoas você vai viajar?
- Por quantos dias planeja ficar?

Você: Vou com minha esposa por 5 dias
Assistente: Perfeito! Para uma viagem romântica de 5 dias em Paris, aqui está minha sugestão de roteiro...
Para encerrar a conversa, digite: sair, exit ou quit
Estrutura do Projeto
assistente-viagens/
├── main.py              # Arquivo principal
├── .env                 # Variáveis de ambiente (não commitado)
├── requirements.txt     # Dependências
└── README.md           # Este arquivo
Funcionalidades
Sistema de Memória

Mantém histórico da conversa por sessão
Contexto contínuo durante toda a interação
Armazenamento temporário em memória

Personalização

Adaptação baseada em número de viajantes
Consideração da duração da viagem
Sugestões específicas por destino

Comandos Disponíveis

sair / exit / quit: Encerra o assistente
Qualquer pergunta sobre viagens será processada

Configuração Avançada
Parâmetros do Modelo
pythonllm = ChatOpenAI(
    temperature=0.7,    # Controla criatividade (0.0 - 1.0)
    model="gpt-4o-mini" # Modelo utilizado
)
Sessões
O sistema utiliza um ID de sessão fixo (user123) para manter o histórico. Para múltiplos usuários, modifique a função iniciar_assistente() para gerar IDs únicos.