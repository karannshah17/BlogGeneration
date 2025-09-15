from llm import LLM

if __name__ == "__main__":
    llm_instance = LLM()
    groq_model = llm_instance.getllm()
    if groq_model:
        print("LLM initialized successfully!")
    else:
        print("LLM initialization failed.")