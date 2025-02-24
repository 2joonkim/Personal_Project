from flask import Blueprint, jsonify, request
from app.models import Answer, User, Choices
from config import db

# Blueprint 생성
answers_bp = Blueprint("submit", __name__, url_prefix="/submit")

@answers_bp.route("/", methods=["POST"])
def submit_answers():
    data = request.get_json()

    # # 데이터 유효성 검사
    # if not data:
    #     return jsonify({"error": "No data provided"}), 400

    try:
        for entry in data:
            user_id = entry.get("userId")
            choice_id = entry.get("choiceId")

            # if not user_id or not choice_id:
            #     return jsonify({"error": "userId and choiceId are required"}), 400

            # # 유효한 user_id와 choice_id 확인
            # user = User.query.get(user_id)
            # choice = Choices.query.get(choice_id)

            # if not user:
            #     return jsonify({"error": f"User with ID {user_id} does not exist"}), 400
            # if not choice:
            #     return jsonify({"error": f"Choice with ID {choice_id} does not exist"}), 400

            # Answer 모델에 데이터 저장
            new_answer = Answer(user_id=user_id, choice_id=choice_id)
            db.session.add(new_answer)

        db.session.commit()  # 모든 답변을 데이터베이스에 커밋

        # 성공 메시지 반환
        return jsonify({"message": f"User: {user_id}'s answers Success Create"}), 201

    except Exception as e:
        db.session.rollback()  # 예외 발생 시 롤백
        return jsonify({"error": str(e)}), 500  # 예외 처리