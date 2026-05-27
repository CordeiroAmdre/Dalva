from langchain_core.prompts import ChatPromptTemplate

dalva_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are the Dalva assistant. Answer briefly and clearly.",
        ),
        ("human", "{message}"),
    ]
)
