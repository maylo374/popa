import PySimpleGUI as sg
import random
import json
import os
from datetime import datetime

# Предопределённые задачи с категориями
TASKS = {
    "Учёба": ["Прочитать статью по Python", "Решить 5 задач по математике", "Выучить 20 новых слов"],
    "Спорт": ["Сделать зарядку", "Пробежать 3 км", "Позаниматься йогой 30 минут"],
    "Работа": ["Написать отчёт", "Провести встречу с командой", "Проверить почту"],
    "Творчество": ["Нарисовать скетч", "Написать рассказ", "Сыграть на гитаре"]
}

# Загрузка истории из JSON
def load_history():
    if os.path.exists("task_history.json"):
        with open("task_history.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# Сохранение истории в JSON
def save_history(history):
    with open("task_history.json", "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=4)

# Генерация случайной задачи
def generate_task(category=None):
    if category and category in TASKS:
        tasks_list = TASKS[category]
    else:
        # Объединяем все задачи, если категория не выбрана
        tasks_list = [task for tasks in TASKS.values() for task in tasks]
    return random.choice(tasks_list), category or "Все"

# Создание интерфейса
def create_layout():
    layout = [
        [sg.Text("Random Task Generator", font=("Arial", 16))],
        [sg.Button("Сгенерировать задачу", key="-GENERATE-")],
        [sg.Combo(["Все", "Учёба", "Спорт", "Работа", "Творчество"], default_value="Все", key="-CATEGORY-", enable_events=True)],
        [sg.Text("Сгенерированная задача:", font=("Arial", 12))],
        [sg.Text("", size=(50, 2), key="-TASK-", font=("Arial", 12), relief="sunken")],
        [sg.Text("История задач:", font=("Arial", 12))],
        [sg.Listbox([], size=(60, 10), key="-HISTORY-")],
        [sg.Button("Очистить историю", key="-CLEAR-")]
    ]
    return layout

# Основной цикл приложения
def main():
    history = load_history()
    window = sg.Window("Random Task Generator", create_layout())

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == "-GENERATE-":
            category = values["-CATEGORY-"]
            task, task_category = generate_task(None if category == "Все" else category)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            history_entry = f"[{timestamp}] {task_category}: {task}"
            history.append(history_entry)
            window["-TASK-"].update(task)
            window["-HISTORY-"].update(history)
            save_history(history)
        elif event == "-CLEAR-":
            history.clear()
            window["-HISTORY-"].update(history)
            save_history(history)

    window.close()

if __name__ == "__main__":
    main()
