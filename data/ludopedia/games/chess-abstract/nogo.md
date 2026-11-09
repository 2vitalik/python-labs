---
title: NoGo (Анти-го)
slug: nogo
aka: [No-Go, Anti-Go, Анти-го]
family: chess-abstract
also: []
klass: figure
axes:
  field: square
  time: turn
  opponent: hotseat
  info: full
  random: none
  goal: state
year: 2005
platforms: [board, PC]
links:
  - {kind: other, url: "https://ludii.games/details.php?keyword=NoGo", best: true, note: "Ludii: повні правила, автор John Moore (II), 04.2005, дошки 9×9 і 6×7, грати з AI"}
  - {kind: other, url: "https://ludii.games/lud/games/NoGo.lud", note: "Ludii .lud: HasFreedom + NoCapture як умова ходу, NoMoves → Loss"}
  - {kind: other, url: "https://www.game-ai-forum.org/icga-tournaments/game.php?id=47", note: "ICGA: NoGo на Computer Olympiad 2011 (BobNoGo) і 2013; походження — BIRS 2011, PSPACE"}
  - {kind: other, url: "https://webdocs.cs.ualberta.ca/~mmueller/ps/2023/ACG_2023_NoGo.pdf", note: "стаття ACG 2023 про розвʼязок малих дошок (з пошуку, не відкривав)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=NoGo+board+game", note: "пошук"}
stage: v1
coverage: 75
mechanics: [cursor-place, no-moves-left, hot-seat, turn-enforcement, ai-opponent, ai-minimax, level-solver, connectivity-check, cell-click, hover-highlight, legal-move-highlight, last-move-highlight, field-size-picker, game-screen, main-menu, end-screen, help-window, undo-step, state-as-data, unit-tests, +place-stone, +last-move-wins, +liberty-capture, +suicide-rule, +all-groups-breathe, +mcts-ai]
proposes: ["+cond:liberties", "+cond:group", "+card:all-groups-breathe", "+card:mcts-ai"]
author: opus
date: 2026-11-09
---

# NoGo — го навпаки: не можна ні взяти, ні самогубитись; хто не має куди поставити, програв

## Суть
Двоє по черзі ставлять камені на перетини, як у [го](go.md), але хід легальний, лише якщо **після нього кожна група на дошці — своя й чужа — має хоча б одне дихання**. Отже, взяти ворожу групу заборонено так само, як поставити свій камінь без дихань. Каменів не знімають, циклів і підрахунку нема: хто на своєму ході не має легального пункту — програв (останній хід виграє). Гра запозичує з го лише поняття «група» і «дихання», а тактично з ним не повʼязана.

## Поле і час
- Порожня квадратна або прямокутна сітка перетинів, 4-сусідство; Ludii — 9×9 (за замовчуванням) і 6×7; більше 9×9 не радять.
- BIRS 2011: людський турнір на 7×6, компʼютерний — на 9×9.
- Чорні першими, далі по черзі; хід = поставити камінь; пасу нема.
- Партія не довша за кількість пунктів дошки: кожен пункт займається не більше разу.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Камінь чорний / білий | piece | колір | ставиться на порожній перетин, не рухається і не знімається |
| Група | zone | звʼязні (4-сусідство) камені одного кольору | мусить мати ≥ 1 дихання після кожного ходу |
| Дихання | mark | порожній сусід групи | останнє дихання будь-якої групи заборонено займати |
| Пункт-«око» | zone | порожній пункт, оточений одним кольором | легальний лише для власника (суперник там самогубився б або взяв) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(place, cell)` → ЯКЩО `turn_of(side)` і `free(cell)` і `custom: «після постановки кожна група на дошці має ≥ 1 дихання»` (`+cond:liberties`) → ТО `place(side, stone)`, `end_turn`.
- КОЛИ `input(place, cell)` → ЯКЩО `custom: «нова група без дихань»` (самогубство) → ТО `block`.
- КОЛИ `input(place, cell)` → ЯКЩО `custom: «камінь забирає останнє дихання ворожої групи»` (взяття) → ТО `block`.
- КОЛИ `turn_start(side)` → ЯКЩО `no_moves(side)` → ТО `lose`.
- Взяття, ко, нічиїх і підрахунку нема; `pass_turn` не існує.
- Перемога: суперник без легального ходу (= ти зробив останній хід) · Поразка: без ходу · Рахунок: 1 / 0.

## Керування і ввід
- (цифрова версія) клік по перетину → камінь; `hover-highlight` — привид каменя; нелегальні пункти можна затіняти (`legal-move-highlight`), щоб гравець бачив, скільки ходів лишилось.
- Hotseat, проти AI (Ludii) або програма проти програми (GTP-рушії олімпіади (?)).

## Вікна, меню, HUD
- (цифрова версія)
- `main-menu`: проти людини / проти AI → `match-setup` (розмір дошки 9×9 / 6×7 / інший, колір).
- `game-screen`: сітка, `turn-indicator`, `last-move-highlight`, лічильник легальних ходів обох сторін (`moves-left-per-side`, див. domineering), затінені нелегальні пункти.
- `end-screen`: «Білі не мають ходу — чорні виграли», «Ще партію».
- `help-window`: одне правило з прикладами «взяття заборонено» / «самогубство заборонено».

## Фічі поза полем
- `ai-opponent-levels` (Ludii AI, MCTS-програми), `hotseat`, `custom-difficulty` (розмір дошки), `undo` у навчальній партії.
- Дослідницький бік: комп'ютерні олімпіади ICGA (Тілбург 2011 — BobNoGo на базі Fuego; Йокогама 2013 — HappyNoGo (?)), розвʼязування малих дошок.

## Варіації й родичі
- Батько за поняттями — [go.md](go.md); протилежність — [atari-go.md](atari-go.md) (там перше взяття виграє, тут будь-яке взяття заборонене).
- Інші «поставив — і місць меншає» з нормальною умовою «останній хід виграє»: [domineering.md](domineering.md), Clobber, Cavity, Gopher, Mig Mang (схожі ігри за Ludii).
- **Осі варіацій**: розмір і форма дошки (9×9 / 6×7 / 7×6 / 3×N для розвʼязків) · хто програє без ходу (нормальна гра / misère (?)) · сусідство (4 / гекс (?)).

## Цікавинки для курсу
- Генератор легальних ходів: flood fill груп і дихань після пробної постановки, перевірка всіх сусідніх груп — 🥉.
- Інкрементальні дихання (union-find груп, лічильники) замість повного перерахунку — 🥈.
- AI: MCTS з випадковими доігровками (BobNoGo — патч до рушія го Fuego) — 🥇.
- Розвʼязувач малих дошок (3×3 … 3×N) з таблицею транспозицій і симетріями — 🥇; аналіз сум регіонів (теорія комбінаторних ігор) — 👑.
- HUD «скільки легальних ходів у кожного» як підказка, хто виграє ендшпіль — 📎.

## Мапа на каталог
- Є: `cursor-place` ↔ камінь на вільний пункт · `no-moves-left` ↔ без ходу — поразка · `hot-seat`, `turn-enforcement` · `ai-opponent`, `ai-minimax`, `level-solver` · `connectivity-check` ↔ групи через BFS · `cell-click`, `hover-highlight`, `legal-move-highlight`, `last-move-highlight` · `field-size-picker` · `game-screen`, `main-menu`, `end-screen`, `help-window` · `undo-step`, `state-as-data`, `unit-tests`.
- **Нема** → пропозиції карток:
  - `+place-stone`, `+last-move-wins` (див. domineering.md); `+liberty-capture`, `+suicide-rule` (див. go.md) — тут обидва перевернуті в заборону.
  - `+all-groups-breathe` «Хід легальний, лише якщо всі групи мають дихання» · entities/legality · 🥉 · слоти {neighborhood: 4|6}.
  - `+mcts-ai` «AI пошуком Монте-Карло по дереву» · game-logic/opponent · 🥇 · слоти {playouts}.

## Пропозиції до словників
- `+cond:liberties` — голос (go.md, atari-go.md): кількість дихань групи порівняно з N.
- `+cond:group` — голос (go.md): сутність належить звʼязній групі одного кольору.
- `+card:all-groups-breathe`, `+card:mcts-ai` — див. «Мапа на каталог».

## Джерела
- ⭐ [Ludii: NoGo](https://ludii.games/details.php?keyword=NoGo) — правила («після кожного ходу всі групи мають дихання; хто не може піти — програв»), автор John Moore (II), 04.2005, дошки, 6×7 у людських матчах, схожі ігри.
- [Ludii: NoGo.lud](https://ludii.games/lud/games/NoGo.lud) — опції 6×7 / 9×9, умова ходу `HasFreedom` + `NoCapture`, кінець `NoMoves Loss`.
- [ICGA: NoGo](https://www.game-ai-forum.org/icga-tournaments/game.php?id=47) — правила «хто самогубився або вбив групу — програв», походження з BIRS 2011, PSPACE, олімпіади 2011 і 2013.
- Результати пошуку (не відкривав): сторінки Мартіна Мюллера про BobNoGo і стаття ACG 2023 — турніри BIRS 7×6 / 9×9, перемога першого на 3×3, найбільша розвʼязана дошка 3×9.
- YouTube — пошук.

## Непевне
- (?) Автор і рік: Ludii — John Moore (II), 2005; ICGA-сторінка — «вигадали організатори BIRS 2011». Можливо, BIRS лише популяризував гру.
- (?) Розміри BIRS (7×6 люди, 9×9 програми), переможець 2013 (HappyNoGo) і розвʼязки 3×3 / 3×9 — з анотацій пошуку, сторінки не відкривались (404 / не відкривав).
- (?) Варіанти misère і на гекс-сітці — не бачив у джерелах, лише як можливі осі.
- (?) Протокол програм олімпіади (GTP) — з памʼяті.
