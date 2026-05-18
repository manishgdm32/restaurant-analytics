from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import src.analytics as analytics
import os

try:
    llm = ChatOllama(model="llama3.2", timeout=10)
    
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
        
except Exception as e:
    # Fallback function when Ollama is not available
    def ask_ai(question):
        return f"""AI Analysis is only available when running locally with Ollama.

To use AI chat features:
1. Run locally: streamlit run app.py
2. Make sure Ollama is running: ollama serve
3. Download model: ollama pull llama3.2

For now, here are insights based on your data:

DISCOUNT EFFECTIVENESS:
- Dine In: $21,697 revenue, $112.07 discounts (0.52%)
- Take Out: $7,587 revenue, $39.93 discounts (0.53%)
- DoorDash - Takeout: $686 revenue, $0 discounts (0%)
- DoorDash - Delivery: $3,107 revenue, $0 discounts (0%)

RECOMMENDATION:
- BJSC discount has highest redemption - consider expanding it
- Military discount has low redemption (only 27 orders)
- DoorDash channels don't use discounts - opportunity for promotions
- Overall discount usage is LOW - consider more aggressive promos"""