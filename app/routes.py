from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from app.openai_service import generate_questions

bp = Blueprint('routes', __name__)

@bp.route('/generate-questions', methods=['POST', 'OPTIONS'])
@cross_origin()
def generate_questions_endpoint():
    if request.method == 'OPTIONS':
        return jsonify({"message": "Preflight request allowed"}), 200  # ✅ Handles CORS Preflight Request
    
    data = request.json
    story_summary = data.get('storySummary', '')

    if not story_summary:
        return jsonify({'error': 'Story summary is required'}), 400

    questions = generate_questions(story_summary)
    return jsonify({'questions': questions})



# ✅ Generate Story from User Responses
@bp.route('/generate-story', methods=['OPTIONS', 'POST'])
@cross_origin()
def generate_story_endpoint():
    if request.method == 'OPTIONS':
        return jsonify({"message": "Preflight request allowed"}), 200

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


# ✅ Update Character Profile Based on User Stories
@bp.route('/update-character-profile', methods=['OPTIONS', 'POST'])
@cross_origin()
def update_character_profile():
    if request.method == 'OPTIONS':
        return jsonify({"message": "Preflight request allowed"}), 200

    data = request.json
    user_id = data.get("user_id")

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    suggested_update = analyze_stories_for_profile_update(user_id)

    if "No updates necessary" in suggested_update:
        return jsonify({"message": "No new stories detected, no updates needed."})

    return jsonify({"message": "Suggested profile update available.", "profile_update": suggested_update})


# ✅ Accept and Save Updated Character Profile
@bp.route('/accept-profile-update', methods=['OPTIONS', 'POST'])
@cross_origin()
def accept_profile_update():
    if request.method == 'OPTIONS':
        return jsonify({"message": "Preflight request allowed"}), 200

    data = request.json
    user_id = data.get("user_id")
    new_profile = data.get("new_profile")

    if not user_id or not new_profile:
        return jsonify({"error": "User ID and profile update are required"}), 400

    db = get_db()
    db.execute(
        "UPDATE users SET character_profile = ? WHERE id = ?",
        (new_profile, user_id)
    )
    db.commit()

    return jsonify({"message": "Character profile updated successfully"})
