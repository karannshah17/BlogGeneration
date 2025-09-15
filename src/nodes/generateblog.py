from src.llms.llm import GroqLLM
from src.state.state import State  

class GenerateBlog:
    def __init__(self, llm):
        self.llm = llm

    def TitleCreation(self, state: State):
        """
        Generates a blog title using the LLM model.
        :param blogstate: State dict containing topic and language.
        :return: Generated title as a string.
        """
        prompt = f"Generate a blog title about '{state['topic']}'.The title should be creative and engaging and seo optimized. and there should be only one title"
        response = self.llm.invoke([{"role": "user", "content": prompt}])
        return {"blog":{"title":response.content}}
    
    def ContentCreation(self, state: State):
        """
        Generates a blog detailed content using the LLM model.
        :param blogstate: State dict containing topic .
        :return: Generated detailed  content as a string.
        """
        prompt = f"Generate a detailed blog content  about '{state['topic']}'.The content  should be at least 2000 characters and should provide indepth insights about the given topic."
        response = self.llm.invoke([{"role": "user", "content": prompt}])
        
        return {"blog":{"title":state['blog']['title'],"content":response.content}}
