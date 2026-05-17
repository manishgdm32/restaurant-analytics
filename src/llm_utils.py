from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import src.analytics as analytics

llm = ChatOllama(model="llama3.2")

RESTAURANT_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template="""You are a restaurant business analyst assistant. You have detailed sales data from an Indian restaurant (Lota) for April 2026.

CONTEXT FROM DATA:
{context}

INSTRUCTIONS:
- Answer based ONLY on the data provided
- Provide specific numbers and percentages
- Give actionable business recommendations
- Keep responses concise but informative
- If you don't have enough data to answer, say so

Question: {question}

Your response:"""
)

chain = RESTAURANT_PROMPT | llm | StrOutputParser()

def ask_ai(question):
    """Send question to AI and get response"""
    context = analytics.get_ai_context()
    response = chain.invoke({"context": context, "question": question})
    return response