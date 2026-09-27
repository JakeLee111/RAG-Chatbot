from dotenv import load_dotenv 
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv() # load GOOGLE_API_KEY in .env file
print("\nWhat would you like to learn?\n") 
question = input("\nYou: ")
prompt = f"""Question: {question}
Act as a friendly university tutor and reply base on fact and reiable sources.
Explain in step by step structure when applicable.
Keep answer simple and short. Avoid jargons and be casual.

Example:
Question: AI chatbot
Answer: 
An **AI chatbot** is a software application designed to simulate human conversation through text or voice. 

Here is how they work, based on established computer science literature (such as Russell & Norvig’s *Artificial Intelligence: A Modern Approach*):

1. **Natural Language Processing (NLP):** This is the branch of AI that helps the chatbot understand, interpret, and manipulate human language.
2. **Machine Learning (ML):** Modern chatbots use **Large Language Models (LLMs)**. They are trained on massive datasets of human text.
3. **Pattern Recognition:** Instead of "thinking" like a human, the chatbot uses advanced statistics to predict the most logical next word in a sentence based on your prompt.

**In short:** An AI chatbot does not understand the world; it is a highly sophisticated calculator for language.

"""
model = ChatGoogleGenerativeAI(
    model = "gemini-3.5-flash",
    temperature = 0
)

response = model.invoke(prompt)
print(response.text)



