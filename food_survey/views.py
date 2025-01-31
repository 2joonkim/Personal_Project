# food_survey/views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import UserResponse
import json
import openai
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main_page(request):
    # 세션 초기화
    if not request.session.session_key:
        request.session.create()
    return render(request, 'main.html')


def question1(request):
    return render(request, 'question1.html')


@csrf_exempt
def save_question1(request):
    if request.method == 'POST':
        try:
            people_count = request.POST.get('answer')
            session_id = request.session.session_key

            # 기존 응답이 있으면 업데이트, 없으면 새로 생성
            response, created = UserResponse.objects.get_or_create(
                session_id=session_id,
                defaults={'people_count': people_count}
            )

            if not created:
                response.people_count = people_count
                response.save()

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def question2(request):
    return render(request, 'question2.html')


@csrf_exempt
def save_question2(request):
    if request.method == 'POST':
        try:
            hunger_level = request.POST.get('answer')
            session_id = request.session.session_key

            response = UserResponse.objects.get(session_id=session_id)
            response.hunger_level = hunger_level
            response.save()

            return JsonResponse({'status': 'success'})
        except UserResponse.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'No previous response found'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def question3(request):
    return render(request, 'question3.html')


@csrf_exempt
def save_question3(request):
    if request.method == 'POST':
        try:
            food_type = request.POST.get('answer')
            session_id = request.session.session_key

            response = UserResponse.objects.get(session_id=session_id)
            response.food_type = food_type
            response.save()

            return JsonResponse({'status': 'success'})
        except UserResponse.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'No previous response found'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def question4(request):
    return render(request, 'question4.html')


@csrf_exempt
def save_question4(request):
    print("=== save_question4 called ===")
    if request.method == 'POST':
        try:
            if not request.session.session_key:
                request.session.create()
            session_id = request.session.session_key
            print(f"Session ID: {session_id}")

            data = json.loads(request.body)
            print(f"Received data: {data}")

            try:
                # 기존 응답 찾기
                response = UserResponse.objects.get(session_id=session_id)
            except UserResponse.DoesNotExist:
                # 없으면 새로 생성
                response = UserResponse(session_id=session_id)

            # 데이터 저장
            if data.get('noPreference', False):
                response.no_preference = True
                # 기본값 설정
                response.spicy_level = 3
                response.oil_level = 3
                response.texture_level = 3
                response.taste_level = 3
                if not response.food_type:  # food_type이 없는 경우
                    response.food_type = '노상관'
                if not response.people_count:  # people_count가 없는 경우
                    response.people_count = '노상관'
                if not response.hunger_level:  # hunger_level이 없는 경우
                    response.hunger_level = '노상관'
            else:
                response.no_preference = False
                response.spicy_level = int(data.get('spicy', 3))
                response.oil_level = int(data.get('oil', 3))
                response.texture_level = int(data.get('texture', 3))
                response.taste_level = int(data.get('taste', 3))

            response.save()
            print("Successfully saved response")
            return JsonResponse({'status': 'success'})
        except Exception as e:
            print(f"Error in save_question4: {str(e)}")
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def result_page(request):
    print("=== result_page called ===")
    if not request.session.session_key:
        print("No session key, redirecting to main")
        return redirect('main')

    session_id = request.session.session_key
    print(f"Session ID: {session_id}")

    try:
        user_response = UserResponse.objects.get(session_id=session_id)

        # AI 추천 시스템 사용
        recommended_food = get_ai_food_recommendation(user_response)

        # 점수에 따른 메시지 로직
        score = recommended_food.get('score', 50)

        # 메시지 로직 변경
        if score >= 75:
            message = "오늘 날 잡았네요?"
        elif score >= 50:
            message = "역시 한국인은 밥심이죠"
        elif score >= 25:
            message = "어제 뭘 많이 먹었나요?!"
        else:
            message = "오늘은 소식하시려구요~?"

        context = {
            'food_name': recommended_food['food_name'],
            'score': score,
            'message': message,
            'description': recommended_food.get('description', ''),
            'reason': recommended_food.get('reason', ''),
            'cuisine_type': recommended_food.get('cuisine_type', '')
        }
        return render(request, 'result.html', context)

    except UserResponse.DoesNotExist:
        print("UserResponse not found")
        return redirect('question1')
    except Exception as e:
        print(f"Error in result_page: {str(e)}")
        return redirect('main')


def get_ai_food_recommendation(user_response):
    """
    OpenAI API를 활용한 AI 기반 음식 추천 함수
    """
    try:
        # OpenAI 클라이언트 초기화
        client = openai.OpenAI(
            api_key=os.getenv('OPENAI_API_KEY')
        )

        # 사용자 정보를 JSON 형식으로 변환
        user_info = {
            "people_count": str(user_response.people_count),
            "hunger_level": str(user_response.hunger_level),
            "food_type": str(user_response.food_type),
            "no_preference": user_response.no_preference,
            "spicy_level": user_response.spicy_level,
            "oil_level": user_response.oil_level,
            "texture_level": user_response.texture_level,
            "taste_level": user_response.taste_level
        }

        # AI에게 전달할 프롬프트 구성
        prompt = f"""
        다음 사용자 선호도 정보를 바탕으로 최적의 음식을 추천해줘:

        {json.dumps(user_info, ensure_ascii=False, indent=2)}

        다음 형식으로 정확히 JSON 응답해줘:
        {{
            "food_name": "추천 음식 이름",
            "description": "음식에 대한 간단한 설명",
            "reason": "이 음식을 추천하는 이유",
            "score": 0-100 사이의 정수 점수,
            "cuisine_type": "한식/중식/일식/양식 중 해당하는 분류"
        }}
        """

        # OpenAI API 호출 (최신 버전)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "당신은 음식 추천 전문 AI 어시스턴트입니다. 사용자의 선호도를 정확히 분석하고 최적의 음식을 추천해야 합니다."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300
        )

        # 응답 파싱 (최신 버전에서 응답 추출 방식 변경)
        recommendation = json.loads(response.choices[0].message.content)

        # 로깅
        logger.info(f"AI 음식 추천 결과: {recommendation}")

        return recommendation

    except Exception as e:
        # 오류 처리
        logger.error(f"AI 추천 중 오류 발생: {str(e)}")
        return {
            "food_name": "오늘의 특선",
            "description": "AI 추천 시스템에 오류가 발생했습니다.",
            "reason": "시스템 오류로 인한 기본 추천",
            "score": 50,
            "cuisine_type": "기타"
        }

