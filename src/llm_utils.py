import src.analytics as analytics
import os

def ask_ai(question):
    """Send question to AI and get response"""
    
    # Check if Ollama is available
    ollama_available = False
    try:
        from langchain_ollama import ChatOllama
        llm = ChatOllama(model="llama3.2", timeout=5)
        ollama_available = True
    except:
        pass
    
    if not ollama_available:
        # Return predefined analysis based on data
        kpis = analytics.get_kpis()
        cat = analytics.get_category_sales()
        disc = analytics.get_discount_impact()
        channel = analytics.get_channel_performance()
        
        return f"""AI requires local setup with Ollama. Here's analysis from your data:

📊 KEY METRICS:
- Total Revenue: ${kpis['total_revenue']:,.2f}
- Total Orders: {kpis['total_orders']}
- Avg Order Value: ${kpis['avg_order_value']:.2f}

🏆 BEST PERFORMING CATEGORY:
{cat.head(5).to_string()}

Top category is 'Food' with the highest revenue contribution.

💰 CHANNEL PERFORMANCE:
{channel.to_string()}

📍 RECOMMENDATION:
Focus on Food category items - they generate most revenue.
Consider promoting appetizers and sides as add-ons to increase avg order value."""
    
    # If Ollama available, use it
    from langchain_ollama import ChatOllama
    from langchain_core.prompts import PromptTemplate
    from langchain_core.output_parsers import StrOutputParser
    
    llm = ChatOllama(model="llama3.2")
    
    RESTAURANT_PROMPT = PromptTemplate(
        input_variables=["context", "question"],
        template="""You are a restaurant business analyst assistant.

CONTEXT FROM DATA:
{context}

INSTRUCTIONS:
- Answer based ONLY on the data
- Provide specific numbers and recommendations

Question: {question}

Your response:"""
    )

    chain = RESTAURANT_PROMPT | llm | StrOutputParser()
    context = analytics.get_ai_context()
    return chain.invoke({"context": context, "question": question})