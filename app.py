import uvicorn
from fastapi import FastAPI, Request
from src.graphs.GraphBuilder import GraphBuilder
from src.llms.llm import GroqLLM


import os
from dotenv import load_dotenv  
load_dotenv()  # Load environment variables from .env file


app = FastAPI()
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

@app.post("/generate_blog")
async def generate_blog(request: Request):
    """
    Run the blog workflow (Title -> Content -> Summary, etc.)
    """
    data=await request.json()
    print(data)
    ##topic = data.get("topic", "")
    initial_state = {
        "blog": {"title": None, "content": None},
        "topic": data.get("topic", "")
       
    }
    llm= GroqLLM()
    llm=llm.getllm()
    graph_builder = GraphBuilder(llm)
    graph=graph_builder.setup_graph_builder(usecase="topic" )
    result =graph.invoke(initial_state)
    return result["blog"]

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)