import os
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.docstore.in_memory import InMemoryDocstore
from config import get_config

config = get_config()
emodel = config["storage"]["embedding"]
storage_path = config["storage"]["path"]

embedding = HuggingFaceEmbeddings(
    model_name=emodel, model_kwargs={"device": "cpu"}
)

"""
Handles the knowledge store 
"""


def faiss(db_path):
    from faiss import IndexFlatL2

    db = (
        FAISS.load_local(db_path, embedding)
        if os.path.isdir(db_path)
        else FAISS(
            embedding_function=embedding,
            index=IndexFlatL2(
                len(embedding.embed_query("get the embedding dimension"))
            ),
            docstore=InMemoryDocstore({}),
            index_to_docstore_id={},
        )
    )
    db.path = db_path
    db.kind = "faiss"
    return db


knowledge_store = faiss(os.path.join(storage_path, "knowledge.faiss"))
