# mansion.py

ROOM_DESCRIPTIONS = {
    "hall": "Вы в холле. Пыльно и тихо. Сквозняк гуляет по полу. У входной двери на ковре блестят свежие капли грязи.",
    "library": "Вы в библиотеке. Старые книги, запах пыли. На полу лежит перчатка с монограммой.",
    "study": "Вы в кабинете. Массивный стол, кресло. На столе лежит старинный ключ, а в пепельнице — недокуренная сигарета.",
    "bedroom": "Вы в спальне. На тумбочке лежит пожелтевшее письмо. Возле кровати — свежие царапины на паркете.",
    "basement": "Вы в подвале. Сыро и темно. На стене выцарапаны странные символы.",
    "attic": "Вы на чердаке. Паутина, коробки. В одной из них карта с пометками.",
    "exit": "Вы у входной двери. Тяжёлая дубовая дверь заперта. В замочной скважине — белый воск, будто кто-то не хотел, чтобы её открыли."
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


def get_long_clues(clues_list):
    return [c for c in clues_list if len(c) > 5]


def format_clues(clues_list):
    return [f"Улика: {c}" for c in clues_list]
    



