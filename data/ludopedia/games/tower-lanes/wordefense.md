---
title: worDefense
slug: wordefense
aka: [Word Defense]
family: tower-lanes
also: [word-number]
klass: cursor
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: runtime
  goal: score
year: 2023
platforms: [web]
links:
  - {kind: itch, url: "https://amidos2006.itch.io/wordefense", best: true, note: "грати в браузері; опис режимів Normal/Hardcore, вмінь і 10 ворогів"}
  - {kind: other, url: "https://amidos2006.itch.io/wordefense/devlog/652459/hardcore-mode-is-now-out", note: "девлог 18.12.2023: Hardcore — вороги наступають самі, як у NecroDancer"}
  - {kind: other, url: "https://html-classic.itch.zone/html/9339140/index.html", note: "HTML5-збірка: з її out.js і assets/data/*.json|txt узято правила (поле 5×6, здоровʼя, рівні)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=worDefense+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 75
mechanics: [word-validation, shoot-forward, hp-damage, enemy-reached-base, spawn-schedule, progress-acceleration, chain-reaction, event-points, score-records, leaderboard, move-timer, mode-select, end-screen, keyboard-controls, cell-click, music-toggle, +lane-grid, +word-as-attack, +split-on-death, +cooldown-ability, +letter-swap, +use-all-letters-bonus, +directional-armor, +vulnerability-toggle, +do-not-shoot, +partial-heal-pips, +step-blocking-advance]
proposes: ["+trigger:word_submitted", "+trigger:enemy_moved", "+effect:shoot", "+effect:toggle_state", "+cond:hit_from", "+ui:letter-orbs", "+ui:word-line", "+ui:charge-ring", "+ui:heart-pips", "+card:word-as-attack", "+card:directional-armor"]
author: opus
date: 2026-11-09
---

# worDefense — склади слово з пʼяти літер-гармат: кожна літера стріляє вгору своєю колонкою, потім вороги роблять крок

## Суть
Покрокова суміш tower defense і словесної гри від Ahmed Khalifa (Amidos2006). Унизу поля 5 «сфер-літер», по одній на колонку; гравець складає з них англійське слово, і кожна літера слова по черзі пускає вогняну кулю вгору **своєю колонкою**. Після залпу вороги наступають на 1–3 клітини, зверху зʼявляється новий ряд, літери оновлюються. Очки — лише за вбитих ворогів, не за довжину слова, тож вибір слова — це вибір колонок і кількості пострілів у кожну.

## Поле і час
- Поле 5 колонок × 6 рядів; під полем — ряд із 5 літер (позиція літери = колонка, з якої вона стріляє). Вороги заходять згори, і хто вийшов за нижній край, той «атакує» гравця.
- Normal: час стоїть, доки не вистрілиш слово (хід = слово). Hardcore: таймер ряду (15 → 4 с за рівнем); вичерпався — вороги кроком уперед і новий ряд без твого пострілу.
- Кулі летять по черзі: наступна стартує, коли попередня влучила або вилетіла за край.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Сфера-літера | player | літера, колонка 0–4 | клік додає літеру в слово; при пострілі пускає кулю вгору своєю колонкою |
| Вогняна куля | projectile | шкода 1 (2 з Double), напрям | летить по прямій, бʼє першого вразливого ворога, зникає |
| Гравець (здоровʼя) | player | 6 половинок серця (3 серця), 5 «крихт» лікування | −N за ворога знизу; 5 крихт = +½ серця; удар обнуляє крихти |
| Курча | neutral | крок 3 | влучив — −1 здоровʼя тобі; дійшло донизу — крихта лікування й +1 очко |
| Малий слиз | enemy | крок 1, шкода 1 | базовий ворог: 1 влучання |
| Слиз | enemy | крок 1 | від влучання ділиться на двох малих (вліво/вправо, якщо вільно) |
| Краб | enemy | HP 2 | два влучання або одне подвоєне |
| Гоблін 1/2/3 | enemy | число = шкода | 1 влучання; знизу бʼє на своє число |
| Дракон | enemy | — | крок по діагоналі (випадково вліво/вправо, якщо вільно), інакше прямо |
| Рослина голодна / сита | enemy | крок 2 | не гине: влучання перемикає стан; голодна знизу бʼє, сита — лікує й дає очко |
| Око | enemy | стан вразливе/невразливе | щокроку перемикає стан; невразливе кулі прошивають наскрізь |
| Вогняний елементаль | enemy | крок 2 | від влучання гине й пускає 4 кулі: вліво, вправо, вгору, вниз |
| Скелет | enemy | HP 4 | лобові кулі знизу бʼють по HP; куля збоку чи згори вбиває одразу |
| Яблуко | pickup | — | у коді: влучання дає крихту лікування, зникає за крок (у рівнях не бачив) |
| Swap | — | заряд 0–1, +0.2 за слово | міняє місцями дві літери (колонки) |
| Double | — | заряд 0–1, +0.2 за слово | обрана літера цього ходу бʼє на 2 |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(click | key, orb)` → ЯКЩО `custom: «довжина слова < 12»` → ТО `custom: «літера додається в кінець слова»` (літеру можна брати повторно).
- КОЛИ `input(backspace)` → ТО `custom: «стерти останню літеру»`.
- КОЛИ `input(fire | enter)` → ЯКЩО `in_dictionary(word)` and `custom: «довжина > 1 і ≥ 2 різні літери»` → ТО `custom: «залп»`; інакше `block` (кнопки Fire не видно).
- КОЛИ `custom: «залп»` → ЯКЩО `custom: «слово містить усі 5 літер»` → ТО `spawn_at(fireball, every_column)` («!!! SPECIAL ATTACK !!!»), далі звичайний залп.
- КОЛИ `custom: «залп: чергова літера слова»` → ЯКЩО `count(fireball, ==, 0)` → ТО `spawn_at(fireball, column_of_letter)` з напрямом угору.
- КОЛИ `contact(fireball, enemy)` → ЯКЩО `not state(enemy, invulnerable)` → ТО `damage(enemy, dmg)`, `disappear(fireball)`.
- КОЛИ `edge(fireball)` → ТО `disappear(fireball)`.
- КОЛИ `hp_zero(enemy)` → ТО `disappear(enemy)`, `score(+1)`.
- КОЛИ `contact(fireball, chicken)` → ТО `lives(-1)`, `disappear_both`.
- КОЛИ `contact(fireball, plant)` → ТО `custom: «перемкнути голодна ↔ сита»`, `disappear(fireball)`.
- КОЛИ `contact(fireball, slime)` → ЯКЩО `free(left)` / `free(right)` → ТО `spawn_at(baby_slime, left | right)`; зайнято або край — один малий на місці; слиз гине.
- КОЛИ `contact(fireball, elemental)` → ТО `spawn_at(fireball, 4 directions)`, `disappear(elemental)`, `score(+1)`.
- КОЛИ `contact(fireball, skeleton)` → ЯКЩО `moving(fireball, up)` → ТО `damage(skeleton, dmg)`; інакше `disappear(skeleton)`, `score(+1)`.
- КОЛИ `custom: «залп завершено»` → ТО `custom: «вороги наступають, найближчі до низу першими»`, `custom: «нові 5 літер»`, `spawn_at(enemy_row, top)`.
- КОЛИ `custom: «ворог наступає на k»` → ЯКЩО `occupied(cell_ahead, enemy)` → ТО `custom: «крок коротшає до вільної клітини»`; інакше `move(enemy, down k)`.
- КОЛИ `custom: «наступ ока»` → ТО `custom: «вразливе ↔ невразливе»`.
- КОЛИ `custom: «наступ дракона»` → ЯКЩО `free(diagonal)` → ТО `move(dragon, diagonal)`; інакше `move(dragon, down)`.
- КОЛИ `reach(enemy, bottom)` → ТО `lives(-damage)`, `disappear(enemy)`; курча / сита рослина — `custom: «крихта лікування»`, `score(+1)`.
- КОЛИ `counter(heal_pips, ==, 5)` → ТО `lives(+1)`, `counter(heal_pips, =0)`.
- КОЛИ `custom: «гравця вдарено»` → ТО `counter(heal_pips, =0)`.
- КОЛИ `input(swap, a, b)` → ЯКЩО `counter(swap_charge, ==, 1)` → ТО `swap(orb_a, orb_b)`, `counter(swap_charge, =0)`.
- КОЛИ `input(double, orb)` → ЯКЩО `counter(double_charge, ==, 1)` → ТО `set_state(orb, double, 1 turn)`, `counter(double_charge, =0)`.
- КОЛИ `custom: «слово вистрілено»` → ТО `counter(swap_charge, +0.2)`, `counter(double_charge, +0.2)`.
- КОЛИ `counter(score, >, threshold)` → ТО `custom: «наступний рівень: важчі ряди ворогів, складніші набори літер, коротший таймер»`.
- КОЛИ `timer(row_time)` → ЯКЩО `mode(hardcore)` → ТО `custom: «вороги наступають»`, `spawn_at(enemy_row, top)`.
- КОЛИ `counter(health, <=, 0)` → ТО `game_over`, `window(end-screen)`.
- Перемога: — (нескінченна гра) · Поразка: здоровʼя 0 · Рахунок: +1 за вбитого ворога, +1 за курча чи ситу рослину, що дійшли донизу; рекорд окремо для Normal і Hardcore.

## Керування і ввід
- Миша/тач: клік по сфері-літері додає літеру; кнопки Fire (видно лише для валідного слова) і Erase.
- Клавіатура: друк літери = клік по відповідній сфері, Backspace — стерти, Enter — постріл.
- Вміння: клік по Swap → дві сфери; клік по Double → одна сфера (у рядку підказки «swap two letters» / «double letter dmg»).
- Старт: стрілками обрати режим (normal/hardcore), надрукувати слово «start» і вистрілити.

## Вікна, меню, HUD
- `game-screen` (старт): логотип, перемикач режиму стрілками, підказка «write "start" to begin», «score depend on killing not word length».
- `game-screen` (гра): поле 5×6, `+ui:letter-orbs`, `+ui:word-line` над ними, Fire/Erase, Swap і Double з `+ui:charge-ring`, `+ui:heart-pips` (серця з половинками + 5 крихт), `score`, `timer-countdown` у Hardcore, кнопки музики й виходу.
- Навчальні рядки в рядку підказок по одному на хід: «enemies can take 2 hits», «don't kill chickens», «chicken restore health», «check your special skills», «skills charge in 5 turns», «try to use all letters».
- `end-screen` поверх поля: «GameOver» + «New Score» (рекорд побито) або «High Score»; `popup-text` «!!! SPECIAL ATTACK !!!».

## Фічі поза полем
- `mode-select`: Normal (вороги стоять, доки ти не вистрілиш) і Hardcore (таймер ряду).
- Рекорди в localStorage окремо для кожного режиму (`leaderboard-local`); на Newgrounds — онлайн-таблиця.
- Прогресія всередині партії: 9 рівнів за порогами очок 20/30/60/70/100/110/150/160, далі нескінченно; рівень визначає пули рядів ворогів, «джокерів», ймовірність порожнього ряду, складність наборів літер і таймер.
- `onboarding-hints`: навчальні рядки по одному на хід на початку партії.
- Словник англійський з домішкою поширених неанглійських слів і власних назв (міста, імена).

## Варіації й родичі
- Родичі: [plants-vs-zombies](plants-vs-zombies.md) (колонки-смуги, вороги йдуть до краю), [rift-of-the-necrodancer](rift-of-the-necrodancer.md) (Hardcore — такт як таймер), [knucklebones](knucklebones.md) (кидок у колонку); словесні — Bookworm Adventures (слово = атака, без поля).
- **Осі варіацій** «слово як атака»: що визначає силу — довжина / рідкісність літер / позиція літери на полі (worDefense) · коли ходять вороги — після слова / за таймером · як вибирати літери — фіксований набір із повтором / плитки, що витрачаються.

## Цікавинки для курсу
- Слово → послідовність пострілів по колонках: перевірка словником + черга куль — 📎.
- Наступ із блокуванням: найближчі до низу ходять першими, крок коротшає до вільної клітини — 🌱.
- Бестіарій з 10 поведінок однією ієрархією класів (hit/attack/advance перевизначені) — 🥉; ідеальна вправа на наслідування.
- Елементаль: вибух у 4 кулі й ланцюгові реакції, скелет з «бронею» лише спереду — 📎.
- Генерація наборів з 5 літер за складністю (скільки слів можна скласти) — 🥈.
- Hardcore: той самий покроковий двіжок під таймером ряду — 🌱.

## Мапа на каталог
- Є: `word-validation` · `shoot-forward` ↔ куля вгору колонкою · `hp-damage` (краб, скелет, здоровʼя гравця) · `enemy-reached-base` · `spawn-schedule` ↔ ряд щоходу · `progress-acceleration` ↔ рівні за очками · `chain-reaction` ↔ елементаль · `event-points` · `score-records`/`leaderboard` · `move-timer` ↔ Hardcore · `mode-select` · `end-screen` · `keyboard-controls` · `cell-click` · `music-toggle`.
- **Нема** → пропозиції карток:
  - `+word-as-attack` «Складене слово стріляє літерами» · game-logic/constraints · 🥉.
  - `+directional-armor` «Броня лише з одного боку» · entities/combat · 📎.
  - `+vulnerability-toggle` «Ворог щокроку вразливий/невразливий» · entities/state · 🌱.
  - `+do-not-shoot` «Сутність, яку не можна вбивати» · entities/interact · 🌱.
  - `+partial-heal-pips` «N крихт = одиниця здоровʼя, удар обнуляє» · entities/state · 🌱.
  - `+letter-swap` «Поміняти дві позиції набору» · interface/input · 🌱.
  - `+step-blocking-advance` «Наступ кроком із блокуванням чергою» · entities/move · 🌱.

## Пропозиції до словників
- `+trigger:word_submitted` — гравець вистрілив валідне слово; `+trigger:enemy_moved` — ворог закінчив крок.
- `+effect:shoot` — випустити снаряд з клітини в напрямку; `+effect:toggle_state` — перемкнути двостанову сутність (рослина, око).
- `+cond:hit_from` — з якого боку прилетів удар (скелет).
- `+ui:letter-orbs` · `+ui:word-line` · `+ui:charge-ring` (заряд уміння) · `+ui:heart-pips` (половинки + крихти).
- `+card:word-as-attack`, `+card:directional-armor`.

## Джерела
- ⭐ [itch.io: worDefense](https://amidos2006.itch.io/wordefense) — мета, Normal/Hardcore, Swap і Double, 10 ворогів з поведінкою, автори, HTML5, клавіатура/миша/тач, коментарі автора про словник.
- [Девлог: Hardcore mode is now out](https://amidos2006.itch.io/wordefense/devlog/652459/hardcore-mode-is-now-out) — 18.12.2023, вороги йдуть самі, якщо зволікаєш.
- [HTML5-збірка гри](https://html-classic.itch.zone/html/9339140/index.html) — `out.js` (класи ворогів, PlayerEntity: 6 здоровʼя і 5 крихт, FireballEntity, порядок залпу, заряд +0.2), `assets/data/levels.json` (пороги, таймери), `tutorial.txt`, `start.txt`, `letters.txt`, `choices.txt`.

## Непевне
- (?) Рік першої публікації: на сторінці видно лише девлог 18.12.2023 і коментарі «2 роки тому»; поставлено 2023.
- (?) Яблуко є в коді, але не зустрічається в мапінгу рядів рівнів — можливо, вирізаний обʼєкт.
- (?) Набори літер: 5 різних літер щоходу з файла наборів, упорядкованого за «складністю»; що саме рахує ця оцінка — лише з коду (`getWords` рахує тролітерні слова).
- (?) Чи є гра на Newgrounds окремою сторінкою — у коді лише інтеграція таблиці рекордів.
