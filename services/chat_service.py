from typing import Any, Dict, List

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_openai import ChatOpenAI

from app.core import prompts
from app.core.config import settings

DEFAULT_MODEL = "gpt-4o-mini"

class ChatService:
    def __init__(self):
        self.llm = ChatOpenAI(model=DEFAULT_MODEL, temperature=0.7, api_key=settings.OPENAI_API_KEY)

    async def get_response(
        self,
        message: str,
        chat_history: List[Dict[str, str]] | None = None,
        context: Dict[str, Any] | None = None,
    ) -> str:
        messages = [SystemMessage(content=prompts.CHAT_SYSTEM_PROMPT)]
        
        if context:
            context_str = "\n".join(f"{k}: {v}" for k, v in context.items())
            messages.append(SystemMessage(content=f"Context:\n{context_str}"))
        
        if chat_history:
            for msg in chat_history:
                role = msg.get("role", "user")
                content = msg.get("content", "")
                if role == "user":
                    messages.append(HumanMessage(content=content))
                elif role == "assistant":
                    messages.append(AIMessage(content=content))
        
        # Add current message
        messages.append(HumanMessage(content=message))
        
        response = await self.llm.ainvoke(messages)
        return response.content

chat_service = ChatService()
