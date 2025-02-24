from flask import Blueprint, jsonify
from config import db

connect_bp = Blueprint("connect", __name__)

@connect_bp.route('/')
def index():
    """
    API 연결 상태 확인
    """
    return jsonify({"message": "Success Connect"}), 200