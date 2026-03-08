from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="llama3.2",
    temperature=0.3
)

def summarize_query(query: str, results: dict):

    documents = results.get("documents", [])

    if documents:
        documents = documents[0]

    context = "\n\n".join(documents)

    prompt = f"""
You are an assistant answering questions using the provided document excerpts.

Use the information in the references to answer the query.
If the references partially contain the answer, infer the answer carefully.
Do not invent facts outside the references.

Query:
{query}

References:
{context}

Answer clearly and concisely.
"""

    response = llm.invoke(prompt)

    return response.content