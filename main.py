import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# --- Router & API Configuration ---
# 1. Set environment variables for LangChain
# LangChain uses the OpenAI wrapper, so we use OpenAI-style environment variables.
os.environ["OPENAI_API_KEY"] = "sk-UiS6REFMozZPFdCC7E1x6w-example"  # virtual key for Router authentication
os.environ["OPENAI_API_BASE"] = "http://localhost:4000"

# --- Build LangChain ---

# 2. Initialize the model (connects to Router)
# The router will automatically route the request, ignoring the model name here.
llm = ChatOpenAI(
    model="vertex_ai/gemini-2.5-flash-lite",  # Model name is just a placeholder for the Router
    temperature=0.7,
    # You may explicitly provide Base URL and Key if you prefer:
    # openai_api_base=LITELLM_ROUTER_URL,
    # openai_api_key="sk-lite-llm-key"
)

# 3. Create a Prompt Template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an intelligent and creative AI assistant. Reply in Vietnamese."),
    ("user", "{topic}")
])

# 4. Build the LCEL (LangChain Expression Language) Chain
chain = prompt | llm | StrOutputParser()

# --- Run the Chain and use routing features ---

print("-" * 50)

# Request 1:
topic_1 = "Explain briefly how LiteLLM helps manage multiple API Keys."
response_1 = chain.invoke({"topic": topic_1})
print(f"Request 1 (Router uses Model A):\n{response_1}\n")

# Request 2:
# The router may use Model B based on the 'simple-shuffle' strategy
topic_2 = "Differentiate Load Balancing and Fallbacks in the context of an AI Router."
response_2 = chain.invoke({"topic": topic_2})
print(f"Request 2 (Router uses Model B):\n{response_2}")