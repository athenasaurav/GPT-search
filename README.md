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
## To Run this program using Docker, Run the following steps (make sure Dcoker is installed)

To install Docker
```
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```
Now we have Docker installed, we are ready to build and depoy the app.

Build Docker APP:
```
docker build -t my_app .  #Replace my_app with any app name you want
```

Now to deploy the app on <ip>:<port>, use the following command:
```
docker run -p 5010:5010 my_app  # Make sure to replace the name of the app to your name choosen earlier. Remember i have choosen 5010 (make sure you have this open)
```

To keep running in background run the following command
```
docker run -d -p 5010:5010 -e my_app # Make sure to replace the name of the app to your name choosen earlier. Remember i have choosen 5010 (make sure you have this open)
```

