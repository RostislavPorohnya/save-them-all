import random
import os
import platform


def clear_screen():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


def get_prefix(value, prefix_map):
    for max_val, prefix in prefix_map:
        if value <= max_val:
            return prefix
    return prefix_map[-1][1]


def upgrade_max_hp(p):
    p["max_hp"] += 2
    p["hp"] = p["max_hp"]
    print("Your life force grows! Max HP:", p["max_hp"])


def upgrade_str(p):
    p["str"] += 1
    print("Your muscles ripple with power! STR:", p["str"])


def upgrade_cha(p):
    p["cha"] += 1
    print("Your words drip with honeyed charm! CHA:", p["cha"])


UPGRADE_ACTIONS = {
    "1": upgrade_max_hp,
    "2": upgrade_str,
    "3": upgrade_cha
}


def upgrade_choice(player):
    print("\nYou find a mystical shrine offering a choice:")
    print("1) Increase Max HP by 2")
    print("2) Increase Strength by 1")
    print("3) Increase Charisma by 1")
    choice = input("> ").strip()
    if choice in UPGRADE_ACTIONS:
        UPGRADE_ACTIONS[choice](player)


def generate_room():
    return random.choices(["enemy", "potion", "empty", "treasure"], [0.7, 0.1, 0.1, 0.1])[0]


def find_potion(player):
    heal = random.randint(2,4)
    if player["potion"] is None:
        player["potion"] = heal
        print(f"You find a healing potion (Heals {heal}). You store it.")
    else:
        print("You find a potion, but you already have one. You leave it.")


def find_treasure(player):
    gold_found = random.randint(2,5)
    player["gold"] += gold_found
    print(f"You find a small pile of gold: +{gold_found} gold. Total gold: {player['gold']}")


def room_navigation_menu():
    print("[1=Move On, 2=Exit]")
    action = input("> ").strip()
    return action != "2"


def combat_menu():
    print("[1=Attack, 2=Negotiate, 3=Use Potion, 4=Exit]")
    return input("> ").strip()


def use_potion(player):
    if player["potion"] is not None:
        heal_val = player["potion"]
        player["hp"] = min(player["hp"] + heal_val, player["max_hp"])
        player["potion"] = None
        print(f"You drink the potion and restore {heal_val} HP. HP:{player['hp']}/{player['max_hp']}")
    else:
        print("You have no potions!")


HP_PREFIX_MAP = [
    (3, "Weak"),
    (6, "Tough"),
    (9999, "Deadly")
]

GREED_PREFIX_MAP = [
    (0, "Honorable"),
    (2, "Greedy"),
    (5, "Ruthless"),
    (9999, "Merciless")
]

ATTACK_PREFIX_MAP = [
    (2, "Feeble"),
    (4, "Fierce"),
    (6, "Savage"),
    (9999, "Devastating")
]


def encounter_enemy(player, enemy_names, scale_stats):
    enemy_hp = random.randint(2,4) + scale_stats["hp"]
    enemy_attack = random.randint(1,2) + scale_stats["attack"]
    enemy_base_greed = random.randint(2,5) + scale_stats["greed"]
    enemy_greed = max(0, enemy_base_greed - player["cha"])

    enemy_name = random.choice(enemy_names)

    hp_prefix = get_prefix(enemy_hp, HP_PREFIX_MAP)
    greed_prefix = get_prefix(enemy_greed, GREED_PREFIX_MAP)
    attack_prefix = get_prefix(enemy_attack, ATTACK_PREFIX_MAP)

    print(f"A foe stands before you! {hp_prefix} {attack_prefix} {enemy_name} the {greed_prefix}")
    print(f"Your HP:{player['hp']}/{player['max_hp']} STR:{player['str']} CHA:{player['cha']} Gold:{player['gold']}"
          f" Potion:{'Yes' if player['potion'] else 'No'}")

    ended_by_negotiation = False
    while enemy_hp > 0 and player["hp"] > 0:
        action = combat_menu()
        match action:
            case "1":
                enemy_hp -= player["str"]
                if enemy_hp > 0:
                    player["hp"] -= enemy_attack
                print(f"You strike! Your HP:{player['hp']}/{player['max_hp']}")
            case "2":
                if player["gold"] >= enemy_greed:
                    player["gold"] -= enemy_greed
                    print(f"You pay off the foe with {enemy_greed} gold. They leave peacefully.")
                    enemy_hp = 0
                    ended_by_negotiation = True
                else:
                    print("Not enough gold to sway them!")
            case "3":
                use_potion(player)
            case "4":
                player["hp"] = 0
            case _:
                print("Invalid action!")

    if enemy_hp <= 0 < player["hp"] and not ended_by_negotiation:
        loot = random.randint(1,3)
        player["gold"] += loot
        print(f"You defeated the foe! You loot {loot} gold. Total gold: {player['gold']}")


def handle_empty_room(player):
    print("The room is empty.")
    return room_navigation_menu()


def handle_potion_room(player):
    find_potion(player)
    return room_navigation_menu()


def handle_treasure_room(player):
    find_treasure(player)
    return room_navigation_menu()


def handle_enemy_room(player, enemy_names, scale_stats):
    encounter_enemy(player, enemy_names, scale_stats)
    if player["hp"] <= 0:
        return False
    return room_navigation_menu()


def apply_random_scale(scale_stats):
    params = ["hp", "attack", "greed"]
    chosen = random.sample(params, 2)
    for c in chosen:
        scale_stats[c] += 1

ROOM_HANDLERS = {
    "empty": handle_empty_room,
    "potion": handle_potion_room,
    "treasure": handle_treasure_room
}

def main():
    player = {
        "hp": 10,
        "max_hp": 10,
        "str": 2,
        "cha": 1,
        "gold": 5,
        "potion": None
    }
    room_count = 0
    enemy_names = ["Zarg", "Mogul", "Hilda", "Brak", "Zyra", "Throg"]
    brother_found = False

    scale_stats = {"hp":0, "attack":0, "greed":0}

    clear_screen()
    print("Your beloved brother has been taken by monsters into an endless dungeon.")
    print("You venture forth, determined to rescue him.")
    print("Type '4' in a room prompt or during combat to exit the game (or Ctrl+C).")

    try:
        while player["hp"] > 0 and not brother_found:
            room_count += 1
            if room_count % 10 == 0:
                upgrade_choice(player)
                apply_random_scale(scale_stats)

            if room_count >= 30 and random.random() < 0.05:
                clear_screen()
                print("*" * 50)
                print("A faint figure in the shadows... It's your brother!")
                print("You have found him at last, and together you escape.")
                print("*" * 50)
                brother_found = True
                break

            room_type = generate_room()
            print(f"\nRoom {room_count}:")

            if room_type == "enemy":
                cont = handle_enemy_room(player, enemy_names, scale_stats)
            else:
                cont = ROOM_HANDLERS[room_type](player)

            if not cont:
                break

        if player["hp"] <= 0:
            clear_screen()
            print("!" * 50)
            print("You have perished in the dungeon.")
            print("!" * 50)
        elif brother_found:
            pass
        else:
            print("Your adventure ends here.")
    except KeyboardInterrupt:
        print("\nYou have chosen to leave the dungeon. Farewell!")

if __name__ == "__main__":
    main()
