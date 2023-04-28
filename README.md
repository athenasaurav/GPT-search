# GPT-search

Install the following in a new virtual env

```
flask
langchain
openai
unstructured[local-inference]
tiktoken
faiss-gpu (or cpu based on your server)
```

Export your API Key on your instance
```
export OPENAI_API_KEY=your_api_key
```
RUN the app from root folder 
```
python app.py
```
*To Run this program using Docker, Run the following steps (make sure Dcoker is installed)

To install Docker
