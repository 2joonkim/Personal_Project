from flask_smorest import Blueprint
from app import db
from app.models import User, AgeStatus, GenderStatus
from flask import request, jsonify

users_bp = Blueprint('users', __name__, url_prefix='/signup')

@users_bp.route('', methods=['POST'])
def signup():
    try:
        data = request.get_json()

        # 필수 입력 값 검증
        name = data.get('name')
        age = data.get('age')
        gender = data.get('gender')
        email = data.get('email')

        if not all([name, age, gender, email]):
            return jsonify({'error': '모든 필드를 입력해주세요. (name, age, gender, email)'}), 400

        # Enum 값 검증
        try:
            age_status = AgeStatus(age)
            gender_status = GenderStatus(gender)
        except ValueError:
            return jsonify({'error': '유효하지 않은 age 또는 gender 값입니다.'}), 400

        # 중복 이메일 검증
        if User.query.filter_by(email=email).first():
            return jsonify({'error': '이미 존재하는 이메일입니다.'}), 400

        # 유저 생성
        new_user = User(
            name=name,
            age=age_status,
            gender=gender_status,
            email=email
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            'message': '회원가입이 완료되었습니다.',
            'user_id': new_user.id
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'서버 오류가 발생했습니다: {str(e)}'}), 500