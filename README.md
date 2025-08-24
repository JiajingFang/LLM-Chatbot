# LLM-Chatbot

```bash
llm_api/
├── llm_api/                # 实际包
│   ├── __init__.py
│   ├── main.py             # FastAPI 入口
│   ├── config.py           # 配置（API Key、模型参数）
│   ├── services/           # LLM 调用逻辑
│   │   ├── __init__.py
│   │   └── chat_service.py
│   ├── rag/                # 可选 RAG 模块
│   │   ├── __init__.py
│   │   └── retriever.py
│   └── utils/              # 工具函数
│       ├── __init__.py
│       └── logger.py
├── tests/                  # 单元测试
│   └── test_chat.py
├── pyproject.toml           # Poetry 配置
├── poetry.lock              # 锁定依赖
├── Dockerfile               # 部署用
└── README.md

```

# todo

hide open_api_key