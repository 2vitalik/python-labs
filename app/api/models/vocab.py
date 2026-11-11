"""The game-description language (T98 → T257 → T270): the words the forms offer that are not catalog cards.
The WHEN / IF / THEN dictionaries of rules, the field's and a level's properties, the arguments' human names.
Entity roles, stats and the field's options are catalog cards (kinds role · stat · fieldopt): options.py.
Arg types: entity · window · int · text · bool · choice:<OPTIONS key>. An entity arg takes a Part id, `*` (anyone),
`@a` / `@b` (the sides of the trigger) or `@both`. Templates render the sentence; a `[…]` segment drops when its args are empty."""
import re

PART_KINDS = ("field", "entity", "window", "menu", "level")

OPTIONS = {  # choice lists: value → label
    "dir": {"up": "вгору", "down": "вниз", "left": "ліворуч", "right": "праворуч", "forward": "вперед", "back": "назад",
            "toward": "до цілі", "away": "від цілі", "random": "випадково", "any": "будь-куди", "diagonal": "по діагоналі", "all8": "у 8 напрямків"},
    "op": {"==": "=", "!=": "≠", ">=": "≥", "<=": "≤", ">": ">", "<": "<"},
    "cell": {"target": "цільова клітина", "ahead": "попереду", "behind": "позаду", "under": "під ногами", "neighbors": "сусідні клітини", "any": "будь-яка"},
    "shape": {"line": "лінія", "group": "група сусідів", "row": "повний ряд", "col": "повний стовпець", "region": "замкнена область",
              "loop": "петля", "cross": "хрест", "square": "квадрат", "radius": "радіус"},
    "deg": {"90": "на 90°", "180": "на 180°", "-90": "на −90°"},
    "axis": {"row": "ряд", "col": "стовпець", "all": "усе поле"},
    "clock": {"start": "запустити", "stop": "зупинити", "add": "додати", "sub": "відняти"},
    "where": {"row": "ряд", "col": "стовпець", "region": "регіон", "cage": "клітка", "line": "лінія", "field": "усе поле"},
}


def w(label, tpl, args=(), group=""):
    return {"label": label, "tpl": tpl, "args": [{"name": n, "type": t, "required": r} for n, t, r in args], "group": group}


E, N, T = "entity", "int", "text"  # the common arg types

TRIGGERS = {
    # contact and space
    "contact": w("контакт А × Б", "{a} × {b}", [("a", E, 1), ("b", E, 1)], "контакт"),
    "enter": w("А стає на клітину Б", "{a} стає на {b}", [("a", E, 1), ("b", E, 1)], "контакт"),
    "leave": w("А сходить з Б", "{a} сходить з {b}", [("a", E, 1), ("b", E, 1)], "контакт"),
    "adjacent": w("А поруч із Б", "{a} поруч із {b}", [("a", E, 1), ("b", E, 1)], "контакт"),
    "line_of_sight": w("А бачить Б по прямій", "{a} бачить {b}", [("a", E, 1), ("b", E, 1)], "контакт"),
    "in_range": w("Б у радіусі від А", "{b} ближче {n} до {a}", [("a", E, 1), ("b", E, 1), ("n", N, 1)], "контакт"),
    "blocked": w("А вперся в перешкоду", "{a} вперся", [("a", E, 1)], "контакт"),
    "reach": w("А досяг місця", "{a} досяг {where}", [("a", E, 1), ("where", T, 1)], "контакт"),
    "edge": w("А вийшов за край поля", "{a} за краєм", [("a", E, 1)], "контакт"),
    # input and time
    "input": w("гравець зробив дію", "ввід «{action}»[ для {a}]", [("action", T, 1), ("a", E, 0)], "ввід і час"),
    "timer": w("кожні N тіків", "кожні {every} тіків", [("every", N, 1)], "ввід і час"),
    "tick": w("кожен тік", "кожен тік", (), "ввід і час"),
    "idle": w("гравець не діє N тіків", "бездіяльність {n} тіків", [("n", N, 1)], "ввід і час"),
    "schedule": w("за розкладом", "за розкладом {list}", [("list", T, 1)], "ввід і час"),
    "rng": w("випадково з ймовірністю", "з ймовірністю {p} %", [("p", N, 1)], "ввід і час"),
    "phase_start": w("почалась фаза тіку", "фаза «{phase}»", [("phase", T, 1)], "ввід і час"),
    "turn_start": w("початок ходу сторони", "початок ходу[ {a}]", [("a", E, 0)], "ввід і час"),
    "turn_end": w("кінець ходу сторони", "кінець ходу[ {a}]", [("a", E, 0)], "ввід і час"),
    # state and counters
    "counter": w("лічильник досяг", "{name} {op} {n}", [("name", T, 1), ("op", "choice:op", 1), ("n", N, 1)], "стан і лічильники"),
    "hp_zero": w("HP А вичерпано", "HP {a} = 0", [("a", E, 1)], "стан і лічильники"),
    "state_on": w("А увійшов у стан", "{a} перейшов у стан «{s}»", [("a", E, 1), ("s", T, 1)], "стан і лічильники"),
    "state_off": w("А вийшов зі стану", "{a} вийшов зі стану «{s}»", [("a", E, 1), ("s", T, 1)], "стан і лічильники"),
    "all_gone": w("зникли всі А", "зникли всі {a}", [("a", E, 1)], "стан і лічильники"),
    "all_on": w("усі А на Б", "усі {a} на {b}", [("a", E, 1), ("b", E, 1)], "стан і лічильники"),
    "no_moves": w("нема легальних ходів", "нема ходів[ у {a}]", [("a", E, 0)], "стан і лічильники"),
    "pattern": w("на полі склався шаблон", "шаблон {shape}[ з {n}]", [("shape", "choice:shape", 1), ("n", N, 0)], "стан і лічильники"),
    "settled": w("поле осіло після падінь", "поле осіло", (), "стан і лічильники"),
    # lifecycle and other rules
    "level_start": w("старт рівня", "старт рівня", (), "життєвий цикл"),
    "level_end": w("кінець рівня", "кінець рівня", (), "життєвий цикл"),
    "wave_start": w("старт хвилі", "старт хвилі", (), "життєвий цикл"),
    "wave_cleared": w("хвилю знищено", "хвилю знищено", (), "життєвий цикл"),
    "spawned": w("зʼявився А", "зʼявився {a}", [("a", E, 1)], "життєвий цикл"),
    "died": w("загинув А", "загинув {a}", [("a", E, 1)], "життєвий цикл"),
    "picked": w("А підібрав Б", "{a} підібрав {b}", [("a", E, 1), ("b", E, 1)], "життєвий цикл"),
    "destroyed": w("А знищено", "{a} знищено", [("a", E, 1)], "життєвий цикл"),
    "all_constraints_met": w("усі обмеження виконано (пазл)", "усі обмеження виконано", (), "пазли"),
    "constraint_broken": w("порушено обмеження (пазл)", "порушено обмеження[ «{text}»]", [("text", T, 0)], "пазли"),
    "custom": w("інше (словами)", "{text}", [("text", T, 1)], "інше"),
}

CONDITIONS = {
    "free": w("клітина вільна", "{cell} вільна", [("cell", "choice:cell", 1)], "поле"),
    "occupied": w("у клітині сутність", "у {cell} є {what}", [("cell", "choice:cell", 1), ("what", E, 1)], "поле"),
    "adjacent_count": w("кількість сусідів виду", "сусідів {what} {op} {n}", [("what", E, 1), ("op", "choice:op", 1), ("n", N, 1)], "поле"),
    "count": w("кількість сутностей на полі", "{what} на полі {op} {n}", [("what", E, 1), ("op", "choice:op", 1), ("n", N, 1)], "поле"),
    "path_exists": w("існує шлях", "є шлях від {a} до {b}", [("a", E, 1), ("b", E, 1)], "поле"),
    "connected": w("множина звʼязна", "усі {what} звʼязні", [("what", E, 1)], "поле"),
    "in_check": w("А під ударом", "{a} під ударом", [("a", E, 1)], "хід гри"),
    "fits": w("фігура вміщується", "{a} вміщується у {cell}", [("a", E, 1), ("cell", "choice:cell", 1)], "поле"),
    "state": w("А у стані", "{a} у стані «{s}»", [("a", E, 1), ("s", T, 1)], "стан"),
    "has": w("у А є предмет", "у {a} є {item}", [("a", E, 1), ("item", E, 1)], "стан"),
    "counter": w("лічильник порівняно з N", "{name} {op} {n}", [("name", T, 1), ("op", "choice:op", 1), ("n", N, 1)], "стан"),
    "same": w("А і Б однакові за…", "{a} і {b} однакові за {prop}", [("a", E, 1), ("b", E, 1), ("prop", T, 1)], "стан"),
    "facing": w("А дивиться у напрямку", "{a} дивиться {dir}", [("a", E, 1), ("dir", "choice:dir", 1)], "стан"),
    "moving": w("А рухається у напрямку", "{a} рухається {dir}", [("a", E, 1), ("dir", "choice:dir", 1)], "стан"),
    "in_range": w("Б у радіусі від А", "{b} ближче {n} до {a}", [("a", E, 1), ("b", E, 1), ("n", N, 1)], "стан"),
    "line_of_sight": w("А бачить Б", "{a} бачить {b}", [("a", E, 1), ("b", E, 1)], "стан"),
    "turn_of": w("зараз ходить сторона", "ходить {a}", [("a", E, 1)], "хід гри"),
    "legal": w("хід легальний", "хід легальний[ ({text})]", [("text", T, 0)], "хід гри"),
    "level": w("номер рівня", "рівень {op} {n}", [("op", "choice:op", 1), ("n", N, 1)], "хід гри"),
    "timer": w("часу лишилось", "час {op} {n}", [("op", "choice:op", 1), ("n", N, 1)], "хід гри"),
    "mode": w("режим гри", "режим «{text}»", [("text", T, 1)], "хід гри"),
    "first_time": w("вперше за рівень", "вперше", (), "хід гри"),
    "chain": w("каскад уже N кроків", "каскад ≥ {n}", [("n", N, 1)], "хід гри"),
    "prob": w("з ймовірністю", "з ймовірністю {p} %", [("p", N, 1)], "хід гри"),
    # puzzle predicates: the constraints a marking must satisfy
    "unique": w("усі значення різні", "у {where} значення різні", [("where", "choice:where", 1)], "обмеження пазла"),
    "sum": w("сума дорівнює", "сума у {where} = {n}", [("where", "choice:where", 1), ("n", N, 1)], "обмеження пазла"),
    "no_adjacent": w("не сусідять", "{what} не сусідять", [("what", E, 1)], "обмеження пазла"),
    "no_2x2": w("нема квадрата 2×2", "нема 2×2 з {what}", [("what", E, 1)], "обмеження пазла"),
    "region_size": w("розмір області", "область з {what} має {n} клітин", [("what", E, 1), ("n", N, 1)], "обмеження пазла"),
    "single_loop": w("рівно одна петля", "одна петля", (), "обмеження пазла"),
    "cover_all": w("покрито всі клітини", "усі клітини покриті {what}", [("what", E, 1)], "обмеження пазла"),
    "run_lengths": w("довжини блоків за підказкою", "блоки у {where} за підказкою", [("where", "choice:where", 1)], "обмеження пазла"),
    "custom": w("інше (словами)", "{text}", [("text", T, 1)], "інше"),
}

# a condition's negation (T278 §7): `!…!` marks the word that says «not», `{op:!}` turns the comparison around.
# A word without one (free text) puts «НЕ» before the whole clause
NEG = {
    "free": "{cell} !не! вільна", "occupied": "у {cell} !нема! {what}", "adjacent_count": "сусідів {what} {op:!} {n}",
    "count": "{what} на полі {op:!} {n}", "path_exists": "!нема! шляху від {a} до {b}", "connected": "!не! всі {what} звʼязні",
    "in_check": "{a} !не! під ударом", "fits": "{a} !не! вміщується у {cell}", "state": "{a} !не! у стані «{s}»",
    "has": "у {a} !нема! {item}", "counter": "{name} {op:!} {n}", "same": "{a} і {b} !не! однакові за {prop}",
    "facing": "{a} !не! дивиться {dir}", "moving": "{a} !не! рухається {dir}", "in_range": "{b} !не! ближче {n} до {a}",
    "line_of_sight": "{a} !не! бачить {b}", "turn_of": "ходить !не! {a}", "legal": "хід !не! легальний[ ({text})]",
    "level": "рівень {op:!} {n}", "timer": "час {op:!} {n}", "mode": "режим !не! «{text}»", "first_time": "!не! вперше",
    "chain": "каскад !<! {n}", "prob": "шанс {p} % !не! випав",
    "unique": "у {where} значення !повторюються!", "sum": "сума у {where} !≠! {n}", "no_adjacent": "{what} !сусідять!",
    "no_2x2": "!є! 2×2 з {what}", "region_size": "область з {what} має !не! {n} клітин", "single_loop": "!не! одна петля",
    "cover_all": "!не! всі клітини покриті {what}", "run_lengths": "блоки у {where} !не! за підказкою",
}
for _k, _neg in NEG.items():
    CONDITIONS[_k]["neg"] = _neg
OP_NOT = {"==": "!=", "!=": "==", ">=": "<", "<=": ">", ">": "<=", "<": ">="}

EFFECTS = {
    # appear / disappear
    "disappear": w("зникає", "зникає {a}", [("a", E, 1)], "поява і зникнення"),
    "spawn": w("зʼявляється", "зʼявляється {entity}[ у {cell}]", [("entity", E, 1), ("cell", "choice:cell", 0)], "поява і зникнення"),
    "spawn_at": w("зʼявляється у місці", "зʼявляється {entity} у {where}", [("entity", E, 1), ("where", T, 1)], "поява і зникнення"),
    "transform": w("перетворюється на", "{a} перетворюється на {into}", [("a", E, 1), ("into", E, 1)], "поява і зникнення"),
    "respawn": w("відроджується", "{a} відроджується[ у {where}]", [("a", E, 1), ("where", T, 0)], "поява і зникнення"),
    "clone": w("клонується", "клон {a}", [("a", E, 1)], "поява і зникнення"),
    # movement
    "block": w("рух не відбувається", "блок", (), "рух"),
    "push": w("штовхається", "штовхає {a}", [("a", E, 1)], "рух"),
    "pull": w("тягнеться", "тягне {a}", [("a", E, 1)], "рух"),
    "move": w("рухається на 1", "{a} рухається {dir}", [("a", E, 1), ("dir", "choice:dir", 1)], "рух"),
    "slide": w("ковзає до упору", "{a} ковзає {dir}", [("a", E, 1), ("dir", "choice:dir", 1)], "рух"),
    "teleport": w("телепортується", "{a} телепортується[ у {where}]", [("a", E, 1), ("where", T, 0)], "рух"),
    "wrap": w("переходить через край (тор)", "{a} через край", [("a", E, 1)], "рух"),
    "swap": w("міняються місцями", "{a} і {b} міняються місцями", [("a", E, 1), ("b", E, 1)], "рух"),
    "rotate": w("повертається", "{a} повертається {deg}", [("a", E, 1), ("deg", "choice:deg", 1)], "рух"),
    "fall": w("падає", "{a} падає", [("a", E, 1)], "рух"),
    "bounce": w("відбивається", "{a} відбивається", [("a", E, 1)], "рух"),
    "face": w("розвертається", "{a} дивиться {dir}", [("a", E, 1), ("dir", "choice:dir", 1)], "рух"),
    "shift": w("зсув ряду / поля", "зсув {axis} {dir}", [("axis", "choice:axis", 1), ("dir", "choice:dir", 1)], "рух"),
    "stun": w("завмирає на N тіків", "{a} завмирає на {n}", [("a", E, 1), ("n", N, 1)], "рух"),
    "speed": w("змінює швидкість", "швидкість {a} {n} %", [("a", E, 1), ("n", N, 1)], "рух"),
    "attach": w("зчіплюється", "{a} зчіплюється з {b}", [("a", E, 1), ("b", E, 1)], "рух"),
    # state and numbers
    "damage": w("шкода", "{a} отримує шкоду {n}", [("a", E, 1), ("n", N, 1)], "стан і числа"),
    "heal": w("лікування", "{a} лікується на {n} HP", [("a", E, 1), ("n", N, 1)], "стан і числа"),
    "lives": w("± життя", "життя {n:+}", [("n", N, 1)], "стан і числа"),
    "score": w("± очки", "очки {n:+}", [("n", N, 1)], "стан і числа"),
    "currency": w("± валюта", "валюта {n:+}", [("n", N, 1)], "стан і числа"),
    "counter": w("± лічильник", "{name} {n:+}", [("name", T, 1), ("n", N, 1)], "стан і числа"),
    "set_value": w("встановити значення", "{a} = {v}", [("a", E, 1), ("v", T, 1)], "стан і числа"),
    "multiplier": w("множник очок", "множник ×{k}", [("k", N, 1)], "стан і числа"),
    "set_state": w("увімкнути стан", "{a} стає «{s}»[ на {dur} тіків]", [("a", E, 1), ("s", T, 1), ("dur", N, 0)], "стан і числа"),
    "clear_state": w("зняти стан", "{a} більше не «{s}»", [("a", E, 1), ("s", T, 1)], "стан і числа"),
    "grow": w("росте / зменшується", "{a} росте на {n}", [("a", E, 1), ("n", N, 1)], "стан і числа"),
    "set_side": w("змінює сторону / власника", "{a} переходить до {side}", [("a", E, 1), ("side", T, 1)], "стан і числа"),
    # inventory
    "pickup": w("підбирає в інвентар", "{a} бере {item}", [("a", E, 1), ("item", E, 1)], "інвентар"),
    "take": w("втрачає предмет", "{a} втрачає {item}", [("a", E, 1), ("item", E, 1)], "інвентар"),
    "give": w("отримує предмет", "{a} отримує {item}", [("a", E, 1), ("item", E, 1)], "інвентар"),
    "use": w("використовує предмет", "{a} використовує {item}", [("a", E, 1), ("item", E, 1)], "інвентар"),
    "place": w("ставить із запасу на поле", "{a} ставить {entity}", [("a", E, 1), ("entity", E, 1)], "інвентар"),
    # cells and field
    "set_cell": w("клітина стає іншою", "{cell} стає {type}", [("cell", "choice:cell", 1), ("type", E, 1)], "клітини й поле"),
    "mark": w("розмітка клітини", "позначити {cell}[: {v}]", [("cell", "choice:cell", 1), ("v", T, 0)], "клітини й поле"),
    "unmark": w("стерти розмітку", "стерти позначку у {cell}", [("cell", "choice:cell", 1)], "клітини й поле"),
    "reveal": w("відкрити клітини", "відкрити {cell}", [("cell", "choice:cell", 1)], "клітини й поле"),
    "hide": w("сховати клітини", "сховати {cell}", [("cell", "choice:cell", 1)], "клітини й поле"),
    "paint": w("зафарбувати", "зафарбувати {cell}[ у {color}]", [("cell", "choice:cell", 1), ("color", T, 0)], "клітини й поле"),
    "fill": w("заливка області", "заливка від {cell}", [("cell", "choice:cell", 1)], "клітини й поле"),
    "clear": w("очистити лінію / групу", "очистити {shape}", [("shape", "choice:shape", 1)], "клітини й поле"),
    "merge": w("злиття двох в одну", "{a} і {b} зливаються в {into}", [("a", E, 1), ("b", E, 1), ("into", E, 1)], "клітини й поле"),
    "explode": w("вибух із формою", "вибух: {shape}[ {n}][, лишає {into}]", [("shape", "choice:shape", 1), ("n", N, 0), ("into", E, 0)], "клітини й поле"),
    # the game itself
    "win": w("перемога 🏆", "перемога 🏆", (), "хід гри"),
    "lose": w("поразка 💀", "поразка 💀", (), "хід гри"),
    "draw": w("нічия", "нічия", (), "хід гри"),
    "next_level": w("наступний рівень", "наступний рівень", (), "хід гри"),
    "restart": w("рестарт рівня", "рестарт рівня", (), "хід гри"),
    "undo": w("скасувати хід (undo)", "скасувати[ {n}] хід", [("n", N, 0)], "хід гри"),
    "game_over": w("кінець гри", "кінець гри", (), "хід гри"),
    "end_turn": w("хід переходить", "хід переходить", (), "хід гри"),
    "pass_turn": w("пас", "пас", (), "хід гри"),
    "extra_move": w("додатковий хід", "додатковий хід", (), "хід гри"),
    "choose": w("гравець обирає", "вибір: {options}", [("options", T, 1)], "хід гри"),
    "window": w("відкрити вікно", "відкривається вікно {window}", [("window", "window", 1)], "хід гри"),
    "message": w("повідомлення", "повідомлення «{text}»", [("text", T, 1)], "хід гри"),
    "sound": w("звук / ефект", "звук «{text}»", [("text", T, 1)], "хід гри"),
    "timer": w("таймер", "таймер: {clock}[ {n}]", [("clock", "choice:clock", 1), ("n", N, 0)], "хід гри"),
    "custom": w("інше (словами)", "{text}", [("text", T, 1)], "інше"),
}

ARGS = {  # the arguments' names in the forms
    "a": "хто", "b": "з ким", "n": "скільки", "every": "N", "p": "%", "dur": "тіків", "cell": "клітина", "dir": "напрям",
    "what": "хто / що", "entity": "хто", "item": "предмет", "into": "на що", "s": "стан", "name": "лічильник", "op": "порівняння",
    "shape": "форма", "where": "де", "text": "словами", "action": "дія", "list": "тіки", "phase": "фаза", "v": "значення",
    "k": "множник", "deg": "кут", "axis": "що", "clock": "дія", "options": "варіанти", "color": "колір", "side": "сторона",
    "type": "тип клітини", "window": "вікно", "prop": "за чим",
}

FIELD = [  # the field's properties, in form order; a choice's options are cards of kind fieldopt with opt `key:value`
    {"key": "topology", "label": "Сітка", "type": "choice"},
    {"key": "view", "label": "Вид", "type": "choice"},
    {"key": "time", "label": "Час", "type": "choice", "multi": True},
    {"key": "control", "label": "Керування", "type": "choice", "multi": True},
    {"key": "gravity", "label": "Гравітація", "type": "choice"},
    {"key": "wrap", "label": "Замкнене поле: вийшов за край — зʼявився з протилежного боку", "type": "bool"},
    {"key": "size", "label": "Розмір за замовчуванням", "type": "text", "hint": "напр. 20×15; різний на рівнях — пиши в рівнях"},
    {"key": "layers", "label": "Шари клітини", "type": "tags",
     "hint": "що може лежати в одній клітині одночасно: підлога · обʼєкт · розмітка · туман"},
]

LEVEL = [  # a level's own properties; the field's ones it may override come after them
    {"key": "mode", "label": "Звідки рівень", "type": "choice", "options": {
        "hand": "зроблений вручну", "file": "з файла", "generated": "згенерований", "endless": "нескінченний"}},
    {"key": "count", "label": "Скільки таких", "type": "text", "hint": "1, 10, «без ліміту»"},
    {"key": "size", "label": "Розмір", "type": "text"},
]

SIDES = {"*": "будь-хто", "@a": "А", "@b": "Б", "@both": "обидва"}  # entity arg values that are not a Part


def vocab() -> dict:
    """The forms' words that live in code — the same source as the validation; the catalog's part is routes/vocab.py."""
    return {"triggers": TRIGGERS, "conditions": CONDITIONS, "effects": EFFECTS, "options": OPTIONS, "sides": SIDES,
            "args": ARGS, "level": LEVEL, "op_not": OP_NOT}


def render(spec: dict, args: dict, name, neg=False, who=None) -> str:
    """Fill the template (`neg` — the negation's): entities through who(arg, value), windows through name(id), choices
    through their labels, `[…]` dropped when empty."""
    who = who or (lambda k, v: SIDES.get(v) or name(v))

    def value(a, flip=False):
        v = args.get(a["name"])
        if v is None or v == "":
            return ""
        if a["type"] == "entity":
            return who(a["name"], v)
        if a["type"] == "window":
            return name(v)
        if a["type"].startswith("choice:"):
            v = OP_NOT.get(str(v), v) if flip else v
            return OPTIONS[a["type"][7:]].get(str(v), str(v))
        return str(v)

    values = {a["name"]: value(a) for a in spec["args"]}
    out = re.sub(r"!([^!{}]+)!", r"\1", spec["neg"] if neg else spec["tpl"])
    for seg in re.findall(r"\[[^\]]*\]", out):
        keys = re.findall(r"\{(\w+)", seg)
        out = out.replace(seg, "" if any(not values.get(k) for k in keys) else seg[1:-1])
    for a in spec["args"]:
        k, v = a["name"], values[a["name"]]
        out = out.replace(f"{{{k}:+}}", ("+" + v) if v and not v.startswith("-") else v)
        out = out.replace(f"{{{k}:!}}", value(a, True)).replace(f"{{{k}}}", v)
    return out.strip()


def sentence(rule, name) -> str:
    """КОЛИ … → ЯКЩО … та … → ТО … the way the site shows it (the bot's alerts use this too). A side of the trigger
    (@a / @b) reads as its entity; its letter stays where the entity alone is ambiguous: «будь-хто» or one entity on both sides."""
    when, cond = rule.when, rule.cond or []
    twin = bool(when.get("a")) and when.get("a") == when.get("b")
    used = {v for it in [*cond, *rule.then] for v in it.values() if v in ("@a", "@b")}
    marked = {s for s in "ab" if f"@{s}" in used and (when.get(s) == "*" or twin)}

    def own(k, v):  # the trigger's side, with the letter ЯКЩО / ТО call it by
        text = SIDES.get(v) or name(v)
        return f"{text} ({SIDES['@' + k]})" if k in marked else text

    def side(k, v):
        target = when.get(v[1:]) if v in ("@a", "@b") else None
        if not target or target in SIDES:
            return SIDES.get(v) or name(v)
        return f"{name(target)} ({SIDES[v]})" if twin else name(target)

    def part(dic, item, who):
        spec = dic.get(item.get("kind"))
        neg = bool(item.get("not") and spec and spec.get("neg"))
        text = render(spec, item, name, neg, who) if spec else item.get("kind", "?")
        return ("не " if item.get("not") and not neg else "") + text

    out = "КОЛИ " + part(TRIGGERS, when, own)
    if cond:
        out += " → ЯКЩО " + " та ".join(part(CONDITIONS, c, side) for c in cond)
    return out + " → ТО " + " · ".join(part(EFFECTS, e, side) for e in rule.then)
