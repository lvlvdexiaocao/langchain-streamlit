from langchain_community.document_loaders import PDFPlumberLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS

# 1. 上传/加载原始 PDF

pdfs_directory = './data'

def upload_pdf(file):
    with open(pdfs_directory+file.name, "wb") as f:
        f.write(file.getbuffer())

def load_pdf(file_path):
    loader = PDFPlumberLoader(file_path)
    documents = loader.load()
    return documents

filepath = "./data/DeepSeek_V3论文（中文版）.pdf"
document = load_pdf(filepath)
# # print(len(documents))


# 2.分块

def create_chunks(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        add_start_index=True
    )
    text_chunks = text_splitter.split_documents(documents)
    return text_chunks

text_chunk = create_chunks(document)
# print("Chunks Count:::",len(text_chunks))

# 3.设置嵌入模型（自由选择）
ollama_model = "quentinz/bge-small-zh-v1.5:f16"
def get_embedding_model(ollama_model_name):
    embeddings = OllamaEmbeddings(model=ollama_model_name)
    return embeddings
# 4.索引文档，使用FAISS（向量数据库）
FAISS_DB_PATH = "vectorstore/db_faiss"
faiss_db = FAISS.from_documents(text_chunk,get_embedding_model(ollama_model))
faiss_db.save_local(FAISS_DB_PATH)