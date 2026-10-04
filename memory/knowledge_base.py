"""知识库模块：加载技术文档 → 切分 → 向量化 → 存入 ChromaDB"""
import chromadb
from pathlib import Path
from sentence_transformers import SentenceTransformer
from config import BASE_DIR


CHROMA_DIR = BASE_DIR / "data" / "chroma_kb"
KNOWLEDGE_DIR = BASE_DIR / "knowledge"
EMBED_MODEL_NAME = "BAAI/bge-small-zh-v1.5"
CHUNK_SIZE = 400
CHUNK_OVERLAP = 50

_client = None
_collection = None
_model = None


def _init():
    """懒加载：第一次调用时初始化"""
    global _client, _collection, _model
    if _collection is not None:
        return
    print("正在初始化知识库...")
    _client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    _collection = _client.get_or_create_collection(
        name="knowledge",
        metadata={"hnsw:space": "cosine"}
    )
    _model = SentenceTransformer(EMBED_MODEL_NAME)
    print("知识库初始化完成！")


def _embed(texts):
    _init()
    return _model.encode(texts, normalize_embeddings=True).tolist()


def _chunk_text(text: str, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """按段落切分，超长硬切"""
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks = []
    current = ""
    for p in paragraphs:
        if len(current) + len(p) <= chunk_size:
            current += "\n\n" + p if current else p
        else:
            if current:
                chunks.append(current)
            if len(p) > chunk_size:
                for i in range(0, len(p), chunk_size - overlap):
                    chunks.append(p[i:i + chunk_size])
                current = ""
            else:
                current = p
    if current:
        chunks.append(current)
    return chunks


def load_documents():
    """加载 knowledge/ 下的所有 .md / .txt"""
    docs = []
    if not KNOWLEDGE_DIR.exists():
        print(f"⚠️ 知识库目录不存在：{KNOWLEDGE_DIR}")
        return docs
    for f in KNOWLEDGE_DIR.rglob("*"):
        if f.suffix.lower() in (".md", ".txt"):
            try:
                text = f.read_text(encoding="utf-8")
                docs.append((f.name, text))
            except Exception as e:
                print(f"读取 {f.name} 失败：{e}")
    return docs


def build_knowledge_base():
    """构建/重建知识库（每次启动时跑一遍）"""
    global _client, _collection, _model

    # 手动初始化（不用 _init，避免 collection 引用错乱）
    if _client is None:
        _client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    if _model is None:
        print("正在加载知识库 embedding 模型...")
        _model = SentenceTransformer(EMBED_MODEL_NAME)

    docs = load_documents()
    if not docs:
        print("知识库为空，跳过构建")
        return

    # 删除旧 collection（如果存在）
    try:
        _client.delete_collection("knowledge")
    except Exception:
        pass

    # 重新创建 collection，并赋值给全局变量
    _collection = _client.get_or_create_collection(
        name="knowledge",
        metadata={"hnsw:space": "cosine"}
    )

    ids, texts, metadatas = [], [], []
    for filename, text in docs:
        chunks = _chunk_text(text)
        for i, chunk in enumerate(chunks):
            ids.append(f"{filename}_{i}")
            texts.append(chunk)
            metadatas.append({"source": filename, "chunk_id": i})

    if not texts:
        return

    vectors = _model.encode(texts, normalize_embeddings=True).tolist()
    _collection.upsert(
        ids=ids,
        embeddings=vectors,
        documents=texts,
        metadatas=metadatas
    )
    print(f"✅ 知识库构建完成：{len(docs)} 个文档，{len(texts)} 个片段")


def search_knowledge(query: str, top_k: int = 3):
    """语义检索知识库"""
    _init()
    if _collection.count() == 0:
        return []
    query_vec = _embed([query])[0]
    results = _collection.query(
        query_embeddings=[query_vec],
        n_results=min(top_k, _collection.count())
    )
    items = []
    if results and results["documents"]:
        for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
            items.append({"content": doc, "source": meta["source"]})
    return items