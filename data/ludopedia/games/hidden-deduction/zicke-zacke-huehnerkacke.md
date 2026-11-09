---
title: Zicke Zacke Hühnerkacke
slug: zicke-zacke-huehnerkacke
aka: [Chicken Cha Cha Cha, Pique Plume, Cocorico Cocoricó, Jakkiebak! Kippenkak!, Kanaset, Csupa Csupasz Tyúkeszű]
family: hidden-deduction
also: [board-digital]
klass: hybrid
axes:
  field: 1d
  time: turn
  opponent: hotseat
  info: hidden
  random: setup
  goal: collect
year: 1998
platforms: [board (Zoch Verlag; Rio Grande Games, Gigamic, Devir, 999 Games та ін.)]
links:
  - {kind: wiki, url: "https://de.wikipedia.org/wiki/Zicke_Zacke_H%C3%BChnerkacke", best: true, note: "компоненти, хід, обгін і пера, кінець гри, нагороди, міжнародні назви, розширення Entenkacke"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Chicken_Cha_Cha_Cha", note: "EN-правила: 24 яйця × 12 малюнків, 12 восьмикутників, обгін, автор, Rio Grande"}
  - {kind: other, url: "https://rulespal.com/chicken-cha-cha-cha/rulebook", note: "правила Rio Grande: 4 курки, 4 пера, по 5 порожніх яєць між курками, ланцюжок обгону"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Zicke+Zacke+H%C3%BChnerkacke+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [cell-click, hot-seat, turn-enforcement, collect-all, goal-counter, game-screen, main-menu, end-screen, +ring-board, +flip-to-match-target, +extra-turn-on-success, +overtake-steal, +flip-back-after-use]
proposes: ["+card:flip-to-match-target", "+card:overtake-steal", "+card:flip-back-after-use", "+ui:feather-count", "+ui:target-tile-highlight"]
author: opus
date: 2026-11-09
---

# Zicke Zacke Hühnerkacke — курячі перегони по кільцю з яєць: памʼять на прихованих плитках керує кожним кроком

## Суть
Дитяча настілка Клауса Цоха: кури біжать по кільцю з 24 відкритих плиток-яєць, а в центрі долілиць лежать 12 восьмикутних плиток з тими самими малюнками. Хід = відкрити один восьмикутник: якщо малюнок збігся з яйцем **попереду своєї курки** — курка стає на нього і гравець ходить далі; ні — хід закінчується. Курка, що наздогнала іншу й перестрибнула її, забирає всі її хвостові пера; виграє той, хто зібрав пера всіх. Клас — гібрид: «рука» (`cursor`) відкриває плитки, а курка (`avatar`) рухається сама за результатом.

## Поле і час
- Кільце з 24 плиток-яєць, відкритих: 12 малюнків × 2 (кури, кролики, їжаки, квіти та ін.); порядок випадковий після перемішування.
- Центр: 12 восьмикутників долілиць, кожен малюнок рівно раз — «колода памʼяті», що лишається на своїх місцях.
- Кури стоять на яйцях рівномірно: з 4 курками між ними по 5 порожніх яєць.
- Хід — серія відкриттів, доки гравець не схибить; часу нема. Кільце замкнене — вперед завжди за годинниковою стрілкою.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Курка | player | колір, пера в хвості | стоїть на яйці; іде на 1 яйце вперед після вдалого відкриття |
| Хвостове перо | pickup | колір власника | переходить до курки, що перестрибнула власника |
| Плитка-яйце | terrain | малюнок (відкритий) | клітина кільця; її малюнок — «ціль» для курки позаду |
| Восьмикутник | tile | малюнок (прихований) | відкривається на хід, потім знову долілиць на те саме місце |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `game_start` → ТО `custom: «перемішати 24 яйця й викласти кільцем відкритими, 12 восьмикутників — долілиць у центрі»`, `place(chicken, egg)` рівномірно, по перу в кожну курку.
- КОЛИ `input(flip, octagon)` → ЯКЩО `same(octagon, egg_ahead, picture)` і `free(egg_ahead)` → ТО `reveal(octagon)`, `move(chicken, egg_ahead)`, `hide(octagon)`, `extra_move`.
- КОЛИ `input(flip, octagon)` → ЯКЩО не `same(octagon, egg_ahead, picture)` → ТО `reveal(octagon)` (усі бачать), `hide(octagon)`, `end_turn`; курка лишається на місці, штрафу нема.
- Обгін: КОЛИ `input(flip, octagon)` → ЯКЩО `occupied(egg_ahead, chicken)` і `same(octagon, first_free_egg_beyond, picture)` → ТО `move(chicken, first_free_egg_beyond)` (стрибок), `take(other_chicken, all_feathers)`, `give(chicken, all_feathers)`, `extra_move`.
- КОЛИ обгін → ЯКЩО `custom: «попереду кілька курок підряд без проміжку»` → ТО один стрибок через усіх, пера всіх перестрибнутих — стрибуну.
- КОЛИ обгін не вдався (`not same`) → ТО `end_turn` без штрафу.
- КОЛИ `counter(feathers_of(chicken), ==, total_feathers)` → ТО `win`.
- Перемога: зібрати всі хвостові пера · Поразка: нема (інші просто не встигли) · Рахунок: нема.

## Керування і ввід
- Настолка: гравець торкається одного восьмикутника, перевертає, показує всім; при збігу ставить курку на наступне яйце й відкриває далі.
- Ходи — за годинниковою стрілкою, першим ходить наймолодший.
- Цифрова версія: клік по восьмикутнику; ціль (яйце попереду) підсвічена; курка й пера анімуються.

## Вікна, меню, HUD
- `main-menu` (цифрова версія): кількість гравців (2–4), колір курки, Грати.
- `game-screen` (цифрова версія): кільце яєць, центр із 12 восьмикутниками, `turn-indicator`, підсвічене яйце-ціль, `feather-count` біля кожної курки.
- `end-screen` (цифрова версія): хто зібрав усі пера.
- Переходи: main-menu → game-screen → end-screen → main-menu.

## Фічі поза полем
- `hotseat` 2–4 гравці; вік від 4 років, партія 20–30 хв.
- Розширення Zicke Zacke Entenkacke — до 6 гравців (правила не читав).

## Варіації й родичі
- [Memory / Concentration](memory-concentration.md) — те саме «відкрий і запамʼятай», але ціль — пара; тут ціль задає поле (яйце попереду), а успіх = крок.
- [Memoarrr!](memoarrr.md) — ціль задає попередня відкрита карта (спільна тварина або пейзаж), провал вибиває з раунду.
- [Das magische Labyrinth](das-magische-labyrinth.md), [Geistertreppe](geistertreppe.md) — інші дитячі «памʼять + перегони» з прихованим полем.
- **Осі варіацій**: звідки ціль «яйце попереду (Zicke Zacke) / попередня карта (Memoarrr!) / пара (Memory)»; що дає успіх «крок / пара / виживання в раунді»; промах «кінець ходу / виліт з раунду»; взаємодія «стрибок і крадіжка пер / нема».

## Цікавинки для курсу
- Кільцевий трек з індексом `(i + 1) % 24` і пошуком першого вільного яйця за чергою курок — 🌱.
- Серія ходів до першого промаху (`extra_move`) з машиною станів «відкрито → перевірка → крок / кінець» — 🌱.
- Обгін із ланцюжком курок і передачею всіх пер — 📎 (кілька випадків: одна курка, ланцюжок, кінець кільця).
- AI з обмеженою памʼяттю: памʼятає побачені восьмикутники з імовірністю p — 📎.
- Порахувати симуляцією середню довжину серії для ідеальної і «забудькуватої» памʼяті — 🥉.

## Мапа на каталог
- Є: `cell-click` ↔ відкрити восьмикутник; `hot-seat` + `turn-enforcement` ↔ черга гравців; `collect-all` + `goal-counter` ↔ зібрати всі пера; `game-screen` / `main-menu` / `end-screen` (цифрова версія).
- **Нема** → пропозиції карток:
  - `+ring-board` «Кільцевий трек» (уже пропонована) — тут кільце з 24 клітин.
  - `+flip-to-match-target` «Відкрий приховане, щоб збігтися з ціллю на полі» · entities/interact · 🌱.
  - `+extra-turn-on-success` (Memory) — серія відкриттів до промаху.
  - `+overtake-steal` «Наздогнав і перестрибнув — забрав трофеї суперника» · game-logic/score · 📎.
  - `+flip-back-after-use` «Відкрита плитка повертається долілиць на своє місце» · entities/state · 🌱.

## Пропозиції до словників
- `+ui:feather-count` — скільки пер у кожної курки (трофеї, що переходять між гравцями).
- `+ui:target-tile-highlight` — підсвітка клітини-цілі, з якою треба збігтися.
- Вжито наявні: `same`, `occupied`, `free`, `extra_move`, `take`, `give`, `place`, `reveal`, `hide`.

## Джерела
- ⭐ [Wikipedia DE: Zicke Zacke Hühnerkacke](https://de.wikipedia.org/wiki/Zicke_Zacke_H%C3%BChnerkacke) — 24 яйця, 12 восьмикутників, хід, обгін, кінець, нагороди (Sonderpreis Kinderspiel 1998, Deutscher Kinderspielepreis), назви в інших країнах, Entenkacke.
- [Wikipedia EN: Chicken Cha Cha Cha](https://en.wikipedia.org/wiki/Chicken_Cha_Cha_Cha) — ті самі правила англійською, Klaus Zoch, Doris Matthäus, Rio Grande Games.
- [RulesPal: Chicken Cha Cha Cha](https://rulespal.com/chicken-cha-cha-cha/rulebook) — склад коробки (4 курки, 4 пера), розстановка «5 порожніх між курками», повернення восьмикутника долілиць, обгін кількох курок.
- YouTube: пошук «Zicke Zacke Hühnerkacke gameplay».

## Непевне
- (?) Чи відкриті за хід восьмикутники лежать догори до кінця ходу (EN-вікі: «потім усі перевертаються») чи кожен одразу повертається долілиць (RulesPal) — у правилах вище взято RulesPal.
- (?) Скільки пер у грі з 2–3 гравцями й чи стоять «зайві» курки на полі — RulesPal правила для двох не наводить.
- (?) Чи перестрибнута курка теж може відразу відвоювати пера, і чи курка без пер лишається в грі — з джерел не видно.
- (?) Рік: DE-вікі — 1998, EN-вікі в категорії «1997»; цифрових версій не знайшов — вікна описано як «(цифрова версія)».
