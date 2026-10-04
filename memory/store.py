"""记忆存储模块：SQLite 存原文 + ChromaDB 存向量"""
import sqlite3
from config import DB_PATH
from memory.vector_store import add_memory, search_memory, delete_memory_vector


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT UNIQUE NOT NULL,
            value TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def save_memory(key: str, value: str) -> str:
    """保存或更新一条记忆（SQLite + 向量库 双写）"""
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute(
            "INSERT INTO memory (key, value) VALUES (?, ?) "
            "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
            (key, value)
        )
        conn.commit()
        # 同步写向量库
        add_memory(key, value)
        return f"已记住：{key} = {value}"
    except Exception as e:
        return f"保存失败：{e}"
    finally:
        conn.close()


def get_memory(key: str) -> str:
    """精确查询（SQLite，支持模糊匹配）"""
    conn = sqlite3.connect(DB_PATH)
    row = conn.execute("SELECT key, value FROM memory WHERE key = ?", (key,)).fetchone()
    if row:
        conn.close()
        return f"{row[0]} 是 {row[1]}"

    all_rows = conn.execute("SELECT key, value FROM memory").fetchall()
    conn.close()
    for k, v in all_rows:
        if key in k or k in key:
            return f"{k} 是 {v}"

    return f"没有找到关于'{key}'的记忆"


def semantic_search(query: str) -> str:
    """语义检索（RAG，ChromaDB）"""
    results = search_memory(query, top_k=3)
    if not results:
        return "没有找到相关的记忆"
    lines = [f"- {k}: {v}" for k, v in results]
    return "根据语义检索，找到这些相关记忆：\n" + "\n".join(lines)


def list_memory() -> str:
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("SELECT key, value FROM memory ORDER BY created_at").fetchall()
    conn.close()
    if not rows:
        return "目前还没有任何记忆"
    lines = [f"- {k}: {v}" for k, v in rows]
    return "我记得这些：\n" + "\n".join(lines)


def delete_memory(key: str) -> str:
    """删除一条记忆（SQLite + 向量库 双删）"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute("DELETE FROM memory WHERE key = ?", (key,))
    if cursor.rowcount > 0:
        conn.commit()
        conn.close()
        delete_memory_vector(key)
        return f"已忘记：{key}"

    all_rows = conn.execute("SELECT key FROM memory").fetchall()
    for (k,) in all_rows:
        if key in k or k in key:
            conn.execute("DELETE FROM memory WHERE key = ?", (k,))
            conn.commit()
            conn.close()
            delete_memory_vector(k)
            return f"已忘记：{k}"

    conn.close()
    return f"没有找到'{key}'，无需删除"