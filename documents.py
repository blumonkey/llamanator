from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from transformers import LlamaTokenizerFast
import os
from common import hash_id
from ui import show_spinner
from logger import logging

"""
Methods that work with documents or document vectors
"""


def load_textfile(fname):
    tokenizer = LlamaTokenizerFast.from_pretrained("oobabooga/llama-tokenizer")
    tokenizer.add_eos_token = True

    splitter = RecursiveCharacterTextSplitter.from_huggingface_tokenizer(
        tokenizer=tokenizer, chunk_size=380
    )
    loader = TextLoader(fname)
    return loader.load_and_split(splitter)


def ingest_docs(db, docs):
    """Ingest a Document list into the vector db.
    The id is a hash of the Document, since it must be unique.
    This means it's impossible to replace a document with this hashing scheme.

    TODO: Check that this is WAI
    """
    ids = (hash_id(str(d)) for d in docs)
    docs_map = dict(zip(ids, docs))
    uids = docs_map.keys()
    existing_ids = set(db.index_to_docstore_id.values())
    new_ids = list(set(uids).difference(existing_ids))
    new_docs = [docs_map[i] for i in new_ids]
    with show_spinner(
        f"Adding {len(new_ids)} new documents, ignoring {len(uids) - len(new_ids)} duplicates."
    ) as c:
        if len(new_ids):
            db.add_documents(new_docs, ids=new_ids)
            logging.info(f"Saving vector store to {db.path}/.")
            return db.save_local(db.path)


def format_docs(docs):
    """Format a list of langchain Document objects for passing to the chat agent"""
    return f"{os.linesep}".join(
        [
            f"{d.metadata.get('source', '')}{os.linesep}{d.metadata.get('time', '---')}{os.linesep}{d.page_content}"
            for d in docs
        ]
    )
