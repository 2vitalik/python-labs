---
title: The Observer's Paradox
slug: the-observers-paradox
aka: [The observant paradox]
family: thinky
also: [push-slide]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: hidden
  random: none
  goal: state
year: 2024
platforms: [web]
links:
  - {kind: play, url: "https://www.puzzlescript.net/play.html?p=42a7e74f578b9d0bdc9c66469d97b262", best: true, note: "грати в браузері; 5 рівнів + бонус, 10 хвилин"}
  - {kind: other, url: "https://gist.github.com/sevansevan/42a7e74f578b9d0bdc9c66469d97b262", note: "вихідний код PuzzleScript: туман, зір, правило повернення ящика в гніздо"}
  - {kind: itch, url: "https://sevansevan.itch.io/the-observers-paradox", note: "сторінка гри: «This game is not about quantum physics»"}
  - {kind: itch, url: "https://sevansevan.itch.io/", note: "інші PuzzleScript-ігри автора (Purrradox, Them, The ballet)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=The+Observer%27s+Paradox+puzzlescript", note: "пошук; геймплей"}
stage: v1
coverage: 85
mechanics: [move-4dir, move-by-input, keyboard-controls, push-object, impassable-cells, all-on-targets, fog-of-war, undo-unlimited, restart-level, sequential-levels, +unobserved-reset, +vision-radius, +color-matched-targets, +nest-blocking]
proposes: ["+cond:observed", "+effect:return_home", "+card:unobserved-reset", "+card:nest-blocking"]
author: opus
date: 2026-11-09
---

# The Observer's Paradox — Sokoban у тумані, де ящик, на який ніхто не дивиться, повертається на своє місце

## Суть
Маленька PuzzleScript-гра Sevan: класичний Sokoban (штовхнути ящики кольорів на цілі того самого кольору), але герой бачить лише клітини поруч, а решта поля чорна. «Квантове» правило: ящик, що опинився поза полем зору, наприкінці ходу стрибає назад у своє гніздо (стартову клітину), якщо гніздо теж не видно й воно вільне. Головоломка — провести ящик до цілі, не випустивши його з очей, або «зафіксувати» гніздо: дивитись на нього чи заблокувати іншим ящиком.

## Поле і час
- Квадратна сітка; рівні 11–14 клітин завширшки й 8–16 заввишки разом із товстою рамкою стін (з коду), один екран.
- Покроково: хід = крок героя; правила зору й повернення виконуються в `late`-фазі після руху.
- Видимість: клітина героя + 8 сусідів (3×3) + ортогональні сусіди цього квадрата — ромб 5×5 без 4 кутів (21 клітина). Стіни зір **не** блокують. Усе інше — суцільний чорний туман, навіть стіни й цілі.
- Каміння-декор на підлозі розкидане випадково при старті рівня — лише графіка (`random: none` для механіки).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой | player | — | рух 4 напрямки; штовхає один ящик; центр зору |
| Червоний ящик (Crate1) | object | колір red | штовхається на 1, якщо за ним вільно; поза зором повертається в червоне гніздо |
| Синій ящик (Crate2) | object | колір blue | те саме для синього гнізда |
| Гніздо S1 / S2 | zone | колір; стоїть під ящиком на старті | точка повернення ящика свого кольору; зайняте будь-яким ящиком — не приймає |
| Ціль A / B | zone | колір | перемога, коли на кожній цілі ящик її кольору |
| Стіна | static | — | непрохідна для героя й ящиків; зір пропускає |
| Туман | zone | — | накриває все поза ромбом зору; оновлюється кожен хід |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next_cell)` → ТО `move(player, dir)`.
- КОЛИ `contact(player, crate)` → ЯКЩО `free(cell_behind)` → ТО `push`, `move(player, dir)`; інакше `block` (ланцюга ящиків нема: ящик, стіна й герой — один шар колізій).
- КОЛИ `turn_end(player)` → ТО `hide(all_cells)`, `reveal(custom: «ромб 5×5 без кутів навколо героя»)`.
- КОЛИ `turn_end(player)` → ЯКЩО `custom: «червоний ящик під туманом»` and `custom: «червоне гніздо під туманом»` and `not occupied(nest1, crate)` → ТО `teleport(crate1, nest1)`, `sound(sfx1)`.
- Те саме для синього ящика й синього гнізда (правило йде після червоного).
- Наслідки: видимий ящик або видиме гніздо не дає повернення; ящик іншого кольору на гнізді блокує повернення назавжди, доки стоїть там.
- КОЛИ `all_on(crate1, target1)` and `all_on(crate2, target2)` (після `late`-фази) → ТО `win`, `next_level`.
- КОЛИ `input(Z)` → ТО `undo(1)`; КОЛИ `input(R)` → ТО `restart`.
- Перемога: усі цілі під ящиками свого кольору · Поразки нема (глухий кут — undo/restart) · Рахунку нема.

## Керування і ввід
- Стрілки або WASD — крок; Z — undo; R — рестарт; Esc — меню (стандарт PuzzleScript).
- Дії X нема; мишею не керується.

## Вікна, меню, HUD
- `main-menu` (титул PuzzleScript): назва, автор, «start game» / «continue».
- `game-screen`: поле в тумані; HUD нема.
- `custom-window` — текстові повідомлення між рівнями («It is said that quantum objects are only defined when observed»…).
- `end-screen`: «Thank you for playing!» → бонусний рівень → «Congratulations, you're the true quantum master!».
- Переходи: титул → рівень 1 → … → повідомлення → рівень 5 → подяка → бонус → фінальне повідомлення.

## Фічі поза полем
- `levels-sequential`: 5 рівнів + бонус; `undo` ∞; `restart-level`; автозбереження поточного рівня (стандарт PuzzleScript, «continue»).
- Нема редактора, підказок, налаштувань.

## Варіації й родичі
- Sokoban (база), DROD та роглайки (туман як обмеження), Loophole (`paradox-sighting` — «тебе не повинні побачити»), Patrick's Parabox / Baba Is You (одне незвичне правило, що перевертає класику).
- Автор пише в коді про ускладнену альтернативу 4-го рівня («harder alt», закоментована).
- Осі варіацій:
  - **що робить ненаблюдуваний обʼєкт**: нічого (Sokoban) / повертається на старт (тут) / зникає / стрибає у випадкове вільне гніздо;
  - **форма зору**: ромб без урахування стін (тут) / промені з блокуванням стінами / конус за напрямком погляду;
  - **що «фіксує» обʼєкт**: погляд героя / погляд на гніздо / зайняте гніздо.

## Цікавинки для курсу
- Туман з ромбом зору й повним перерахунком щоходу — 📎 (маска клітин, без стін).
- «Квантове» повернення: перевірка «ящик і гніздо обидва поза зором, гніздо вільне» → телепорт — 📎.
- Блокування чужого гнізда ящиком іншого кольору як стратегія — 🌱 (дизайн, код — та сама умова `occupied`).
- Розвʼязувач BFS по станах із врахуванням повернень (стан = позиція героя + ящики; повернення — частина переходу) — 🥈.
- Порядок фаз: рух → зір → повернення → перевірка перемоги; помилка в порядку дає інші розвʼязки — 🌱 (вправа на конвеєр правил).

## Мапа на каталог
- Є: `move-4dir` · `move-by-input` · `keyboard-controls` ↔ крок; `push-object` ↔ ящик; `impassable-cells` ↔ стіни; `all-on-targets` ↔ перемога; `fog-of-war` ↔ туман; `undo-unlimited` · `restart-level` ↔ Z/R; `sequential-levels` ↔ 5 + бонус.
- **Нема** → пропозиції карток:
  - `+unobserved-reset` «Ненаблюдуваний обʼєкт повертається на старт» · entities/interact · 📎 · слоти {who_observes: player, needs_home_unseen: bool}.
  - `+vision-radius` (уже в корпусі, Mutant Year Zero) — тут ромб радіуса 2 без стін.
  - `+color-matched-targets` «Ціль приймає лише ящик свого кольору» · game-logic/win · 🌱.
  - `+nest-blocking` «Зайняте гніздо не приймає повернення» · entities/legality · 🌱.

## Пропозиції до словників
- `+cond:observed` — сутність або клітина в полі зору героя (тут через `custom` «під туманом»).
- `+effect:return_home` — сутність повертається у свою стартову клітину (тут — `teleport` у гніздо).
- `+card:unobserved-reset`, `+card:nest-blocking` — див. вище.
- ⏳-слова, вжиті тут: `input`, `turn_end`, `free`, `occupied`, `move`, `hide`, `reveal`, `teleport`, `all_on`, `undo`, `restart`, `next_level`, `sound`.

## Джерела
- ⭐ [PuzzleScript: грати](https://www.puzzlescript.net/play.html?p=42a7e74f578b9d0bdc9c66469d97b262) — сама гра; повний код відкривається через «hack».
- [Gist з кодом](https://gist.github.com/sevansevan/42a7e74f578b9d0bdc9c66469d97b262) — OBJECTS, COLLISIONLAYERS, RULES (зір, туман, повернення), WINCONDITIONS, 6 рівнів і тексти повідомлень; прочитано через `api.github.com/gists/<id>`.
- [itch: The Observer's Paradox](https://sevansevan.itch.io/the-observers-paradox) — сторінка гри (у списку ігор автора).
- [itch: SevanSevan](https://sevansevan.itch.io/) — інші ігри автора.

## Непевне
- (?) Якщо гнізд одного кольору кілька, PuzzleScript вибере перше знайдене вільне гніздо в порядку сканування; у всіх рівнях гри гніздо одне на колір, тож перевірити не було на чому.
- (?) Опис у gist називає гру «The observant paradox», у коді й на itch — «The Observer's Paradox»; рік — 2024 за датою gist (1 жовтня 2024).
