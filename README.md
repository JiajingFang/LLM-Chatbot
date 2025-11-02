# LLM-Chatbot

```bash
llm_api/
├── llm_api/                
│   ├── __init__.py
│   ├── main.py             # FastAPI entry point
│   ├── config.py           # config（API Key. model name）
│   ├── services/           # LLM call logic
│   │   ├── __init__.py
│   │   └── chat_service.py
│   │   └── comparison.py
│   ├── rag/                # wip RAG
│   │   ├── __init__.py
│   │   └── retriever.py
│   └── utils/              # utils
│       ├── __init__.py
│       └── logger.py
├── tests/                  # test
│   └── test_chat.py
├── pyproject.toml           # Poetry setting
├── poetry.lock              # poetry dependency
├── Dockerfile               # wip
└── README.md

```

# todo
1 show the answer better and change to english

2 jwt and login page

3 separate collection for compare and chat prompt

4 save the answer

5 auto deploy in git env(in react_deployment_guide local)
