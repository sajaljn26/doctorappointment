# main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import logging
from langchain_core.messages import HumanMessage

# Import tools directly from toolkit.toolkits
from toolkit.toolkits import (
    check_availability_by_doctor,
    check_availability_by_specialization,
    set_appointment,
    cancel_appointment,
    reschedule_appointment
)

app = FastAPI()

# Define data models
class Message(BaseModel):
    role: str
    content: str

class UserQuery(BaseModel):
    id_number: int
    messages: List[Message]

@app.post("/execute")
async def execute_agent(user_input: UserQuery):
    try:
        # Avoid circular imports
        from agent import DoctorAppointmentAgent

        agent = DoctorAppointmentAgent()
        app_graph = agent.workflow()

        # Extract messages
        messages = [
            HumanMessage(content=msg.content)
            for msg in user_input.messages
            if msg.role == "user"
        ]

        # Create state for workflow
        initial_state = {
            "messages": messages,
            "id_number": user_input.id_number,
            "next": "",
            "query": messages[0].content if messages else "",
            "current_reasoning": ""
        }

        print("🚀 Invoking workflow with state:", initial_state)

        result = app_graph.invoke(initial_state)

        print("✅ Agent returned:", result)

        # Extract assistant messages from result
        assistant_messages = [
            {"role": "assistant", "content": msg.content}
            for msg in result.get("messages", [])
            if hasattr(msg, 'content') and isinstance(msg.content, str)
        ]

        return {
            "id_number": user_input.id_number,
            "messages": assistant_messages,
            "status": "success"
        }

    except Exception as e:
        print("🔥 ERROR OCCURRED:", str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def health_check():
    return {"status": "running"}
