from flask import Blueprint, request, jsonify
from db import get_db
from app.openai_service import analyze_stories_for_profile_update

bp = Blueprint('routes', __name__)

@bp.route('/update-character-profile', methods=['POST'])
def update_character_profile():
    """User-triggered character profile refinement based on new stories."""
    data = request.json
    user_id = data.get("user_id")

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    suggested_update = analyze_stories_for_profile_update(user_id)

    if "No updates necessary" in suggested_update:
        return jsonify({"message": "No new stories detected, no updates needed."})

    return jsonify({"message": "Suggested profile update available.", "profile_update": suggested_update})

@bp.route('/accept-profile-update', methods=['POST'])
def accept_profile_update():
    """User-approved character profile update."""
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
