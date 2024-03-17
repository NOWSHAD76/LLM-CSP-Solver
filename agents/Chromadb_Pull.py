def chromadb_pull(query: str, api_key = "") -> str:
    """
    Pulls the latest version of the ChromaDB database from the server.
    """
    ### Importing the Database into the LLM
    import csv
    from dotenv import load_dotenv

    load_dotenv()

    with open('agents\Planning_Agent_Vector.csv') as file:
        lines = csv.reader(file)
        # Store Questions and Answers Prompt here.
        documents = []
        # Store ProblemID here
        metadata=[]
        # Unique ID for each question
        ids = []
        id = 1

        # loop tru each line in the csv file
        for i, line in enumerate(lines):
            if i == 0:
                continue
            # Store the problem ID
            metadata.append({"item_id": line[0]})
            # Store the question
            documents.append(line[1])
            # Store the unique ID
            ids.append(str(id))
            id += 1
        pass
    
    import chromadb
    from chromadb.utils import embedding_functions

    #openai_ef = embedding_functions.OpenAIEmbeddingFunction(api_key = api_key,model_name="text-embedding-ada-002")

    # Memory only instance
    chroma_client = chromadb.Client()

    #sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-mpnet-base-v2")

    collections = chroma_client.get_or_create_collection('CPO_Collection')

    # Add all entries to the vector database.
    collections.add(documents=documents, metadatas=metadata, ids=ids)

    results = collections.query(
                            query_texts=query, 
                            n_results=3,
                            include=['documents', 'distances', 'metadatas'])

    #print(results['documents'])
    # get result with lowest distance

    closest_neighbour = results['distances'][0]
    return closest_neighbour

prompt ="""
Problem Statement: An airline operates flights requiring the following crew: Flight 1 needs 2 pilots and 3 cabin crew members. Flight 2 needs 2 pilots and 4 cabin crew members. There are 3 pilots (P1, P2, P3) and 5 cabin crew members (C1, C2, C3, C4, C5) available. Each crew member can only work on one flight. Assign crew members to flights to meet requirements.

Constraints:

Each flight has specific pilot and cabin crew requirements.
Each crew member can only be assigned to one flight.
       """

get_nein = (chromadb_pull(prompt))
for i in get_nein:
    print("Drawing from ChromaDB...")
    print(i)
    print("\n")