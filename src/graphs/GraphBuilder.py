from langgraph.graph import StateGraph, START, END
from src.state.state import State as Blogstate
from src.nodes.generateblog import GenerateBlog


class GraphBuilder:
    """
    A simple graph builder for LangGraph-style in-memory graphs.
    Nodes and edges can have metadata for custom behaviors.
    """
    def __init__(self,llm):
        self.graph = StateGraph(Blogstate)
        self.llm = llm
        
        
    def build_blog_graph(self):
        # Define nodes with metadata
        self.generate_blog = GenerateBlog(self.llm)
        self.graph.add_node("TitleCreation",self.generate_blog.TitleCreation)
        self.graph.add_node("ContentCreation", self.generate_blog.ContentCreation)        
       
        
        # Define edges with metadata
        self.graph.add_edge(START, "TitleCreation")
        self.graph.add_edge("TitleCreation", "ContentCreation")        
        self.graph.add_edge("ContentCreation", END)
        
        
        return self.graph

    def setup_graph_builder(self,usecase):
        if usecase=="topic":
            self.build_blog_graph()
            return self.graph.compile()
        
        else:
            raise ValueError("Unsupported use case")