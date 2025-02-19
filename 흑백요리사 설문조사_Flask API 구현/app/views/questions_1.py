from flask import Blueprint, jsonify, request
from app.models import Question, Image
from config import db
from collections import OrderedDict

questions_1_bp = Blueprint("questions", __name__, url_prefix="/questions")

# 질문 개수 확인
@questions_1_bp.route("/count", methods=["GET"])
def get_question_count():
    total_questions = Question.query.count()  # 총 질문 개수 계산
    return jsonify({"total": total_questions}), 200