from flask import Blueprint, jsonify, request
from app.models import Choices, Question
from config import db

# Blueprint 생성
choices_bp = Blueprint("choice", __name__, url_prefix="/choice")

# 선택지 목록 조회
@choices_bp.route("/<int:question_id>", methods=["GET"])
def get_choices_by_question(question_id):
    # 특정 질문에 대한 선택지 가져오기
    choices = Choices.query.filter_by(question_id=question_id).all()
    if not choices:
        return jsonify({"error": "해당 질문에 대한 선택지가 없습니다."}), 404

    return jsonify({
        "choices": [
            {
                "id": choice.id,
                "content": choice.content,
                "is_active": choice.is_active
            } for choice in choices
        ]
    }), 200

# 선택지 생성
@choices_bp.route("/", methods=["POST"])
def create_choice():
    data = request.get_json()

    question_id = data.get("question_id")
    content = data.get("content")
    is_active = data.get("is_active", True)

    # 필수 데이터 확인
    if not question_id or not content:
        return jsonify({"error": "question_id와 content는 필수입니다."}), 400

    # 질문 확인
    question = Question.query.get(question_id)
    if not question:
        return jsonify({"error": "유효하지 않은 question_id입니다."}), 400

    # 선택지 생성
    new_choice = Choices(
        question_id=question_id,
        content=content,
        is_active=is_active
    )
    db.session.add(new_choice)
    db.session.commit()

    return jsonify({"message": "선택지가 성공적으로 생성되었습니다.", "choice": new_choice.to_dict()}), 201

# 선택지 삭제
@choices_bp.route("/<int:choice_id>", methods=["DELETE"])
def delete_choice(choice_id):
    choice = Choices.query.get(choice_id)
    if not choice:
        return jsonify({"error": "유효하지 않은 choice_id입니다."}), 404

    db.session.delete(choice)
    db.session.commit()

    return jsonify({"message": f"선택지 ID {choice_id}가 성공적으로 삭제되었습니다."}), 200