class RAGPromptManager:

    def get_chat_prompt(
        self,
        question: str,
        context: str,
    ) -> str:

        return f"""
You are a helpful AI assistant for answering
questions about video content.

Use ONLY the provided context to answer.

If the answer is not present in the context,
say you do not know.

Keep the answer concise and factual.

Question:
{question}

Context:
{context}

Answer:
"""


prompt_manager = (
    RAGPromptManager()
)