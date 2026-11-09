---
title: Survivors
slug: survivors
aka: []
family: dig-gravity
also: [thinky]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: none
  goal: collect
year: 1986
platforms: [ZX Spectrum, C64, Atari 8-bit, BBC Micro, Acorn Electron, C16/Plus4, MSX, Amstrad CPC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Survivors_(video_game)", best: true, note: "три дроїди з одним умінням кожен, енергія, поразка при втраті будь-кого"}
  - {kind: other, url: "https://8bs.com/elecgame/survivors.htm", note: "інструкція з вкладки (BBC/Electron): сім рівнів, клавіші, HUD"}
  - {kind: other, url: "https://worldofspectrum.org/pub/sinclair/games-info/s/Survivors.txt", note: "інструкція ZX Spectrum: клавіші, вибір дроїда 1/2/3, нове життя"}
  - {kind: other, url: "https://spectrumcomputing.co.uk/zxsr.php?id=5083", note: "огляди ZX-версії (бачив у пошуку)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Survivors+1986+Atlantis+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [party-switch, dig-terrain, push-object, gravity-fall, item-pickup, collect-all, hp-damage, environment-death, time-out, sequential-levels, game-pause, sound-effects, status-panel, keyboard-controls, remaining-counter, +split-abilities, +crush-enemy-by-fall, +trap-enemy, +any-member-lost, +manual-restart]
proposes: ["+trigger:smashed", "+cond:ability", "+effect:rescue", "+role:rescuee", "+card:split-abilities", "+card:any-member-lost", "+axis:actors-party-specialized"]
author: opus
date: 2026-11-09
---

# Survivors — Boulder Dash, розібраний на трьох дроїдів: один копає, другий рятує, третій штовхає

## Суть
Класична фізика rocks-and-diamonds (земля, каміння падає, коли під ним порожньо), але дії гравця **розділені між трьома дроїдами**: дроїд 1 лише копає тунелі, дроїд 2 лише «телепортує» вцілілих (аналог збирання діамантів), дроїд 3 лише штовхає каміння. Гравець перемикає активного дроїда клавішею 1/2/3 і планує, хто куди пройде. Якщо будь-який дроїд загинув або замурований — рівень не пройти: це одна команда з трьох незамінних членів.

## Поле і час
- Квадратна сітка печери (купол гібернації); розмір поля і скрол — не перевірено (?).
- Real-time: каміння падає без участі гравця, вартові-мутанти рухаються самі.
- Зворотний таймер рівня (радіація посилюється) — час вичерпано → поразка.
- Сім рівнів (за інструкцією з вкладки).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Дроїд 1 (копач) | player | енергія | рух 4 напрямки; прокопує землю «на великій швидкості»; не штовхає й не рятує |
| Дроїд 2 (телепортер) | player | енергія | ходить лише вільними тунелями; наступ на вцілілого — той телепортується в безпеку |
| Дроїд 3 (силач) | player | енергія | штовхає по одному каменю; не копає |
| Земля | terrain | — | прохідна лише для дроїда 1; після нього — порожня клітина |
| Камінь (boulder) | object | — | падає, коли під ним порожньо; удар по дроїду знімає багато енергії; давить вартових |
| Вцілілий (survivor) | pickup | — | зникає, коли на нього стає дроїд 2; лічильник «врятовано / лишилось» |
| Вартовий Mk.1 (Guardian) | enemy | — | рухається сам (?); дотик знімає енергію дроїда; гине під каменем або замурований камінням |
| Стіна купола | static | — | непрохідна (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(select, n)` → ТО `custom: «активним стає дроїд n; решта стоять»`.
- КОЛИ `input(move, dir)` → ЯКЩО `free(cell)` → ТО `move(active, dir)`.
- КОЛИ `contact(droid1, earth)` → ТО `set_cell(cell, empty)`, `move(droid1, dir)`.
- КОЛИ `contact(droid2|droid3, earth)` → ТО `block`.
- КОЛИ `contact(droid3, boulder)` → ЯКЩО `free(cell_behind)` → ТО `push(boulder)`; інакше `block`.
- КОЛИ `contact(droid1|droid2, boulder)` → ТО `block`.
- КОЛИ `contact(droid2, survivor)` → ТО `pickup`, `counter(saved, +1)`, `score(n)` (?).
- КОЛИ `contact(droid1|droid3, survivor)` → ТО `block` (?).
- КОЛИ `tick` → ЯКЩО `free(below)` → ТО `fall(boulder)`.
- КОЛИ `custom: «камінь упав на дроїда»` → ТО `hp(droid, -n)` — «серйозна» втрата енергії, не миттєва смерть.
- КОЛИ `contact(guardian, droid)` → ТО `hp(droid, -n)`.
- КОЛИ `custom: «камінь упав на вартового»` → ТО `disappear_b`.
- КОЛИ `custom: «вартовий оточений камінням і не може рухатися»` → ТО `disappear_a` (?) — «trap» за інструкцією; чи зникає, чи просто знешкоджений — не перевірено.
- КОЛИ `hp_zero(droid)` → ТО `restart` — «треба починати знову».
- КОЛИ `custom: «будь-який дроїд замурований без виходу»` → ТО `custom: «рівень непрохідний»`; гравець сам перезапускає (ESC×2 / 4+5).
- КОЛИ `all_gone(survivor)` → ТО `next_level`; після сьомого — `win`.
- КОЛИ `counter(time, <=, 0)` → ТО `lose` — радіація стала надто сильною.
- Перемога: усі вцілілі врятовані на всіх рівнях · Поразка: час вичерпано, енергія будь-якого дроїда = 0 · Рахунок: на екрані є, правила нарахування — не знайдено.

## Керування і ввід
- ZX: Q/A/O/P — вгору/вниз/вліво/вправо; BBC/Electron: Z/X — вліво/вправо, * і ? — вгору/вниз.
- 1, 2, 3 — вибрати дроїда (перемикання миттєве, `party-switch`).
- ZX: 4+5 разом — нове життя (вихід із глухого кута); BREAK+CAPS — нова гра; ENTER — пауза.
- BBC/Electron: ESC — пауза (будь-яка клавіша — далі), ESC двічі — нове життя; Q — звук увімк./вимк.

## Вікна, меню, HUD
- `game-screen`: поле + панель: енергія кожного з трьох дроїдів, рахунок, час, «лишилось людей», «врятовано людей».
- `splash-screen` / заставка з таблицею клавіш (?).
- `pause-menu` — без пунктів: пауза до будь-якої клавіші.
- `end-screen` — кінець гри (?).
- HUD: `energy-bar` ×3, `score`, `timer-countdown`, `remaining-counter` (лишилось), `progress-bar`/лічильник «врятовано».

## Фічі поза полем
- `levels-sequential` — сім рівнів поспіль.
- `pause`, `sound-toggle`.
- Ручний рестарт життя (ESC×2 / 4+5) — замість undo: застряг — почни знову.

## Варіації й родичі
- Сімʼя: [boulder-dash](boulder-dash.md) (ядро фізики), [xor](xor.md) (два аватари з перемиканням, без таймера), [supaplex](supaplex.md), [repton](repton.md).
- Сусіди поза сімʼєю: The Lost Vikings (троє з різними вміннями, 1993), Kwirk/Catrap (`party-switch` у push-slide).
- **Осі варіацій**: аватари — «один усе вміє (BD) / двоє однакових (XOR) / троє, кожен з одним дієсловом (Survivors)»; поразка — «втрата життя / втрата будь-якого члена команди = рівень зламано»; вороги — «вбивають дотиком / знімають енергію».

## Цікавинки для курсу
- Розділення дієслів між аватарами: таблиця «хто що може з якою клітиною» — 📎: та сама `interaction-table`, але з ключем «дроїд × клітина».
- Перемикання активного аватара 1/2/3 із застиглими іншими — 🌱.
- Енергія замість смерті від дотику (HP у кожного члена команди окремо) — 📎.
- Детектор «рівень зламано»: чи може ще кожен дроїд дістатись потрібних клітин (BFS з урахуванням умінь) — 🥇.
- Убити ворога каменем згори або замурувати (перевірка «нема вільних сусідів») — 📎.

## Мапа на каталог
- Є: `party-switch` ↔ клавіші 1/2/3 · `dig-terrain` ↔ дроїд 1 · `push-object` ↔ дроїд 3 · `gravity-fall` ↔ каміння · `item-pickup` + `collect-all` ↔ вцілілі · `hp-damage` ↔ енергія · `environment-death` ↔ камінь згори · `time-out` ↔ радіація · `sequential-levels` · `game-pause` · `sound-effects` · `status-panel` · `remaining-counter` · `keyboard-controls`.
- **Нема** → пропозиції карток:
  - `+split-abilities` «Кожен аватар має лише свої дієслова» · entities/legality · 📎 · слот {avatar → verbs}.
  - `+any-member-lost` «Втрата будь-якого члена команди = поразка» · game-logic/lose · 🌱.
  - `+crush-enemy-by-fall` «Ворог гине під падаючим обʼєктом» · entities/death · 🌱 (повтор BD).
  - `+trap-enemy` «Замурувати ворога» · entities/death · 📎.
  - `+manual-restart` (повтор Heartlight) — нове життя клавішею при глухому куті.

## Пропозиції до словників
- `+trigger:smashed` — на сутність упав обʼєкт (повтор з Heartlight; тут двічі: дроїд і вартовий).
- `+cond:ability(a, verb)` — чи вміє активний аватар це дієслово (копати / штовхати / рятувати).
- `+effect:rescue` — «зібрати» живу сутність телепортом (лічильник врятованих; візуально ≠ pickup).
- `+role:rescuee` — сутність, яку треба врятувати, а не зібрати (Lemmings, Survivors, Choplifter).
- `+card:split-abilities` · `+card:any-member-lost` — див. «Мапа на каталог».
- `+axis:actors-party-specialized` — значення осі `actors`: «загін із різними вміннями» на відміну від `party`.

## Джерела
- ⭐ [Wikipedia: Survivors](https://en.wikipedia.org/wiki/Survivors_(video_game)) — три дроїди, енергія, вартові, поразка при втраті дроїда, платформи й роки.
- [8bs.com: Survivors](https://8bs.com/elecgame/survivors.htm) — текст вкладки BBC/Electron: сім рівнів, клавіші, HUD, ESC×2.
- [World of Spectrum: інструкція](https://worldofspectrum.org/pub/sinclair/games-info/s/Survivors.txt) — клавіші ZX, 1/2/3, 4+5, ENTER-пауза.
- [Spectrum Computing: огляд](https://spectrumcomputing.co.uk/zxsr.php?id=5083) — сторінка оглядів (у пошуку, не відкривав).
- YouTube: пошук «Survivors 1986 Atlantis gameplay».

## Непевне
- (?) Чи котиться камінь з каменя (roll-off), чи лише падає прямо — джерела кажуть лише «падає, коли під ним порожньо».
- (?) Як рухаються вартові (патруль, погоня) і чи вбиває їх «замурування», чи лише знешкоджує.
- (?) Скільки життів, як нараховуються очки, чи блокують вцілілі дроїдів 1 і 3.
- (?) Розмір поля, скрол, тривалість таймера рівня.
