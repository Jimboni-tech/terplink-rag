import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
import pandas as pd

chroma_client = chromadb.PersistentClient(path='../data/chroma-data')
df = pd.read_csv("../data/org-data-cleaned.csv")
df = df.dropna(subset=['Information', 'Name', 'URL'])
df = df[df['Information'].str.strip() != ""]
embedding = SentenceTransformerEmbeddingFunction(model_name = "all-MiniLM-L6-v2")
org_collection = chroma_client.get_or_create_collection(
    name="student_org_collection", embedding_function=embedding
)
ids = []
docs = []
metadata=[]
batch_size = 100
for i in range(0, len(df), batch_size):
    batch = df.iloc[i:i+batch_size]
    org_collection.add(
        ids=[str(idx) for idx in batch.index],
        documents=batch['Information'].tolist(),
        metadatas=[
            {"Name": row['Name'], "Time": row['Time'], "URL": row['URL']}
            for _, row in batch.iterrows()
        ]
    )


org_collection.add(
    ids=ids,
    documents=docs,
    metadatas=metadata
)
