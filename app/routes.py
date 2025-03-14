from flask import Blueprint, request, jsonify
from flask_cors import CORS
from app.openai_service import generate_questions, generate_story, revise_story

bp = Blueprint('routes', __name__)
CORS(bp)

@bp.route('/generate-questions', methods=['POST'])
def generate_questions_endpoint():
    data = request.json
    story_summary = data.get('storySummary', '')
    if not story_summary:
        return jsonify({'error': 'Story summary is required'}), 400

    questions = generate_questions(story_summary)
    return jsonify({'questions': questions})

@bp.route('/generate-story', methods=['POST'])
def generate_story_endpoint():
    data = request.json
    story_summary = data.get('storySummary', '')
    responses = data.get('responses', [])

    if not story_summary or len(responses) != 5:
        return jsonify({'error': 'Story summary and exactly 5 responses required'}), 400

    try:
        final_story = generate_story(story_summary, responses)
        return jsonify({'finalStory': final_story})
    except Exception as e:
        return jsonify({'error': f'Error generating story: {str(e)}'}), 500

@bp.route('/revise-story', methods=['POST'])
def revise_story_endpoint():
    data = request.json
    original_story = data.get('story', '')
    dialogue = data.get('dialogue', '5')  # Default to neutral if missing
    history = data.get('history', '5')
    humor = data.get('humor', '5')
    length = data.get('length', '5')
    moral = data.get('moral', '5')
    custom_note = data.get('customNote', '')

    if not original_story:
        return jsonify({'error': 'Original story is required'}), 400

    try:
        revised_story = revise_story(original_story, dialogue, history, humor, length, moral, custom_note)
        return jsonify({'revisedStory': revised_story})
    except Exception as e:
        return jsonify({'error': f'Error revising story: {str(e)}'}), 500

