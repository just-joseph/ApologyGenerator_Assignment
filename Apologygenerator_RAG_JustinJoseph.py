import argparse
import langchain
from kendra import KendraStore
import pandas as pd

# Supported language models. Add more supported models here (e.g., Jurassic-1 Jumbo, EleutherAI Bard etc.)
supported_models = {
    "openai": langchain.llms.ChainOpenAI,
    "gpt3": langchain.llms.ChainGPT3,
    "bard": langchain.llms.ChainBARD,
    "chatgpt": langchain.llms.ChainChatGPT,
}

# Argument parsing
parser = argparse.ArgumentParser(description="Generate apology comments in response to negative feedback")
parser.add_argument("--data", type=str, required=True, help="Path to your CSV data file")
parser.add_argument("--model", type=str, choices=supported_models.keys(), default="chatgpt", help="Language model to use")
parser.add_argument("--kendra_config", type=str, help="Path to your Kendra configuration file")
args = parser.parse_args()

# Data loading 
data = pd.read_csv(args.data)
comments = data["comment"]
ratings = data["rating"]
# user_info = data["user_information"]   # commenting user_info because it is not required for now

# Model selection and instantiation
model = supported_models[args.model]()

# Kendra configuration (load from file or provide directly)
if args.kendra_config:
    with open(args.kendra_config, "r") as f:
        kendra_config = json.load(f)
else:
    # Or user-defined Kendra configuration can be modified here
    kendra_config = {
    "bucket": "your-kendra-bucket",
    "index": "your-kendra-index",
    "aws_region": "your-aws-region",
    "aws_credentials": {
        "aws_access_key_id": "your-aws-access-key-id",
        "aws_secret_access_key": "your-aws_secret-access_key",
    } }

# VectorStore connection
vector_store = KendraStore(**kendra_config)

# Vectorization using Langchain's transformers and Kendra VectorStore
def vectorize(text):
    tokens = model.tokenizer(text)
    embeddings = model.embed(tokens)
    text_vector = model.pooler(embeddings)
    vector_store.put(text, text_vector)
    return text_vector

comment_vectors = vectorize(comments)

# Function to handle a single query
def handle_query(query):
    query_vector = vectorize(query)
    similar_comments = vector_store.search(query_vector, num_results=3)

    for comment, score in similar_comments:
        if rating[comment] in [1, 2]:
            # System prompt incorporating specific comment and sentiment
            prompt = f"The user commented '{comment}' and rated it poorly. How can I apologize in a way that shows we care and are working to improve?"
            # Generate apology response using the system prompt
            apology = model(prompt)
            print(f"Comment: {comment}\nApology: {apology}")

# Handle a single query based on command-line args
while True:
    query = input("Ask a question (or 'quit' to stop): ")
    if query == "quit":
        break
    handle_query(query)




