import openai
import os

openai.api_key = os.getenv('OPENAI_API_KEY')  # Render will set this from your environment variables

def generate_questions(story_summary):
    prompt = f"""
    Please read the following story summary provided by an elderly participant.

    Story Summary: 
    {story_summary}

    Based on this story, generate 5 personalized follow-up questions. These questions should help the participant describe:
    1. Their initial feelings or motivations.
    2. The challenges they faced.
    3. Any divine or unexpected help they received.
    4. How the situation was resolved.
    5. What they learned from the experience.

    Output the questions as a JSON array.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )
    questions = response['choices'][0]['message']['content'].strip().split('\n')
    return questions

def generate_story(story_summary, responses):
    responses_text = "\n".join([f"{i+1}. {response}" for i, response in enumerate(responses)])

    prompt = f"""
    Please combine the following story summary and participant responses into a complete personal story. Use the following structure:

    1. Initial Challenge or Need
    2. Demonstration of Faith
    3. Unexpected or Divine Preparation
    4. Miraculous Resolution
    5. Lasting Impact

    Story Summary: 
    {story_summary}

    Participant Responses:
    {responses_text}

    Create a warm, personal, narrative-style story with a reflective tone. Use the participant's own voice where possible.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500
    )
    return response['choices'][0]['message']['content'].strip()