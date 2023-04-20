def create_bars(value, max):
    perc = (float(value) / float(max)) * 100
    str = ""
    emp = ""
    first_digit = 0

    if perc >= 10:
        if perc == 100:
            first_digit = 10
        else:
            first_digit = int(perc // 10)

    for i in range(first_digit):
        str += ":blue_square:"
    for y in range(10 - first_digit):
        emp += ":black_large_square:"

    str += emp
    return str


def create_health_bar(health, max_health):
    perc = (float(health) / float(max_health)) * 100
    str = ""
    emp = ""
    first_digit = 0

    if perc >= 10:
        if perc == 100:
            first_digit = 10
        else:
            first_digit = int(perc // 10)

    for i in range(first_digit):
        str += ":white_large_square:"
    for y in range(10 - first_digit):
        emp += ":red_square:"

    str += emp
    return str


def create_stamina_bar(stamina, max_stamina):
    perc = (float(stamina) / float(max_stamina)) * 100
    str = ""
    emp = ""
    first_digit = 0

    if perc >= 10:
        if perc == 100:
            first_digit = 10
        else:
            first_digit = int(perc // 10)

    for i in range(first_digit):
        str += ":blue_square:"
    for y in range(10 - first_digit):
        emp += ":black_large_square:"

    str += emp
    return str


def create_invisible_spaces(amount):
    white = ""
    for x in range(amount):
        white += "\u200E "
    return white


def calculate_upgrade_cost(user, next_upgrade_cost):
    level = user.get_all_stat_levels() + (
        1 if next_upgrade_cost else 0) - 80  # -80 because that's if every stat default is 10
    x = max(((level + 81) - 92) * 0.02, 0)  # Ensure x is not negative
    rune_cost = int((x + 0.1) * ((level + 81) ** 2)) + 1
    total_cost = 150 + round((int(level) * 150) * 2, 0)
    return total_cost + rune_cost
