import json
import os # 파이썬을 이용해서 시스템 내부에 접근이 가능하다 

task_file = 'tasks.json'

def load_task():
    if os.path.exists('tasks.json'):#파일이 있는경우
        with open(task_file, 'r', encoding='utf-8') as file: #file => open(task_file, 'r', encoding='utf-8') as file
            return json.load(file) #json.load()
    return []
        
def save_task(tasks): #add_task를 통해 전달받은 해야할 일을 파일에 저장하는 기능
    with open(task_file, 'w', encoding='utf-8') as file: #file => open(TASK_FILE, 'w', encoding='utf-8')
        json.dump(tasks, file, indent=4, ensure_ascii=False)

def add_task(task_name): #할 일 추가 함수
    tasks = load_task() # 파일이 있다면 가져와
    task = {'name':task_name, "completed":False} #파이썬 공부하기에 대한 데이터가 들어갔어
    tasks.append(task)
    save_task(tasks)

def view_task():  # 할 일 목록보기   
    tasks = load_task() 
    if not tasks:  
        print("할 일이 없습니다.")
    else:
        for idx, task in enumerate(tasks, start=1):
            status = "완료" if task["completed"] else "미완료"
            print(f"{idx}. {task['task']} [{status}]")

def complete_task(task_number): # 할 일 완료
    tasks = load_task()  
    if 0 < task_number <= len(tasks): #
        tasks[task_number - 1]["completed"] = True 
        #tasks[0] ["completed"] > {name :파이썬 공부하기 , completed : False} completed에 True집어넣음
        save_task(tasks)
        print(f"할 일 : '{tasks[task_number - 1]['task']}'이(가) 완료되었습니다.") 
    else: #3번 입력한 경우 잘못된 입력입니다. 출력
        print("잘못된 번호입니다.")

def delete_task(task_number):#할 일 삭제
    tasks = load_task()
    if 1 <= task_number <= len(tasks):
        delete_tsk = tasks.pop(task_number-1)
        save_task(tasks)
        print (f'할 일 : {delete_tsk['name']} 이(가) 삭제되었습니다.')
    else:
        print('유효하지 않은 작업 번호입니다. 다시 확인해주세요.')

def show_menu(): #메뉴를 보여주는 함수
    print("작업 관리 애플리케이션")
    print("1. 할 일 추가")
    print("2. 할 일 목록보기")
    print("3. 할 일 완료")
    print("4. 할 일 삭제")
    print("5. 종료")

def main():
    while True:
        show_menu()
        choice = input("원하는 작업을 선택해주세요 (1~5): ") # 1
        if choice == '1':
            task_name = input("추가할 작업을 입력해주세요") # 파이썬 공부하기
            add_task(task_name)

        elif choice == '2':
            view_task()

        elif choice == '3':
            task_number = int(input("완료를 원하는 작업의 번호를 입력해주세요"))
            complete_task(task_number)
        elif choice == '4':
            task_number = int(input("삭제를 원하는 작업의 번호를 입력해주세요"))
            delete_task(task_number)
        elif choice == '5':
            print("시스템을 종료합니다.")
            break
        else:
            print("잘못 입력하셨습니다. 1번부터 5번까지의 기능 중 하나를 선택해주세요")

main()