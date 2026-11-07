# mansion.py

ROOM_DESCRIPTIONS = {
    "hall": "Вы в холле. Пыльно и тихо. Сквозняк гуляет по полу.",
    "library": "Вы в библиотеке. Старые книги, запах пыли. На полу лежит перчатка с монограммой.",
    "study": "Вы в кабинете. Массивный стол, кресло. На столе лежит старинный ключ.",
    "bedroom": "Вы в спальне. На тумбочке лежит пожелтевшее письмо.",
    "basement": "Вы в подвале. Сыро и темно. На стене выцарапаны странные символы.",
    "attic": "Вы на чердаке. Паутина, коробки. В одной из них карта с пометками.",
    "exit": "Вы у входной двери. Тяжёлая дубовая дверь заперта. Нужен ключ."
}

clues = []
visited_rooms = set()

def add_clue(clues_list, clue_text):
    clues_list.append(clue_text)

def count_clues(clues_list):
    return len(clues_list)

def describe(room):
    return ROOM_DESCRIPTIONS.get(room, "Вы в неизвестной комнате. Вокруг темно и тихо.")

def visit_room(room):
    if room not in visited_rooms:
        visited_rooms.add(room)
        if room in ["library", "basement", "attic"]:
            add_clue(clues, f"Улика из комнаты {room}: найдена важная деталь.")

def get_long_clues(clues_list):
    return [c for c in clues_list if len(c) > 5]

def format_clues(clues_list):
    return [f"Улика: {c}" for c in clues_list]



