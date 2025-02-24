from flask import Blueprint, jsonify, request
from app.models import Question, Image
from config import db
from collections import OrderedDict

# Blueprint 생성
questions_bp = Blueprint("question", __name__, url_prefix="/question")

# 질문 목록 조회
@questions_bp.route("/get", methods=["GET"])
def get_questions():
    questions = Question.query.all()

    # 질문 데이터를 이미지 URL과 함께 반환
    result = []
    for q in questions:
        image = Image.query.get(q.image_id)  # 이미지 ID를 사용하여 이미지 조회
        question_data = {
            "id": q.id,
            "title": q.title,
            "image": {"url": image.url} if image else None,  # 이미지가 존재하면 URL 포함
        }
        result.append(question_data)

    return jsonify(result), 200

# 질문 생성
@questions_bp.route("/", methods=["POST"])
def create_question():
    data = request.get_json()
    title = data.get("title")
    image_id = data.get("image_id")
    sqe = data.get("sqe", 0)

    if not title or not image_id:
        return jsonify({"error": "필수 데이터가 부족합니다."}), 400

    # 이미지 확인
    image = Image.query.get(image_id)
    if not image:
        return jsonify({"error": "유효하지 않은 이미지 ID입니다."}), 400

    new_question = Question(title=title, image_id=image_id, sqe=sqe)
    db.session.add(new_question)
    db.session.commit()

    return jsonify(new_question.to_dict()), 201

# 특정 질문 조회
@questions_bp.route("/<int:question_id>", methods=["GET"])
def get_question_by_id(question_id):
    # 질문 데이터 조회
    question = Question.query.get(question_id)
    if not question:
        return jsonify({"error": "질문을 찾을 수 없습니다."}), 404

    # 이미지 데이터 조회
    image = Image.query.get(question.image_id)

    # 질문 데이터 생성 (순서 강제)
    question_data = OrderedDict()
    question_data["id"] = question.id
    question_data["title"] = question.title
    question_data["image"] = {"url": image.url} if image else None

    # 응답 데이터 반환
    return jsonify({"question": question_data}), 200