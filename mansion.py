from random import *

#random.seed(42)  # для воспроизводимости при проверке

# Константы комнат
ROOM_HALL = "hall"
ROOM_LIBRARY = "library"
ROOM_STUDY = "study"
ROOM_BEDROOM = "bedroom"
ROOM_BASEMENT = "bedroom"
ROOM_BASEMENT = "basement"
ROOM_ATTIC = "attic"
ROOM_EXIT = "exit"

def help():
    return (
        "Доступные команды:\n"
        "  помощь                — показать список команд\n"
        "  осмотри             — описание текущей комнаты\n"
        "  иди в <комната>       — перейти в комнату (например: иди в библиотеку)\n"
        "  возьми <предмет>      — взять предмет\n"
        "  используй <предмет>   — использовать предмет\n"
        "  инвентарь             — показать инвентарь\n"
        "  выход                 — завершить игру"
    )


def describe(room):
    if room == ROOM_HALL:
        return "Вы в холле. Отсюда можно: библиотека, кабинет, спальня, подвал, чердак, выход."
    if room == ROOM_LIBRARY:
        return "В библиотеке на полу перчатка с монограммой."
    if room == ROOM_STUDY:
        return "В кабинете на столе лежит старинный ключ."
    if room == ROOM_BEDROOM:
        return "В спальне на тумбочке пожелтевшее письмо."
    if room == ROOM_BASEMENT:
        return "В подвале на стене странные символы, в углу — ржавый фонарь."
    if room == ROOM_ATTIC:
        return "На чердаке среди коробок — карта с пометками."
    if room == ROOM_EXIT:
        return "У входной двери. Дверь заперта. Нужен ключ."
    return "Неизвестная комната."

def move(current, target):
    # из холла можно в конкретные комнаты
    if current == ROOM_HALL:
        if target == "библиотека": return ROOM_LIBRARY
        if target == "кабинет": return ROOM_STUDY
        if target == "спальня": return ROOM_BEDROOM
        if target == "подвал": return ROOM_BASEMENT
        if target == "чердак": return ROOM_ATTIC
        if target == "выход": return ROOM_EXIT
        return None
    # из любой другой комнаты только в холл
    if target == "холл":
        return ROOM_HALL
    return None

def event():
    r = randint(1, 4)
    if r == 1: return "Скрипнула половица."
    if r == 2: return "Хлопнула дверь на этаже."
    if r == 3: return "В темноте мелькнула тень."
    return "Тишину нарушает тихий шёпот."

def can_take(room, item):
    if room == ROOM_STUDY and item == "ключ": return True
    if room == ROOM_BASEMENT and item == "фонарь": return True
    if room == ROOM_LIBRARY and item == "перчатка": return True
    if room == ROOM_BEDROOM and item == "письмо": return True
    if room == ROOM_ATTIC and item == "карта": return True
    return False

def random_clue():
    r =   randint(1, 5)  # 5 вариантов улик
    if r == 1:
        return "За шкафом вы заметили выцветшую фотографию — на ней тот же особняк, но в другом цвете."
    elif r == 2:
        return "Под половицей лежит обрывок письма с датой: «17.03.1923»."
    elif r == 3:
        return "На подоконнике — крошечная пуговица с гербом. Она явно не от современной одежды."
    elif r == 4:
        return "В щели между досками — старая монета. На ней выбит незнакомый символ."
    else:  # r == 5
        return "На стене едва заметна царапина: похоже, кто-то пытался что-то записать."

