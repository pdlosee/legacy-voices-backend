from flask import Blueprint, request, jsonify
from app.openai_service import generate_questions, generate_story

bp = Blueprint('routes', __name__)

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

    final_story = generate_story(story_summary, responses)
    return jsonify({'finalStory': final_story})