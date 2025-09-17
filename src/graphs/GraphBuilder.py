from langgraph.graph import StateGraph, START, END
from src.state.state import State as Blogstate
from src.nodes.generateblog import GenerateBlog
from src.llms.llm import GroqLLM

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
    
    def build_language_graph(self):
        # Define nodes with metadata
        self.generate_blog = GenerateBlog(self.llm)
        self.graph.add_node("TitleCreation",self.generate_blog.TitleCreation)
        self.graph.add_node("ContentCreation", self.generate_blog.ContentCreation)   
        self.graph.add_node("GermanTranslation", lambda state: self.generate_blog.Translation({**state, "user_language": "German"}))  
        self.graph.add_node("FrenchTransation", lambda state: self.generate_blog.Translation({**state, "user_language": "French"}))       
        self.graph.add_node("Route", self.generate_blog.route)     
        
        # Define edges with metadata
        self.graph.add_edge(START, "TitleCreation")
        self.graph.add_edge("TitleCreation", "ContentCreation") 
        self.graph.add_edge("ContentCreation", "Route")    
        self.graph.add_conditional_edges("Route", self.generate_blog.route_decision, {
            "German": "GermanTranslation",
            "French": "FrenchTransation"
        })

        self.graph.add_edge("GermanTranslation", END)
        self.graph.add_edge("FrenchTransation", END)
        
        return self.graph
    
    

    def setup_graph_builder(self,usecase):
        if usecase=="topic":
            self.build_blog_graph()
            return self.graph.compile()
        elif usecase=="language":
            self.build_language_graph()
            return self.graph.compile()
        
        else:
            raise ValueError("Unsupported use case")
        

llm=GroqLLM().getllm()
graph=GraphBuilder(llm).build_blog_graph().compile()