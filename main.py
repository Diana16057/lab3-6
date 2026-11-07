# main.py
# Точка входа. Полностью русский интерфейс.

from mansion import (
    add_clue, count_clues, describe, visit_room,
    get_long_clues, format_clues, clues, visited_rooms
)

# --- КОНФИГУРАЦИЯ: перевод русских команд и комнат в английские ключи ---
ROOM_MAP = {
    "холл": "hall",
    "библиотека": "library",
    "кабинет": "study",
    "спальня": "bedroom",
    "подвал": "basement",
    "чердак": "attic",
    "выход": "exit"
}

COMMAND_MAP = {
    "иди": "go",
    "осмотри": "look",
    "возьми": "take",
    "используй": "use",
    "улики": "clues",
    "инвентарь": "inventory",
    "помощь": "help",
    "выход": "exit"  # Эта команда завершает игру, а не комнату
}

# Состояние игрока
current_room = "hall"
has_key = False
lantern_taken = False
letter_taken = False
map_taken = False
turn_counter = 0

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

    # --- ЛОГИКА ПЕРЕВОДА ВВОДА ---
    command = COMMAND_MAP.get(raw_command, raw_command)

    target_room = None
    if command == "go":
        target_room = ROOM_MAP.get(raw_arg, raw_arg)

    # Случайные события
    if command not in ["clues", "inventory", "help"]:
        turn_counter += 1
        if turn_counter % 3 == 0:
            event_rand = turn_counter % 4
            events = [
                "Скрипнула половица где-то вдалеке.",
                "Хлопнула дверь на втором этаже.",
                "В темноте мелькнула тень.",
                "Тишину нарушает тихий шёпот."
            ]
            print(events[event_rand])

    # --- ОБРАБОТКА КОМАНД ---

    if command == "help":
        print("Доступные команды:")
        print("  иди [холл, библиотека, кабинет, спальня, подвал, чердак, выход]")
        print("  осмотри — изучить комнату")
        print("  возьми [предмет] — подобрать вещь")
        print("  используй [предмет] — применить вещь")
        print("  улики — показать статистику и список")
        print("  инвентарь — показать вещи у вас")
        print("  выход — завершить игру (если у двери и есть ключ)")

    elif command == "go":
        if not target_room:
            print("Используйте: иди [название комнаты]. Например: иди библиотека")
            continue

        if target_room not in ROOM_MAP.values():
            print("Такой комнаты не существует. Доступные комнаты: холл, библиотека, кабинет, спальня, подвал, чердак, выход.")
            continue

        # Логика перемещения
        if current_room == "hall":
            if target_room in ["library", "study", "bedroom", "basement", "attic", "exit"]:
                current_room = target_room
                room_name_ru = next(k for k, v in ROOM_MAP.items() if v == current_room)
                print(f"Вы прошли в {room_name_ru}.")
                visit_room(current_room)
            else:
                print("Из холла можно пойти только в: библиотека, кабинет, спальня, подвал, чердак, выход.")
        else:
            if target_room == "hall":
                current_room = "hall"
                print("Вы вернулись в холл.")
                visit_room(current_room)
            else:
                print("Отсюда можно вернуться только в холл (команда: иди холл).")

    elif command == "look":
        print(describe(current_room))
        room_name_ru = next(k for k, v in ROOM_MAP.items() if v == current_room)

        if current_room == "library" and "В библиотеке найдена перчатка с монограммой" not in clues:
            add_clue(clues, "В библиотеке найдена перчатка с монограммой.")
            print("Вы заметили деталь: перчатка с монограммой!")
        elif current_room == "basement" and "В подвале на стене выцарапаны странные символы" not in clues:
            add_clue(clues, "В подвале на стене выцарапаны странные символы.")
            print("Вы заметили деталь: странные символы на стене!")
        elif current_room == "attic" and "На чердаке найдена карта с пометками" not in clues:
            add_clue(clues, "На чердаке найдена карта с пометками.")
            print("Вы заметили деталь: карта с пометками!")

    elif command == "take":
        item = raw_arg
        if not item:
            print("Используйте: возьми [предмет]. Например: возьми ключ")
            continue

        if current_room == "study" and item in ["ключ", "key"] and not has_key:
            has_key = True
            print("Вы взяли старинный ключ с гравировкой.")
        elif current_room == "basement" and item in ["фонарь", "lantern"] and not lantern_taken:
            lantern_taken = True
            print("Вы подобрали ржавый фонарь.")
        elif current_room == "bedroom" and item in ["письмо", "letter"] and not letter_taken:
            letter_taken = True
            print("Вы взяли пожелтевшее письмо.")
        elif current_room == "attic" and item in ["карта", "map"] and not map_taken:
            map_taken = True
            print("Вы свернули пыльную карту.")
        else:
            print("Такого предмета здесь нет или вы уже взяли его.")

    elif command == "use":
        item = raw_arg
        if not item:
            print("Используйте: используй [предмет]")
            continue

        if item in ["фонарь", "lantern"] and lantern_taken:
            print("Вы зажгли фонарь. Стало светлее, но всё равно жутковато.")
        elif item in ["карта", "map"] and map_taken:
            print("На карте отмечены скрытые проходы. Похоже, в холле есть люк.")
        elif item in ["письмо", "letter"] and letter_taken:
            print("Письмо написано неразборчиво, но в нём упоминается кто-то из прежних хозяев.")
        else:
            print("У вас нет этого предмета или его нельзя использовать сейчас.")

    elif command == "clues":
        print(f"Собрано улик: {count_clues(clues)}")
        long_clues = get_long_clues(clues)
        if long_clues:
            print("Длинные улики (длина > 5 символов):")
            for c in long_clues:
                print(f"  - {c}")

        formatted = format_clues(clues)
        if formatted:
            print("Полный список улик:")
            for f in formatted:
                print(f"  {f}")

    elif command == "inventory":
        inv_list = []
        if lantern_taken: inv_list.append("фонарь")
        if letter_taken: inv_list.append("письмо")
        if map_taken: inv_list.append("карта")
        if has_key: inv_list.append("ключ")

        if not inv_list:
            print("Ваш инвентарь пуст.")
        else:
            print("У вас: " + ", ".join(inv_list))

    elif command == "exit":
        if current_room != "exit":
            print("Сначала дойдите до входной двери (команда: иди выход).")
        elif not has_key:
            print("Дверь заперта. Нужен ключ!")
        else:
            total = count_clues(clues)
            if total >= 4:
                ending = ("Вы вставили ключ в замок. Щёлчок — и дверь открылась. "
                          "Благодаря собранным уликам вы поняли, что особняк был построен как ловушка. "
                          "Теперь вы знаете больше, чем хотели бы. Вы выходите в рассвет.")
            elif total >= 2:
                ending = ("Ключ повернулся в замке. Дверь распахнулась. "
                          "Улик хватило, чтобы сложить картину, но не все загадки разгаданы. "
                          "Вы покидаете особняк, чувствуя, что история ещё не закончена.")
            else:
                ending = ("Дверь открылась. Вы вышли, но почти ничего не поняли. "
                          "Особняк хранит свои тайны, а вы уносите с собой лишь обрывки догадок.")
            print(ending)
            break

    else:
        print("Неизвестная команда. Введите 'помощь' для списка команд.")




