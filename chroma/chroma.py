import chromadb
from chromadb.api.types import Documents, Embeddings
from chromadb.api.models.Collection import Collection
from typing import Tuple, List

# CHROMA_PERSISTENT_PATH = "D:\SMU_Classes\Jan 2024 Term Latest\AI Planning\Grp Project\LLM-CSP-Solver\chroma\data"
CHROMA_PERSISTENT_PATH = "chroma\data"


def create_chroma_collection(documents: List[str], name: str) -> Collection:
    """
    Create chroma collection if not exists

    Parameters:
    -----------
    documents: Documents that needs to be added to collection
    name: Name of the collection

    Returns:
    -----------
    ChromaDB collection client
    """
    print("Working on creating collection ", name)
    chroma_client = chromadb.PersistentClient(path=CHROMA_PERSISTENT_PATH)
    db = chroma_client.create_collection(name=name)
    for i, row in enumerate(documents):

        db.add(documents=row, ids=str(i))
    return db


def get_relevant_doc(db: Collection, error: str, top_k: int = 10):
    """
    Get relevant Questions and Answers

    Parameters:
    -----------
    db: Chroma collection client
    error: Error given by the executor agent
    top_k: No of relavant documents that needs to be returned by chroma

    Returns:
    -----------
    List of relevant documents
    """
    results = db.query(query_texts=[error], n_results=top_k)
    docs = ""
    for doc in results["documents"]:
        for d in doc:
            docs = docs + "\n" + d

    return docs


def get_chroma_collection(name: str) -> Collection:
    """
    Get chroma collection client

    Parameters:
    -----------
    name: Name of the collection

    Returns:
    -----------
    ChromaDB collection client
    """
    chroma_client = chromadb.PersistentClient(path=CHROMA_PERSISTENT_PATH)
    try:
        db = chroma_client.get_collection(name)
    except:
        # print("Chroma collection not found")
        raise Exception("Chroma collection not found")
        # db = create_chroma_collection(data, name)
    return db


if __name__ == "__main__":
    ## Creating Library documentation lookup
    file_name = "chroma\data\documentation.txt"
    with open(file_name, encoding="utf8", mode="r") as f:
        data = f.read()  # .strip()
    chunks = data.split("---------")
    print("All chunks ", len(chunks))
    collection_name = "docplex_documentation"
    db = create_chroma_collection(chunks, collection_name)
    db = get_chroma_collection(collection_name)
    # question = "AttributeError: 'CpoModel' object has no attribute 'all_different'"
    question = "AttributeError: 'CpoModel' object has no attribute 'all_distinct'\n"
    results = get_relevant_doc(db, question, 3)
    print(results)
    ## Creating planning_agent example collection
    file_name = "chroma\data\planning_agent_examples.txt"
    with open(file_name, encoding="utf8", mode="r") as f:
        data = f.read()  # .strip()
    chunks = data.split("---------")
    print("All chunks ", len(chunks))
    collection_name = "planning_agent_examples"
    db = create_chroma_collection(chunks, collection_name)
    db = get_chroma_collection(collection_name)
    question = "Scheduling problem example"
    results = get_relevant_doc(db, question, 3)
    print(results)
    ## Creating planning_agent example collection
    file_name = "chroma\data\coding_agent_examples.txt"
    with open(file_name, encoding="utf8", mode="r") as f:
        data = f.read()  # .strip()
    chunks = data.split("---------")
    print("All chunks ", len(chunks))
    # print(chunks[:3])
    collection_name = "coding_agent_examples"
    db = create_chroma_collection(chunks, collection_name)
    db = get_chroma_collection(collection_name)
    question = "Scheduling problem example"
    results = get_relevant_doc(db, question, 3)
    print(results)
