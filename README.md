# ApologyGenerator_Assignment
To run this code, use:
python apology_generator.py --data your_data.csv --model chatgpt


This Python code aims to generate apology responses for negative feedback within a user interaction setting. Here's a breakdown of its key components and functionalities:

1. Model Options and Configuration:
It offers various language models through the supported_models dictionary, allowing you to choose from options like OpenAI, GPT-3, BARD, ChatGPT, and potentially adding more supported models.
It provides command-line arguments (--data, --model, --kendra_config) to specify the data file, preferred model, and Kendra configuration path for flexibility.

2. Data Loading and Preprocessing:
The code loads your tabular data (comment, rating, user_information) from a CSV file using pandas.
It extracts comments, ratings, and user information for further processing.

3. Kendra VectorStore Connection:
It utilizes the KendraStore class from the kendra library to connect to your Kendra VectorStore instance.
The Kendra configuration can be loaded either from a file or provided directly within the code.

4. Vectorization:
It employs the chosen language model's tokenizer and embedding features to convert comments into numerical vectors.
These vectors capture the semantic meaning of the comments and enable similarity search in Kendra VectorStore.

5. Query Handling and Response Generation:
The code defines a handle_query function that takes a user query as input.
It converts the query into a vector and searches for similar comments in Kendra VectorStore.
For comments with negative ratings (1 or 2), it creates a system prompt incorporating the specific comment and sentiment.
This prompt serves as a guide for the language model to generate an apology response that acknowledges the issue and expresses care/improvement efforts.
The generated apology response is then displayed alongside the original comment.

6. User Interaction (Interactive mode):
User interaction loop allows users to input questions and receive apologies based on similar comments.

8. Running the Code:
The above provided command demonstrates how to run the script, specifying the data file and model choice.
Adjust the command or arguments based on your specific setup and Kendra configuration.

Overall, this code presents a versatile and comprehensive RAG solution for generating apologies in response to negative feedback, leveraging text vectorization, semantic search, and language model-powered response generation.
