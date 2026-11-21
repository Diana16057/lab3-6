# main.py
import random

import mansion  # импортируем сам модуль — флаги будем читать через точку
from mansion import (
    add_clue, count_clues, describe, visit_room,
    get_long_clues, format_clues,
    show_help, try_move, look_room, take_item, use_item,
    get_ending,
    clues
)

# --- КОНФИГУРАЦИЯ: перевод русских команд и комнат в английские ключи ---
COMMAND_MAP = {
    "иди": "go",
    "осмотри": "look",
    "возьми": "take",
    "используй": "use",
    "улики": "clues",
    "инвентарь": "inventory",
    "помощь": "help",
    "выход": "exit"
}

ROOM_MAP = {
    "холл": "hall",
    "библиотека": "library",
    "кабинет": "study",
    "спальня": "bedroom",
    "подвал": "basement",
    "чердак": "attic",
    "выход": "exit"
}

# Русские названия комнат для вывода игроку
ROOM_NAMES_RU = {
    "hall": "холл",
    "library": "библиотека",
    "study": "кабинет",
    "bedroom": "спальня",
    "basement": "подвал",
    "attic": "чердак",
    "exit": "входная дверь"
}

# --- НАЧАЛО ИГРЫ ---
current_room = "hall"

print("Квест-детектив: Таинственный особняк")
print("Цель: соберите улики, найдите ключ и откройте выход.")
print("Команды: иди [комната], осмотри, возьми [предмет], используй [предмет], улики, инвентарь, помощь, выход")
print(describe(current_room))

while True:
    try:
        command_input = input("> ").strip().lower()
    except EOFError:
        break

    if not command_input:
        continue

    parts = command_input.split()
    raw_command = parts[0] if len(parts) > 0 else ""
    raw_arg = parts[1] if len(parts) > 1 else ""

    command = COMMAND_MAP.get(raw_command, raw_command)
    target_room = None

    if command == "go":
        target_room = ROOM_MAP.get(raw_arg, raw_arg)

    # --- СЛУЧАЙНЫЕ СОБЫТИЯ ---
    if command not in ["clues", "inventory", "help"]:
        if random.random() < 0.3:
            event = random.choice([
                "Скрипнула половица где-то вдалеке.",
                "Хлопнула дверь на втором этаже.",
                "В темноте мелькнула тень.",
                "Тишину нарушает тихий шёпот."
            ])
            print(event)

    # --- ОБРАБОТКА КОМАНД ---

    if command == "help":
        show_help()

    elif command == "go":
        if not target_room:
            print("Используйте: иди [название комнаты]. Например: иди библиотека")
            continue

        new_room, message = try_move(current_room, target_room, ROOM_NAMES_RU)
        if new_room is not None:
            current_room = new_room
            print(message)
            visit_room(current_room)
        else:
            print(message)

    elif command == "look":
        look_room(current_room)

    elif command == "take":
        item = raw_arg
        if not item:
            print("Используйте: возьми [предмет]. Например: возьми ключ")
            continue
        take_item(current_room, item)

    elif command == "use":
        item = raw_arg
        if not item:
            print("Используйте: используй [предмет]")
            continue
        use_item(item)

    elif command == "clues":
        print(f"Собрано улик: {count_clues(clues)}")
        long_clues = get_long_clues(clues)
        if long_clues:
            print("Длинные улики:")
            for c in long_clues:
                print(f"  {c}")
        else:
            print("Длинных улик пока нет.")
        print("Полный список улик:")
        for formatted in format_clues(clues):
            print(f"  {formatted}")

    elif command == "inventory":
        inv = []
        if mansion.has_key:
            inv.append("ключ")
        if mansion.lantern_taken:
            inv.append("фонарь")
        if mansion.letter_taken:
            inv.append("письмо")
        if mansion.map_taken:
            inv.append("карта")

        if inv:
            print("В инвентаре: " + ", ".join(inv))
        else:
            print("Инвентарь пуст.")

    elif command == "exit":
        if current_room != "exit":
            print("Сначала дойдите до входной двери (команда: иди выход).")
        elif not mansion.has_key:
            print("Дверь заперта. Нужен ключ!")
        else:
            print(get_ending(count_clues(clues)))
            break

    else:
        print("Неизвестная команда. Введите 'помощь' для справки.")







