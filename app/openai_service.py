import os
import logging
from openai import OpenAI

# Set up logging for debugging
logging.basicConfig(level=logging.INFO)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def generate_questions(story_summary):
    try:
        prompt = f"""
        You are an LDS biographical interviewer helping users tell their life stories through faith-centered reflection. 
        Read the following story summary and generate 5 follow-up questions following this structure:

        1. Initial Challenge or Need
        2. Demonstration of Faith
        3. Unexpected or Divine Preparation
        4. Miraculous Resolution
        5. A Lasting Impact

        Story Summary:
        {story_summary}

        Please generate exactly 5 questions that help deepen the user's reflection and faith-based insights.
        """

        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a thoughtful, faith-centered interviewer guiding life stories."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=750
        )

        content = response.choices[0].message.content.strip()
        questions = [q.strip() for q in content.split('\n') if q.strip()]

        if len(questions) != 5:
            raise ValueError(f"Expected 5 questions, got {len(questions)} - Response content: {content}")

        return questions

    except Exception as e:
        logging.error(f"Error generating questions: {e}", exc_info=True)
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
        You are a skilled LDS storyteller dedicated to preserving personal history with authenticity and emotional depth.
        Transform the following story summary and participant responses into a **deeply personal, immersive, and engaging LDS faith-centered narrative** in the **first-person perspective**.

        ### Story Structure:
        1. **An Initial Challenge or Need** - Establish the setting, emotions, and obstacles.
        2. **A Demonstration of Faith** - Show how faith, trust, or obedience played a role.
        3. **Unexpected or Divine Preparation** - Reveal any prior experiences that prepared the person for this moment.
        4. **A Miraculous Resolution** - Describe the outcome, highlighting divine intervention.
        5. **A Lasting Impact** - Conclude with how the experience shaped faith and perspective.

        **Story Summary:**
        {story_summary}

        **Participant Responses:**
        {responses_text}

        Please generate a warm, reflective, and engaging personal story that captures **the subtle yet profound ways faith operates in everyday life**.
        """

        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a faith-centered storyteller transforming life experiences into compelling first-person narratives."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=4096
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        logging.error(f"Error generating story: {e}", exc_info=True)
        return "We're sorry — we encountered an error while creating your story. Please contact the project team for assistance."

def revise_story(original_story, dialogue, history, humor, length, moral, custom_note):
    try:
        revision_prompt = f"""
        Revise the following LDS-themed personal story based on the user’s requested changes.

        - Adjust the **amount of natural conversation** (0-10 scale): {dialogue}/10.
        - Adjust **historical & cultural details** (0-10 scale): {history}/10.
        - Adjust **humor** (0-10 scale): {humor}/10.
        - Adjust **story length** (0-10 scale): {length}/10.
        - Adjust **moral lesson emphasis** (0-10 scale): {moral}/10.

        Additional user notes: {custom_note}

        **Revise the story accordingly while maintaining narrative coherence and emotional depth.**

        Original Story:
        {original_story}
        """

        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are an expert storyteller and editor, refining personal narratives."},
                {"role": "user", "content": revision_prompt}
            ],
            max_tokens=4096
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        logging.error(f"Error revising story: {e}", exc_info=True)
        return "We're sorry — an error occurred while revising your story."
