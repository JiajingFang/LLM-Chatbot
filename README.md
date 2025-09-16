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
feat:
impl rag

infra:
save user token in db
add Dockerfile

add more tests