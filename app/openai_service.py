import os
import logging
from openai import OpenAI

logging.basicConfig(level=logging.INFO)

client = OpenAI()

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
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )

        content = response.choices[0].message.content.strip()

        # Basic safety processing to split into 5 questions.
        questions = content.split('\n')
        questions = [q.strip() for q in questions if q.strip()]

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
