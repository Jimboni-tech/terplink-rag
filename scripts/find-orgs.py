import chromadb
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

client = chromadb.PersistentClient(path='../data/chroma-data')
org_collection = client.get_collection(name="student_org_collection")


def get_relevant_orgs(input: str, top_k: int = 5):
    orgs = org_collection.query(
        query_texts=[input],
        n_results=top_k,
        include=['metadatas']
    )
    results = []
    for meta in orgs['metadatas'][0]:
        results.append({
            "Name": meta['Name'],
            "Time": meta.get('Time', ''),
            "URL": meta['URL']
        })
    return results


if __name__ == '__main__':
    user_question = input()
    orgs = get_relevant_orgs(user_question, top_k=5)
    context = "\n".join(
        f"Name: {org['Name']}\nTime: {org['Time']}\nURL: {org['URL']}\n"
        for org in orgs
    )
    template = """Question: {question}
    Context: {context}
    Answer: Here are the student orgs that would best fit you"""

    prompt = ChatPromptTemplate.from_template(template)

    model = OllamaLLM(model="llama3.1")

    chain = prompt | model

    response = chain.invoke({"question": user_question, "context": context})
    print(context)
    print(response)
