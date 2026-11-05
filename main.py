import os
import random


# Настройки критического урона
CRITICAL_CHANCE = 0.20
CRITICAL_MULTIPLIER = 2


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def create_hero(name):
    return {
        "name": name,
        "hp": 45,
        "max_hp": 45,
        "potions": 2,
        "victories": 0
    }


def calculate_healing(hp, max_hp, amount):
    return min(amount, max_hp - hp)


def calculate_attack_damage():
    damage = random.randint(7, 12)

    is_critical = random.random() < CRITICAL_CHANCE

    if is_critical:
        damage *= CRITICAL_MULTIPLIER

    return damage, is_critical


def use_potion(hero):
    if hero["potions"] == 0:
        return False, "Зелья закончились!"

    healed = calculate_healing(
        hero["hp"], hero["max_hp"], 20
    )

    if healed == 0:
        return False, "У тебя полное здоровье!"

    hero["hp"] += healed
    hero["potions"] -= 1

    return True, f"Восстановлено {healed} HP!"


def draw_screen(hero, enemy, room, messages):
    clear_screen()

    print("=" * 38)
    print(f" ПОДЗЕМЕЛЬЕ АУРИОНА | КОМНАТА {room}/3")
    print("=" * 38)

    print(f"\nГЕРОЙ: {hero['name']}")
    print(f"HP: {hero['hp']}/{hero['max_hp']}")
    print(f"Зелья здоровья: {hero['potions']}")

    print("\n" + "-" * 38)

    print(f"ВРАГ: {enemy['name']}")
    print(f"HP: {enemy['hp']}/{enemy['max_hp']}")

    print("\n" + "-" * 38)
    print("ПОСЛЕДНИЙ ХОД:")

    for message in messages:
        print(f" > {message}")

    print("-" * 38)

    if hero["hp"] > 0 and enemy["hp"] > 0:
        print("\n1. Атаковать")
        print("2. Выпить зелье")
        print("3. Характеристики")


def battle(hero, enemy_data, room, start_message):
    enemy = enemy_data.copy()
    enemy["max_hp"] = enemy["hp"]

    messages = [start_message]

    while True:
        draw_screen(hero, enemy, room, messages)

        if hero["hp"] <= 0 or enemy["hp"] <= 0:
            input("\nНажми Enter, чтобы продолжить...")
            return hero["hp"] > 0

        choice = input("\nВыбери действие: ").strip()

        if choice == "1":
            damage, is_critical = calculate_attack_damage()

            enemy["hp"] = max(0, enemy["hp"] - damage)

            if is_critical:
                messages = [
                    f"⚡ КРИТИЧЕСКИЙ УДАР! {damage} урона!"
                ]
            else:
                messages = [
                    f"Ты нанес {damage} урона!"
                ]

        elif choice == "2":
            success, message = use_potion(hero)
            messages = [message]

            if not success:
                continue

        elif choice == "3":
            messages = [
                f"Имя: {hero['name']}",
                f"Побед: {hero['victories']}",
                f"Зелий: {hero['potions']}",
                f"Шанс крита: {CRITICAL_CHANCE:.0%}"
            ]
            continue

        else:
            messages = ["Неверная команда! Попробуй снова."]
            continue

        # Проверка победы над противником
        if enemy["hp"] <= 0:
            hero["victories"] += 1
            messages.append(f"{enemy['name']} побежден!")
            continue

        # Ответная атака противника
        enemy_damage = random.randint(
            enemy["min_damage"],
            enemy["max_damage"]
        )

        hero["hp"] = max(0, hero["hp"] - enemy_damage)

        messages.append(
            f"Противник нанес {enemy_damage} урона!"
        )

        if hero["hp"] == 0:
            messages.append("Твой герой погиб!")


def main():
    clear_screen()

    print("=" * 38)
    print("         ПОДЗЕМЕЛЬЕ АУРИОНА")
    print("=" * 38)

    print("\nДобро пожаловать в Гильдию!")
    name = input("Как зовут твоего героя? ").strip()

    if not name:
        name = "Путник"

    hero = create_hero(name)

    print(f"\nПриветствую, {hero['name']}!")
    print("Тебе предстоит пройти три комнаты.")
    print("В последней тебя ждет Древний Страж!")

    input("\nНажми Enter, чтобы начать...")

    enemies = [
        {
            "name": "Пещерный слизень",
            "hp": 18,
            "min_damage": 2,
            "max_damage": 5
        },
        {
            "name": "Скелет-воин",
            "hp": 25,
            "min_damage": 3,
            "max_damage": 7
        },
        {
            "name": "Древний Страж",
            "hp": 35,
            "min_damage": 4,
            "max_damage": 9
        }
    ]

    start_message = "Бой начинается!"

    for room, enemy in enumerate(enemies, start=1):
        victory = battle(
            hero, enemy, room, start_message
        )

        if not victory:
            clear_screen()
            print("=" * 38)
            print("           ИГРА ОКОНЧЕНА")
            print("=" * 38)

            print(f"\nПобеждено монстров: {hero['victories']}")
            print("Попробуй пройти подземелье еще раз!")
            break

        if room < len(enemies):
            hero["potions"] += 1
            start_message = "Ты нашел зелье здоровья! +1"

    else:
        clear_screen()
        print("=" * 38)
        print("              ПОБЕДА!")
        print("=" * 38)

        print("\nТы победил Древнего Стража!")
        print("Первый артефакт Гильдии теперь твой!")

        print(f"\nОставшееся HP: {hero['hp']}")
        print(f"Побеждено монстров: {hero['victories']}")


if __name__ == "__main__":
    main()
