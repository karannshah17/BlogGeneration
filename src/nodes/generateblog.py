from src.llms.llm import GroqLLM
from src.state.state import State  
from langchain_core.messages import HumanMessage, SystemMessage
from src.state.state import Blog  

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

    def Translation(self, state: State):
        """
        Translates the blog content to the specified language{{language}} using the LLM model.
        :param blogstate: State dict containing blog content and target language  {{language}}.
        """
        translation_prompt = """Translate the following blog content to {user_language}:\n\n{blog_content}. 
        The translation should be accurate and maintain the original meaning.Adapt cultural references appropriately.
        Return ONLY a JSON object in this exact format:
            {{
             "title": "<translated title>",
             "content": "<translated content>"
            }} Do not include any extra text, explanations, markdown, or tags."""

        blog_content = state['blog']['content']
        user_language = state['language']

        messages=[HumanMessage(content=translation_prompt.format(user_language=user_language, blog_content=blog_content))]
        translated_content = self.llm.with_structured_output(Blog).invoke(messages)
        return {"blog":{"title":translated_content.title,"content":translated_content.content}}
        


    def route(self, state: State):
       return {"language": state['language']}

    def route_decision(self, state: State):
        if state['language'] == "German":
            return "German"
        elif state['language'] == "French":
            return "French"
        else:
            return "German"
