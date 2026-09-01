import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# 1. 加载环境变量配置（如 API KEY）
load_dotenv()

def load_and_split(pdf_path: str = None, web_url: str = None):
    docs = []
    
    # 解析本地 PDF
    if pdf_path and os.path.exists(pdf_path):
        print(f"正在加载本地 PDF 文件: {pdf_path}")
        loader = PyPDFLoader(pdf_path)
        docs.extend(loader.load())
    elif pdf_path:
        raise FileNotFoundError(f"未找到指定的 PDF 文件，请核对路径: {pdf_path}")
    
    # 解析在线网页
    if web_url:
        print(f"正在加载网页: {web_url}")
        loader = WebBaseLoader(web_url)
        docs.extend(loader.load())

    if not docs:
        raise ValueError("请提供有效的 PDF 路径或网页 URL。")

    print(f"文档加载完成，共提取 {len(docs)} 页/篇原始数据。开始分块...")

    # 针对芯片参考手册等技术文档进行分块切分
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,      # 每个切片块的字符数
        chunk_overlap=120,   # 切片之间的重叠字符数，防止边界断句丢语义
        separators=["\n\n", "\n", "。", "！", "？", ".", ";", " ", ""]
    )
    chunks = splitter.split_documents(docs)
    print(f"切分完成，共生成 {len(chunks)} 个文本块。")
    return chunks

def build_vector_store(chunks, db_path="./chroma_db"):
    print("正在加载向量模型 (BAAI/bge-small-zh-v1.5)，首次加载会自动下载模型权重...")
    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-zh-v1.5")
    
    print("正在将文本块转化为向量并存入本地 ChromaDB 数据库，请稍候...")
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=db_path
    )
    print(f"\n==========================================")
    print(f"向量库构建成功！数据已持久化保存在本地: '{db_path}'")
    print(f"==========================================")

if __name__ == "__main__":
    # Windows 标准路径（加 r 防止转义）
    target_pdf = r"D:\BaiduNetdiskDownload\STM32入门教程资料\参考文档\STM32F10xxx参考手册（英文）.pdf"
    
    # 执行加载与向量化
    doc_chunks = load_and_split(pdf_path=target_pdf)
    build_vector_store(doc_chunks)