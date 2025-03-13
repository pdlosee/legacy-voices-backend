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
        You are a skilled LDS storyteller dedicated to preserving personal history with authenticity and emotional depth.
        
        Transform the following story summary and participant responses into a **deeply personal, immersive, and engaging LDS faith-centered narrative** in the **first-person perspective**. Ensure the final story is **at least 1500-2000 words** and feels like a **real, lived memory**, not a formal retelling.
        
        Follow this natural storytelling structure:
        1. **An Initial Challenge or Need** - Establish the setting, capturing the emotions, fears, or uncertainties the storyteller faced.
        2. **A Demonstration of Faith** - Show how the storyteller exercised faith, trust, or obedience in God, using **realistic dialogue and internal reflections**.
        3. **Unexpected or Divine Preparation** - Reveal any prior events, teachings, or experiences that, in hindsight, prepared them for this moment.
        4. **A Miraculous Resolution** - Describe how the situation was resolved, highlighting **small but powerful moments of divine intervention or realization**.
        5. **A Lasting Impact** - Conclude with how this experience strengthened their faith, changed their perspective, or influenced future decisions.
        
        **Key Requirements:**
        - **Write in a natural, conversational, and emotionally resonant style.**
        - **Ensure the storyteller's voice feels authentic**—as if they are telling the story themselves.
        - **Expand historical and cultural details** where appropriate to enrich the setting and context.
        - **Avoid summarizing lessons explicitly**—let them emerge naturally through actions and realizations.
        - **Use natural conversation dialogue between the characters in the story.** to enhance immersion and authenticity.
        - **A minimum of 35% of the story words will reflect conversation between story characters.** to add credability.
        - **Add a humor tone where appropriate in the story** to enhance reader engagement
        - **Story length goal is a minimum of 2000 words** expand with historical detail if story content is minimal
        
        Story Summary: 
        {story_summary}
        
        Participant Responses:
        {responses_text}
        
        Please generate a warm, reflective, and engaging personal story that captures **the subtle yet profound ways faith operates in everyday life**.
        """

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
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
