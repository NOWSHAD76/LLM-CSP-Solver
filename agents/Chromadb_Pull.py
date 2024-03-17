def chromadb_pull(query: str, api_key = "") -> str:
    """
    Pulls the latest version of the ChromaDB database from the server.
    """
    ### Importing the Database into the LLM
    import csv

    with open('Planning_Agent_Vector.csv') as file:
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

    # openai_ef = embedding_functions.OpenAIEmbeddingFunction(api_key = api_key, model_name="text-embedding-ada-002")

    # Memory only instance
    chroma_client = chromadb.Client()

    # sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-mpnet-base-v2")

    collections = chroma_client.get_or_create_collection('CPO_Collection')

    # Add all entries to the vector database.
    collections.add(documents=documents, metadatas=metadata, ids=ids)#, embedding_function=sentence_transformer_ef)

    results = collections.query(
                            query_texts=query, 
                            n_results=1,
                            include=['documents', 'distances', 'metadatas'])

    #print(results['documents'])
    # get result with lowest distance

    closest_neighbour = results['documents'][0][0]
    return closest_neighbour

