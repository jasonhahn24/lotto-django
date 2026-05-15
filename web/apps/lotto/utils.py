import secrets

def generate_auto_numbers():
    pool = list(range(1, 46))
    selected = []
    while len(selected) < 6:
        idx = secrets.randbelow(len(pool))
        selected.append(pool.pop(idx))
    return sorted(selected)

def check_prize_rank(ticket_numbers, draw_numbers, bonus):
    ticket_set = set(ticket_numbers)
    draw_set   = set(draw_numbers)
    matched    = len(ticket_set & draw_set)
    has_bonus  = bonus in ticket_set

    if   matched == 6:               return 1, '1등 🎉 (6개 일치)'
    elif matched == 5 and has_bonus: return 2, '2등 🎊 (5개 + 보너스)'
    elif matched == 5:               return 3, '3등 🥳 (5개 일치)'
    elif matched == 4:               return 4, '4등 😊 (4개 일치)'
    elif matched == 3:               return 5, '5등 🙂 (3개 일치)'
    else:                            return 0, '낙첨 😢'