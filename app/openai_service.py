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
        5. Lasting Impact
        
        Story Summary: 
        {story_summary}
        
        Please generate exactly 5 questions that help deepen the user's reflection and faith-based insights. 
        """

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a thoughtful, faith-centered interviewer guiding life stories."},
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
        Transform the following story summary and participant responses into a **detailed, immersive, and engaging LDS faith-centered narrative** of at least **1500-2000 words**.

        Follow this structure:
        1. **An Initial Challenge or Need** - Describe the hardship or need that set the stage for this experience.
        2. **A Demonstration of Faith** - Show how the storyteller exercised faith, trust, or obedience in God.
        3. **Unexpected or Divine Preparation** - Reveal any prior events or experiences that, in hindsight, prepared them for this moment.
        4. **A Miraculous Resolution** - Describe how the situation was resolved, highlighting any divine intervention or spiritual insight.
        5. **A Lasting Impact** - Conclude with how this experience strengthened their faith and shaped their understanding of God’s role in their life.

        Please **write in an engaging, personal, and emotionally resonant style**, capturing the storyteller's authentic voice.
        Expand historical and cultural details to **enrich the setting and context**.
        Include **natural-sounding dialogue** where appropriate to enhance realism.

        Story Summary: 
        {story_summary}
        
        Participant Responses:
        {responses_text}
        
        Please generate a warm, reflective, engaging personal story that emphasizes faith and divine presence in life’s moments.
        """

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a faith-centered storyteller transforming life experiences into compelling narratives."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=4000
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        logging.error(f"Error generating story: {e}", exc_info=True)
        return "We're sorry — we encountered an error while creating your story. Please contact the project team for assistance."
