# mansion.py

ROOM_DESCRIPTIONS = {
    "hall": "Вы в холле. Пыльно и тихо. У двери — свежие капли грязи.",
    "library": "Вы в библиотеке. Старые книги, запах пыли. На полу лежит перчатка с монограммой.",
    "study": "Вы в кабинете. Массивный стол, кресло. На столе — старинный ключ и пепельница.",
    "bedroom": "Вы в спальне. На тумбочке — письмо. Возле кровати — царапины на паркете.",
    "basement": "Вы в подвале. Сыро и темно. На стене — странные символы.",
    "attic": "Вы на чердаке. Паутина, коробки. В одной из них — карта с пометками.",
    "exit": "Вы у входной двери. Тяжёлая дубовая дверь заперта. В скважине — белый воск."
}

# Состояние игры (хранится прямо в модуле для простоты квеста)
clues = []
visited_rooms = set()
has_key = False
lantern_taken = False
letter_taken = False
map_taken = False


def add_clue(clues_list, clue_text):
    clues_list.append(clue_text)


def count_clues(clues_list):
    return len(clues_list)


def describe(room):
    return ROOM_DESCRIPTIONS.get(room, "Вы в неизвестной комнате. Вокруг темно и тихо.")


def visit_room(room):
    if room not in visited_rooms:
        visited_rooms.add(room)


def get_long_clues(clues_list):
    return [c for c in clues_list if len(c) > 5]


def format_clues(clues_list):
    return [f"Улика: {c}" for c in clues_list]


def show_help():
    print("Доступные команды:")
    print("  иди [холл, библиотека, кабинет, спальня, подвал, чердак, выход]")
    print("  осмотри — изучить комнату")
    print("  возьми [предмет] — подобрать вещь")
    print("  используй [предмет] — применить вещь")
    print("  улики — показать статистику и список")
    print("  инвентарь — показать вещи у вас")
    print("  выход — завершить игру (если у двери и есть ключ)")


# --- НОВЫЕ ФУНКЦИИ ДЛЯ ЛОГИКИ ---

def try_move(current_room, target_room, ROOM_NAMES_RU):
    """Пытается переместить игрока. Возвращает (new_room, message). Если нельзя — (None, error_message)."""
    
    # Проверка: можно ли вообще в эту комнату (существует ли ключ)
    if target_room not in ROOM_NAMES_RU:
        return None, "Такой комнаты не существует."

    # Логика перемещений (граф комнат)
    if current_room == "hall":
        allowed = ["library", "study", "bedroom", "basement", "attic", "exit"]
        if target_room in allowed:
            return target_room, f"Вы прошли в {ROOM_NAMES_RU[target_room]}."
        else:
            return None, "Из холла можно пойти только в: библиотека, кабинет, спальня, подвал, чердак, выход."
    
    else:
        # Из любой другой комнаты можно только в холл
        if target_room == "hall":
            return "hall", "Вы вернулись в холл."
        else:
            return None, "Отсюда можно вернуться только в холл (команда: иди холл)."


def look_room(current_room):
    """Обрабатывает команду 'осмотри': выводит описание и добавляет улики."""
    print(describe(current_room))

    # Короткие улики (≤5 символов)
    short_clues = {
        "hall": ("след", "Вы заметили деталь: свежий след на полу!"),
        "basement": ("пыль", "Вы заметили деталь: толстый слой пыли на ящике!"),
        "attic": ("тень", "Вы заметили деталь: странная тень в углу чердака!")
    }

    if current_room in short_clues:
        clue_text, msg = short_clues[current_room]
        if clue_text not in clues:
            add_clue(clues, clue_text)
            print(msg)
            return

    # Длинные улики
    long_clues_map = {
        "library": ("В библиотеке найдена перчатка с монограммой.", "Вы заметили деталь: перчатка с монограммой!"),
        "study": ("В кабинете в пепельнице сигарета с редким сортом табака.", "Вы заметили деталь: дорогая сигарета в пепельнице!"),
        "bedroom": ("Возле кровати в спальне свежие царапины на паркете.", "Вы заметили деталь: царапины на паркете у кровати!"),
        "exit": ("Замочная скважина входной двери залита воском.", "Вы заметили деталь: воск в замочной скважине!")
    }

    if current_room in long_clues_map:
        clue_text, msg = long_clues_map[current_room]
        if clue_text not in clues:
            add_clue(clues, clue_text)
            print(msg)
            return

    print("Здесь вы уже всё осмотрели.")


def take_item(current_room, item_name):
    """Обрабатывает команду 'возьми'. Возвращает True, если предмет взят."""
    # ЭТА СТРОКА ДОЛЖНА БЫТЬ ПЕРВОЙ ВНУТРИ ФУНКЦИИ
    global has_key, lantern_taken, letter_taken, map_taken

    item_name = item_name.lower()

    if current_room == "study" and item_name in ["ключ", "key"] and not has_key:
        has_key = True
        print("Вы взяли старинный ключ с гравировкой.")
        return True

    elif current_room == "basement" and item_name in ["фонарь", "lantern"] and not lantern_taken:
        lantern_taken = True
        print("Вы подобрали ржавый фонарь.")
        return True

    elif current_room == "bedroom" and item_name in ["письмо", "letter"] and not letter_taken:
        letter_taken = True
        print("Вы взяли пожелтевшее письмо.")
        return True

    elif current_room == "attic" and item_name in ["карта", "map"] and not map_taken:
        map_taken = True
        print("Вы свернули пыльную карту.")
        return True

    print("Такого предмета здесь нет или вы уже взяли его.")
    return False




def use_item(item_name):
    """Обрабатывает команду 'используй'."""
    item_name = item_name.lower()

    if item_name in ["фонарь", "lantern"] and lantern_taken:
        print("Вы зажгли фонарь. Стало светлее, но всё равно жутковато.")
        return True
    elif item_name in ["карта", "map"] and map_taken:
        print("На карте отмечены скрытые проходы. Похоже, в холле есть люк.")
        return True
    elif item_name in ["письмо", "letter"] and letter_taken:
        print("Письмо написано неразборчиво, но в нём упоминается кто-то из прежних хозяев.")
        return True
    else:
        print("У вас нет этого предмета или его нельзя использовать сейчас.")
        return False
    
def get_ending(total_clues):
    """Возвращает текст финала в зависимости от количества собранных улик."""
    if total_clues >= 6:
        return (
            "Вы вставили ключ в замок. Щёлчок — и дверь открылась. "
            "Собранные улики сложились в полную картину: особняк был ловушкой, "
            "а прежние хозяева — лишь куклами в чужой игре. "
            "Вы выходите в рассвет, зная ровно то, что нужно. Лучшая развязка!"
        )
    elif total_clues >= 3:
        return (
            "Ключ повернулся в замке. Дверь распахнулась. "
            "Улик хватило, чтобы понять главное: кто-то возвращался в дом через чёрный ход "
            "и оставлял следы для того, кто сумеет их прочитать. "
            "Но не все загадки разгаданы — часть истории осталась за дверью. "
            "Вы покидаете особняк с ощущением, что история ещё не закончена."
        )
    elif total_clues >= 1:
        return (
            "Дверь открылась. Вы вышли на свежий воздух, "
            "но улики, которые вы собрали, лишь добавили вопросов. "
            "Капли грязи, тень на чердаке, пыль в подвале — обрывки, из которых картину не собрать. "
            "Особняк хранит свои тайны, а вы уносите с собой только догадки."
        )
    else:
        return (
            "Дверь открылась без вопросов и без ответов. "
            "Вы вышли, не поняв абсолютно ничего: кто хлопал дверью наверху, "
            "кто оставил след у порога. Особняк победил — он остался такой же загадкой, "
            "какой был в начале. Возможно, стоит вернуться и осмотреть всё как следует."
        )



