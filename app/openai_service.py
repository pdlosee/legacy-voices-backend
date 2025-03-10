import os
import logging
from openai import OpenAI

# Set up logging for Render (optional but useful)
logging.basicConfig(level=logging.INFO)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def generate_questions(story_summary):
    try:
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

        Output only the 5 questions, each on a new line.
        """

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )

        content = response.choices[0].message.content.strip()
        questions = [q.strip() for q in content.split('\n') if q.strip()]

        if len(questions) != 5:
            raise ValueError(f"Expected 5 questions, got {len(questions)} - Response content: {content}")

        return questions

    except Exception as e:
        logging.error(f"Error generating questions from OpenAI: {e}", exc_info=True)
        return [
            "We encountered an error creating your personalized questions. Please try again later.",
            "If the problem persists, contact the project team for assistance.",
            "This may be due to a temporary system issue.",
            "Thank you for your patience.",
            "We look forward to hearing your story!"
        ]

def generate_story(story_summary, responses):
    try:
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

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        logging.error(f"Error generating story from OpenAI: {e}", exc_info=True)
        return "We're sorry — we encountered an error while creating your story. Please contact the project team for assistance."
