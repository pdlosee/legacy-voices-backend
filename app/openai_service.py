import openai
from app.db import get_db

def generate_questions(story_summary):
    """Generate follow-up questions based on the story summary."""
    prompt = f"""
    The user has provided the following story summary:

    "{story_summary}"

    Based on this summary, generate five insightful follow-up questions that encourage reflection and detail. The questions should help the user expand on their story meaningfully.

    Return the five questions in a numbered list.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[{"role": "system", "content": prompt}],
        max_tokens=250
    )

    return response['choices'][0]['message']['content'].split("\n")

def generate_story(story_summary, responses):
    """Generate a full narrative story using the story summary and user responses."""
    prompt = f"""
    The user provided the following story summary:
    "{story_summary}"

    They also provided the following detailed responses to five questions:
    {responses}

    Using this information, craft a compelling and emotionally engaging personal story that sounds authentic. The story should have a conversational tone, include dialogue, and reflect the user’s unique experiences.

    Return only the completed story.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[{"role": "system", "content": prompt}],
        max_tokens=2000
    )

    return response['choices'][0]['message']['content']

def get_character_profile(user_id):
    """Retrieve the user's character profile from the database"""
    db = get_db()
    result = db.execute("SELECT character_profile FROM users WHERE id = ?", (user_id,)).fetchone()
    return result["character_profile"] if result else None

def get_user_stories(user_id):
    """Retrieve all stories written by the user from the database."""
    db = get_db()
    stories = db.execute("SELECT final_story FROM stories WHERE user_id = ?", (user_id,)).fetchall()
    return [story["final_story"] for story in stories] if stories else []

def analyze_stories_for_profile_update(user_id):
    """Compare past stories with current profile to detect updates."""
    current_profile = get_character_profile(user_id)
    user_stories = get_user_stories(user_id)

    if not user_stories:
        return "No new stories detected, no updates needed."

    prompt = f"""
    Below is the user's existing character profile:
    {current_profile}

    Here are the most recent stories they have told:
    {user_stories}

    Analyze the stories and determine:
    - Are there any new recurring themes or traits that should be included?
    - Do these stories reinforce certain personality aspects that should be emphasized more?
    - Should any outdated or unnecessary aspects be removed?

    Return ONLY suggested refinements, if any. If no changes are needed, respond with: "No updates necessary."
    """

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[{"role": "system", "content": prompt}],
        max_tokens=500
    )

    return response['choices'][0]['message']['content']
