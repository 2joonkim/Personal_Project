from flask import Blueprint, jsonify, request
from app.models import Image, ImageStatus
from config import db

# Blueprint 생성
images_bp = Blueprint("image", __name__, url_prefix="/image")

# 메인 이미지 조회
@images_bp.route("/main", methods=["GET"])
def get_main_image():
    main_image = Image.query.filter_by(type="main").first()
    if not main_image:
        return jsonify({"error": "메인 이미지를 찾을 수 없습니다."}), 404

    # URL만 포함한 데이터 반환
    return jsonify({"image": main_image.url}), 200

# 이미지 업로드
@images_bp.route("/", methods=["POST"])
def upload_image():
    try:
        data = request.get_json()
        url = data.get("url")
        type = data.get("type")

        if not url or not type:
            return jsonify({"error": "필수 데이터가 부족합니다."}), 400

        # Enum 검증
        try:
            type_enum = ImageStatus(type)
        except ValueError:
            return jsonify({"error": f"유효하지 않은 이미지 타입: {type}"}), 400

        new_image = Image(url=url, type=type_enum)
        db.session.add(new_image)
        db.session.commit()

        return jsonify(new_image.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"서버 오류가 발생했습니다: {str(e)}"}), 500
    
@images_bp.route("/main", methods=["DELETE"])
def delete_main_image():
    try:
        main_image = Image.query.filter_by(type="main").first()
        if not main_image:
            return jsonify({"error": "메인 이미지를 찾을 수 없습니다."}), 404

        db.session.delete(main_image)
        db.session.commit()

        return jsonify({"message": "메인 이미지가 삭제되었습니다."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"서버 오류가 발생했습니다: {str(e)}"}), 500