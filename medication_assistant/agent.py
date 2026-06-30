from google.adk.agents import LlmAgent
from medication_assistant.prompts import SYSTEM_PROMPT
from medication_assistant.tools import (
    add_medication,
    get_today_schedule,
    get_today_status,
    log_dose,
    get_adherence_summary,
)

root_agent = LlmAgent(
    name="medication_routine_assistant",
    model="gemini-2.5-flash",
    description="Helps users track medications, schedules, and adherence.",
    instruction=SYSTEM_PROMPT,
    tools=[
        add_medication,
        get_today_schedule,
        get_today_status,
        log_dose,
        get_adherence_summary,
    ],
)