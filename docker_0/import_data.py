import pandas as pd
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http import models as rest

# Load the CSV file
file_path = "data.csv"
df = pd.read_csv(file_path)

# Extract all column names from the CSV file
selected_columns = df.columns.tolist()

print(selected_columns)

# Combine header and values into a single text string for each row
def combine_headers_with_values(row, columns):
    combined_text = " , ".join([f"{col}: {row[col]}" for col in columns])
    return combined_text

df['source'] = df.apply(lambda row: combine_headers_with_values(row, selected_columns), axis=1)

# Load the model
model_name = "nomic-ai/nomic-embed-text-v1.5"
model = SentenceTransformer(model_name, trust_remote_code=True)

# Function to generate embeddings
def get_embedding(text):
    try:
        embedding = model.encode(text)
        return embedding.tolist()  # Convert embedding to list
    except Exception as e:
        print(f"Error in getting embedding: {e}")
        return None

# Apply the embedding function to the concatenated text
df['content_vector'] = df['source'].apply(get_embedding)

# Initialize Qdrant client
client = QdrantClient(host='127.0.0.1', port=6333)


# Let's assume you want to delete a collection known as "default"
collection_name = "default"

existing_collections = client.get_collections().collections


# Delete the default collection if it exists
try:
    client.delete_collection(collection_name=collection_name)
    print(f"Deleted collection '{collection_name}'.")
except Exception as e:
    print(f"An error occurred while deleting the collection: {e}")

vector_size = 768  # Assuming the model outputs 768-dimensional vectors

# Check if the collection exists, if not, create it
if not client.collection_exists(collection_name):
    client.create_collection(
        collection_name=collection_name,
        vectors_config=rest.VectorParams(
            distance=rest.Distance.COSINE,
            size=vector_size,
        )
    )
    print(f"Collection '{collection_name}' created.")
else:
    print(f"Collection '{collection_name}' already exists.")

# Upsert the vectors into the collection
for idx, row in df.iterrows():
    embedding = row['content_vector']

    if embedding is not None:
        point = rest.PointStruct(
            id=idx,
            vector=embedding,  # Use the "default" vector name
            payload=row.to_dict(),
        )

        # Upsert to Qdrant
        client.upsert(
            collection_name=collection_name,
            points=[point]
        )

print("Embedding and upsert completed.")
