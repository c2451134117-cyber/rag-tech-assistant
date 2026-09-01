import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

def main():
    # 1. 加载本地向量库
    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-zh-v1.5")
    vector_store = Chroma(
        persist_directory="./chroma_db",
        embedding_function=embeddings
    )
    # 检索相关度最高的 4 个段落
    retriever = vector_store.as_retriever(search_kwargs={"k": 4})

    # 2. 配置 DeepSeek LLM
    llm = ChatOpenAI(
        model="deepseek-chat",
        api_key=os.getenv("sk-0cb600ce5ffe43bda9548bfb931a7ccc"),
        base_url=os.getenv("https://api.deepseek.com"),
        temperature=0.2
    )

    # 3. 设定 Prompt 提示词模板
    prompt = ChatPromptTemplate.from_template("""
    你是一个精通嵌入式系统与芯片架构的技术助手。请根据以下从《STM32F10xxx参考手册》中检索到的英文参考资料，用中文准确、专业地回答用户的问题。
    如果资料中没有提到相关信息，请明确回答“参考手册中未找到相关内容”，不要随意编造寄存器或配置细节。
【回答要求】
    1. 解释相关外设的工作原理、关键寄存器及配置流程。
    2. 如果用户的问题涉及初始化、外设配置或功能实现，请务必提供清晰、规范的 C 语言代码示例（可使用标准外设库/HAL 库或直接操作寄存器，并附带关键代码注释）。
    3. 如果资料中没有提及相关信息，请明确说明“参考资料中未找到”，不要捏造不存在的寄存器位。

    【参考资料】
    {context}

    【用户问题】
    {question}
    """)

    # 4. 构建检索生成链 (LCEL)
    rag_chain = (
        {"context": retriever | (lambda docs: "\n\n".join(d.page_content for d in docs)),
         "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    print("\n==========================================")
    print("STM32F10xxx 参考手册问答助手已就绪！")
    print("输入你的问题即可开始查询，输入 'exit' 或 'quit' 退出。")
    print("==========================================")

    while True:
        query = input("\n请输入问题: ").strip()
        if query.lower() in ["exit", "quit", "q"]:
            print("再见！")
            break
        if not query:
            continue
        
        print("\n正在检索手册并生成回答...")
        try:
            response = rag_chain.invoke(query)
            print(f"\n【回答】:\n{response}")
        except Exception as e:
            print(f"\n[错误] 请求失败: {e}")

if __name__ == "__main__":
    main()