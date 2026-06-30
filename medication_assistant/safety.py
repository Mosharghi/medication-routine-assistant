UNSAFE_KEYWORDS = [
    "double my dose",
    "halve my dose",
    "increase my dose",
    "decrease my dose",
    "stop taking",
    "quit this medicine",
    "start this medicine",
    "what should I take",
    "is this interaction safe",
    "is it safe with",
    "overdose",
    "poisoning",
]

def is_medical_advice_request(user_text: str) -> bool:
    """
    Very simple check for medication-advice questions.
    This is not perfect, but it helps you demonstrate safety in the capstone.
    """
    if not user_text:
        return False
    text = user_text.lower()
    return any(keyword in text for keyword in UNSAFE_KEYWORDS)


SAFETY_REFUSAL_MESSAGE = (
    "I can help you track medications and routines, but I cannot provide medical "
    "advice, change doses, or check if medicines are safe together. "
    "Please talk to a doctor, pharmacist, nurse, or emergency service for that."
)
