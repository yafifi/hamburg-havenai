from src.api.gemini_client import call_gemini

def analyze_context(context):
    prompt = f"""
    You are an AI logistics analyst.

    Analyze the following input:
    {context}

    Provide structured insights.

    Weather:
    {context['weather']}

    Ships:
    {context['ships']}

    Return:
    - Delay risks
    - Explanation
    - Ranking
    """

    return call_gemini(prompt)