from mansion import describe, move, event, can_take, help, random_clue

# состояние
room = "hall"
clues = 0
has_key = False

# флаги осмотра (чтобы не давать улику дважды)
lib_seen = False
bed_seen = False
base_seen = False
att_seen = False

lantern_taken = False
letter_taken = False
map_taken = False
glove_taken = False

print("Квест: Таинственный особняк")
print("Команды: иди [комната], осмотри, возьми [предмет], используй [предмет], инвентарь, улики, выход")
print(describe(room))

while True:
    cmd = input("> ").strip().lower()
    if not cmd:
        continue

    parts = cmd.split()
    action = parts[0]

    # иди
    if action == "иди":
        target = parts[1] if len(parts) > 1 else ""
        new_room = move(room, target)
        if new_room:
            room = new_room
            print(f"Вы прошли в {target}.")
            print(event())
            print(random_clue())
        else:
            print("Туда нельзя пройти.")
        continue

    # осмотри
    if action == "осмотри":
        msg = describe(room)
        # логика 
        if room == "library" and not lib_seen:
            clues += 1
            lib_seen = True
            msg += " Вы нашли перчатку — это улика!"
        elif room == "bedroom" and not bed_seen:
            clues += 1
            bed_seen = True
            msg += " Вы нашли письмо — это улика!"
        elif room == "basement" and not base_seen:
            clues += 1
            base_seen = True
            msg += " На стене символы — это улика! В углу фонарь."
        elif room == "attic" and not att_seen:
            clues += 1
            att_seen = True
            msg += " В коробке карта — это улика!"

        print(msg)
        print(event())
        continue

    # возьми
    if action == "возьми":
        item = parts[1] if len(parts) > 1 else ""
        if not can_take(room, item):
            print("Такого предмета здесь нет.")
            continue

        if item == "ключ" and not has_key:
            has_key = True
            print("Вы взяли ключ.")
        elif item == "фонарь" and not lantern_taken:
            lantern_taken = True
            print("Вы подобрали фонарь.")
        elif item == "перчатка" and not glove_taken:
            glove_taken = True
            print("Вы подобрали перчатку.")
        elif item == "письмо" and not letter_taken:
            letter_taken = True
            print("Вы взяли письмо.")
        elif item == "карта" and not map_taken:
            map_taken = True
            print("Вы свернули карту.")
        else:
            print("Этот предмет у вас уже есть.")
        continue

    # используй
    if action == "используй":
        item = parts[1] if len(parts) > 1 else ""
        if item == "фонарь" and lantern_taken:
            print("Стало светлее, но всё равно жутко.")
        elif item == "карта" and map_taken:
            print("На карте отмечены скрытые проходы.")
        elif item == "письмо" and letter_taken:
            print("Письмо неразборчиво, но там упоминается прежний хозяин.")
        elif item == "перчатка" and glove_taken:
            print("На внутренней стороне монограмма: «B.S.»")
        else:
            print("Нельзя использовать этот предмет сейчас.")
        continue

    # инвентарь
    if action == "инвентарь":
        inv = ""
        if lantern_taken: inv+="фонарь"
        if letter_taken: inv+="письмо"
        if map_taken: inv.append+="карта"
        if glove_taken: inv+="перчатка"
        if has_key: inv+="ключ"

        if inv:
            print(f"У вас: {inv}")
        else:
            print("Инвентарь пуст.")
        continue

    # улики
    if action == "улики":
        print(f"Собрано улик: {clues}")
        continue

    if action == "помощь":
        print(help())

    # выход
    if action == "выход":
        if room != "exit":
            print("Сначала дойдите до двери (иди выход).")
            continue
        if not has_key:
            print("Дверь заперта. Нужен ключ!")
            continue

        # финал по количеству улик
        if clues >= 4:
            print("Ключ щёлкнул. Дверь открылась. Вы узнали слишком много… Выходите в рассвет.")
        elif clues >= 2:
            print("Ключ повернулся. Дверь распахнулась. Не все загадки разгаданы — история продолжается.")
        else:
            print("Дверь открылась. Вы вышли, почти ничего не поняв. Особняк хранит свои тайны.")
        break

    print("Неизвестная команда. Введите помощь.")



