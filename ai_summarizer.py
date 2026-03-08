from langchain_ollama import ChatOllama


llm = ChatOllama(
    model='llama3.2',
    temperature=0.3
    )


async def summarize_query(query:str,)