"""向量存储模块：ChromaDB + BGE 中文 embedding 实现 RAG 语义检索"""
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from config import BASE_DIR


# ============ 配置 ============
CHROMA_DIR = BASE_DIR / "data" / "chroma"
EMBED_MODEL_NAME = "BAAI/bge-small-zh-v1.5"


# ============ 单例：模型和客户端只加载一次 ============
_client = None
_collection = None
_model = None


def _init():
    """懒加载，第一次调用时初始化"""
    global _client, _collection, _model
    if _collection is not None:
        return

    print("正在初始化向量库...")
    # 1. 初始化 ChromaDB（持久化到本地）
    _client = chromadb.PersistentClient(path=str(CHROMA_DIR))

    # 2. 获取或创建 collection
    _collection = _client.get_or_create_collection(
        name="memory",
        metadata={"hnsw:space": "cosine"}   # 余弦相似度
    )

    # 3. 加载中文 embedding 模型
    print("正在加载 BGE 中文 embedding 模型（首次会下载，约 100MB）...")
    _model = SentenceTransformer(EMBED_MODEL_NAME)
    print("向量库初始化完成！")


def _embed(texts):
    """把文本转成向量"""
    _init()
    return _model.encode(texts, normalize_embeddings=True).tolist()


def add_memory(key: str, value: str):
    """把一条记忆写入向量库"""
    _init()
    # 用 "key: value" 作为语义文本
    text = f"{key}: {value}"
    vec = _embed([text])[0]
    _collection.upsert(
        ids=[key],
        embeddings=[vec],
        documents=[text],
        metadatas=[{"key": key, "value": value}]
    )


def search_memory(query: str, top_k: int = 3):
    """语义检索，返回最相近的 top_k 条记忆"""
    _init()
    if _collection.count() == 0:
        return []

    query_vec = _embed([query])[0]
    results = _collection.query(
        query_embeddings=[query_vec],
        n_results=min(top_k, _collection.count())
    )

    items = []
    if results and results["metadatas"]:
        for meta in results["metadatas"][0]:
            items.append((meta["key"], meta["value"]))
    return items


def delete_memory_vector(key: str):
    """从向量库删除一条记忆"""
    _init()
    try:
        _collection.delete(ids=[key])
    except Exception:
        pass