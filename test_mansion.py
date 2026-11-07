import pytest
from mansion import add_clue, count_clues, describe, get_long_clues, format_clues, clues, visited_rooms

def test_add_clue():
    clues.clear()
    add_clue(clues, "Перчатка с монограммой")
    assert len(clues) == 1
    assert clues[0] == "Перчатка с монограммой"

def test_count_clues():
    clues.clear()
    add_clue(clues, "Странный символ на стене")
    add_clue(clues, "Пожелтевшее письмо")
    assert count_clues(clues) == 2

def test_describe():
    assert describe("hall").startswith("Вы в холле")
    assert describe("study").startswith("Вы в кабинете")
    assert describe("unknown_room").startswith("Вы в неизвестной комнате")

def test_long_clues():
    clues.clear()
    add_clue(clues, "Ключ")
    add_clue(clues, "Перчатка с монограммой")
    add_clue(clues, "Записка")
    long_clues = get_long_clues(clues)
    assert len(long_clues) == 2
    assert "Ключ" not in long_clues

def test_format_clues():
    clues.clear()
    add_clue(clues, "Странный символ на стене")
    formatted = format_clues(clues)
    assert formatted == ["Улика: Странный символ на стене"]
