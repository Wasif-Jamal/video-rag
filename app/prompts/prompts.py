class RAGPromptManager:

    def get_chat_prompt(
        self,
        question: str,
        context: str,
        history: str,
    ):

        return f"""
    You are a helpful AI assistant for answering
    questions about videos.

    Use ONLY:
    1. Conversation history
    2. Retrieved context

    If the answer is not present,
    say:
    "I do not know."

    Conversation History:
    {history}

    Retrieved Context:
    {context}

    Current Question:
    {question}

    Answer:
    """ 

prompt_manager = (
    RAGPromptManager()
)