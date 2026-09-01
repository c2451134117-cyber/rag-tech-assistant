\# Local-RAG-Assistant



基于 \*\*LangChain\*\*、\*\*DeepSeek API\*\* 与本地 \*\*BGE 向量模型\*\* 搭建的本地 PDF / 网页技术文档检索与问答助手。



&#x20;核心特性

\- \*\*混合架构\*\*：本地端运行轻量级 Embedding (`BAAI/bge-small-zh-v1.5`)，云端调用 DeepSeek 进行高精度推理。

\- \*\*持久化向量检索\*\*：使用 ChromaDB 建立本地语义索引，避免重复解析。

\- \*\*低成本 \& 高隐私\*\*：文本向量化完全免费离线，仅在提问时消耗极少量 LLM Token。



\## 🚀 快速上手



\### 1. 环境准备

```bash

git clone [https://github.com/c2451134117-cyber/rag-tech-assistant.git](https://github.com/c2451134117-cyber/rag-tech-assistant.git)
cd rag-tech-assistant


\# 创建并激活虚拟环境

python -m venv venv

venv\\Scripts\\activate  # Linux/macOS 使用: source venv/bin/activate



\# 安装依赖

pip install -r requirements.txt

