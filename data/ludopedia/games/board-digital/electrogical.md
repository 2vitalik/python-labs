---
title: Electrogical (エレクトロジカル)
slug: electrogical
aka: [エレクトロジカル]
family: board-digital
also: [connect-rotate, word-number]
klass: cursor
axes:
  field: square
  time: programmed
  opponent: none
  info: full
  random: none
  goal: state
year: 2026
platforms: [PC (Steam, Windows)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/2501650/Electrogical/", best: true, note: "kinjo / Phoenixx; повний реліз 15.04.2026, ранній доступ з 21.11.2024: «jigsaw puzzles + four basic arithmetic operations», 250+ пазлів без ліміту часу, лише мишка, підказки, Steam Leaderboards"}
  - {kind: other, url: "https://www.famitsu.com/article/202610/91465", note: "Famitsu (JA): старт «通電», мета — точне число на цілі, обчислення по шляху (−1 → +4 → +2), NEKO йде в бік виступу фігури, бездротова, ковзна й поворотна фігури, автовідповідь"}
  - {kind: other, url: "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=2501650&count=30&maxlength=4000", note: "патчноути: фігури Start і Goal, Magnet, Rocket з прев'ю шляху, розширення й квадрати 2×2/3×3, фішки очок за парні/непарні/прості, ~30 типів фігур, Insight Hint Puzzles"}
  - {kind: other, url: "https://www.stackup.org/post/review-electrogical", note: "огляд: фігури з числом або знаком дії, дивні форми фігур і плати, автоматичне розвʼязання, приховані записи-логи"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Electrogical+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [cursor-place, multi-cell-size, pipe-connectors, tile-rotate, teleport, path-preview, movement-animation, conflict-highlight, restart-level, world-map, level-select, level-unlock, sequential-levels, leaderboard, achievements-window, settings-window, game-screen, +arithmetic-path, +number-combine, +electric-signal, +run-simulation, +rail-slider, +magnet-pull, +rocket-piece, +piece-extension, +parity-prime-bonus, +hint-solution-steps, +show-solution, +insight-puzzles, +piece-tray-cycle, +lore-logs]
proposes: ["+effect:apply_op", "+cond:is_prime", "+ui:piece-tray", "+feature:insight-puzzles", "+card:arithmetic-path", "+card:rail-slider", "+card:parity-prime-bonus"]
author: opus
date: 2026-11-19
---

# Electrogical — клади пазли-фігури з +1, −1, ×, ÷ на плату так, щоб струм приніс на ціль рівно потрібне число

## Суть
Японська казуальна головоломка розробника kinjo (видавець Phoenixx): «пазл + чотири дії арифметики». На платі, схожій на друковану, є старт «通電» (подати струм) і ціль із числом; гравець розкладає фігури-пазли з виступами й западинами, на кожній — дія (+n, −n, множення, дріб). Після запуску суперпровідна істота NEKO біжить від старту фігура за фігурою в бік виступів, і кожна змінює заряд по черзі (−1 → +4 → +2); на цілі має вийти **точно** задане число. Пізніші етапи додають закріплені поворотні фігури, ковзні на рейках, бездротові переходи, магніт, ракету й етапи-челенджі з очками й таблицями рекордів.

## Поле і час
- Плата — поле клітин неправильної форми, «схоже на складну друковану плату»; фігури теж різної форми, тож треба і вмістити їх, і скласти правильний ланцюжок (?) — точна сітка не описана в джерелах.
- Шари: плата (клітини, рейки) + фігури (вільні з лотка або закріплені заздалегідь) + NEKO під час прогону.
- Дві фази: **розкладка** (статична, без часу) → **прогін** після кліку по старту: NEKO йде шляхом, фігури спрацьовують по черзі, ковзна фігура їде рейкою, ракета й магніт зсувають фігури → перевірка на цілі (`time: programmed`).
- Етапи мають номери «світ-етап» (7-5, 21-5) на мапі; Chapter 1 → Reactor Stage → Chapter 2, далі пост-сюжетні, пробні й челендж-етапи. Ліміту часу нема.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| NEKO (超伝導生命体) | neutral | заряд — поточне число | після запуску йде від фігури до фігури в бік опуклого виступу, несе заряд |
| Фігура Start («通電») | source | початкове значення (?) | клік запускає прогін; її може зсунути магніт |
| Фігура Goal | sink | цільове число | приймає NEKO; число блимає, якщо заряд не збігся |
| Фігура-дія | conduit | +n / −n / ×n / дріб, форма з виступами | змінює заряд, коли NEKO проходить; веде далі в бік виступу |
| Поворотна фігура | conduit | закріплена на платі | рухати не можна, можна змінити кут |
| Ковзна фігура | conduit | стоїть на рейці | коли NEKO поруч — їде рейкою до кінця й стикується з фігурою там |
| Бездротова фігура | conduit | віддалений партнер | переносить NEKO на віддалене місце без сусідства |
| Магніт | switch | — | притягує / зсуває інші фігури (?) |
| Ракета | object | шлях руху | рухається під час прогону; з v1.4.0 шлях показано заздалегідь |
| Фігура-розширення | conduit | чіпляється до інших (?) | впливає на очки квадратів 2×2 і 3×3 у челенджах (?) |
| Фішка очок | pickup | парні / непарні / прості; Comeback Circuit Chip | у челендж-етапах додає очки за значення |
| Лоток фігур | supply | непокладені фігури | колесо миші перебирає; ПКМ повертає фігуру сюди |
| Плата | zone | форма, рейки, закріплені фігури | місце для фігур |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(place(piece, cells))` → ЯКЩО `fits(piece, cells)` (?) → ТО `place(player, piece)`; інакше `block`.
- КОЛИ `input(rmb(piece))` → ТО `custom: «фігура повертається на початкову позицію»` (v1.0.1).
- КОЛИ `input(click(piece_a, piece_b))` → ТО `swap(piece_a, piece_b)` — обмін одним кліком (реліз 1.2).
- КОЛИ `input(wheel)` → ТО `custom: «вибрати наступну непокладену фігуру»` (v1.3.0).
- КОЛИ `input(click(rotatable))` → ТО `rotate(piece, step)` (крок кута — (?)).
- КОЛИ `input(click(start))` → ТО `set_state(neko, running)`, `set_value(charge, start_value)` (?).
- КОЛИ `enter(neko, piece)` → ТО `set_value(charge, charge ∘ piece.op)` (+n, −n, ×n, дріб), `move(neko, custom: «на сусіда в бік опуклого виступу»)`.
- КОЛИ `enter(neko, wireless)` → ТО `teleport(neko, linked)`.
- КОЛИ `adjacent(neko, slider)` → ТО `slide(slider, rail_dir)` — до кінця рейки, де фігура (за Famitsu).
- КОЛИ `custom: «спрацював магніт»` → ТО `pull(pieces)` (?) — може зсунути навіть Start (патч 1.2.1).
- КОЛИ `custom: «спрацювала ракета»` → ТО `move(rocket, path)` (?); шлях видно заздалегідь.
- КОЛИ `custom: «NEKO знову проходить уже заживлену фігуру»` → ТО `custom: «повторна активація»` (?) — згадано в анонсі оновлень.
- КОЛИ `reach(neko, goal)` → ЯКЩО `counter(charge, ==, target)` → ТО `win`, `next_level`; інакше `flash(goal)` — число цілі блимає, розкладку можна правити.
- Челендж-етапи: КОЛИ `level_end` → ТО `score(+n)` за фішки — парні, непарні чи прості значення («Prime Number Combo», квадрати 2×2/3×3); рахунок іде в Steam Leaderboards етапу.
- КОЛИ `input(click(hint))` → ТО `custom: «підказка крок за кроком: місце однієї фігури»`.
- КОЛИ `input(click(auto_answer))` → ТО `custom: «показати розвʼязок»`.
- Перемога: заряд на цілі = цільове число · Поразка: нема (часу й ходів не рахують) · Рахунок: лише в челенджах (фішки) → таблиці рекордів.

## Керування і ввід
- Лише мишка: взяти фігуру з лотка й покласти на плату (перетягування чи клік — (?)), ПКМ — повернути фігуру в лоток, колесо — перебрати непокладені, клік по двох фігурах — обміняти.
- Клік по поворотній фігурі — змінити кут; клік по Start — запуск.
- На мапі колесо — масштаб (v1.0.1).

## Вікна, меню, HUD
- `map-window` / `world-map`: етапи вузлами з номерами, позначка «!» на оновлених етапах; Chapter 2 відкривається після Reactor Stage (кнопка пропуску для гравців раннього доступу).
- `game-screen`: плата, лоток фігур, NEKO, номер етапу праворуч угорі, кнопка скидання, кнопка рейтингу (`leaderboard` етапу), підказки; число на цілі блимає при розбіжності; прев'ю шляху ракети (`path-preview`); підказки-тултіпи інтерфейсу (v1.0.6).
- `hints-window`: покрокова підказка й автовідповідь; `custom-window` «Insight Hint Puzzles» — необовʼязкові спрощені пазли, що пояснюють ідею, а не відповідь.
- `log-window` (?): приховані записи колишніх колег про станцію — сюжет.
- `settings-window`: збереження з кнопкою видалення (з 1.2.1 — захист від випадкового), версія збірки; `achievements-window` (Steam, 4).
- Переходи: мапа → етап → (прогін збігся) → наступний етап на мапі.

## Фічі поза полем
- `levels-sequential` + `world-map`: 250+ пазлів, сюжет у двох розділах; у ранньому доступі (v1.1.0) додали 32 пост-сюжетні, 7 пробних і 25 челендж-етапів з фішками.
- `hint` (крок за кроком по одній фігурі), `show-solution` (автовідповідь), `+feature:insight-puzzles`.
- `leaderboard-online` (Steam Leaderboards на етап), `achievements`, `cloud-save`, `localization` (JA, EN, zh-Hans, zh-Hant, DE, RU).
- `restart-level` (скидання), без undo-кнопки в описах (?); `collectibles` — приховані логи сюжету.
- Окремо від автора — EQUALINE, гра на швидкий рахунок (у бандлі) (?).

## Варіації й родичі
- Еволюція в ранньому доступі: від базових фігур-дій до ~30 типів (травень 2025) — ковзні, поворотні, бездротові, магніт, ракета, розширення, фішки очок.
- Родичі в корпусі: `word-number/nyt-digits.md`, `word-number/countdown-numbers.md`, `word-number/krypto.md` (скласти ціль із чисел і дій), `connect-rotate/railway-islands.md` (розкладка → запуск → перевірка), `connect-rotate/trainyard.md`, `connect-rotate/electric-box.md` (струм через деталі), `board-digital/daedalian-opus.md` і `cats-organized-neatly.md` (вкласти фігури в поле).
- **Осі варіацій**: напрям потоку (виступ пазла / порти труби / стрілка) · дії (лише +/− / ×, ÷, дроби) · фігури (вільні / закріплені поворотні / ковзні / телепорт) · мета (точне число / максимум очок у челенджі).

## Цікавинки для курсу
- Значення вздовж шляху: граф фігур, напрям за виступом, застосування дій по черзі, перевірка «рівно ціль» — 📎.
- Розвʼязувач: перебір розкладок фігур по слотах з відсіканням за проміжними значеннями — 🥇.
- Подієві фігури під час прогону (ковзна, магніт, ракета, повторна активація) — порядок спрацювань у симуляції — 🥈.
- Фішки очок: бонус за парні / непарні / прості значення + рекорди етапу — 🌱 (`is_prime`) / 📎 з таблицею.
- Покрокова підказка з еталонного розвʼязку (одна фігура на місце) — 🌱.
- Прев'ю шляху рухомої фігури до запуску — 📎.

## Мапа на каталог
- Є: `cursor-place` ↔ фігура з лотка на плату; `multi-cell-size` (?) ↔ фігури різної форми; `pipe-connectors` ↔ виступи як вихід; `tile-rotate` ↔ поворотна фігура; `teleport` ↔ бездротова; `path-preview` ↔ шлях ракети; `movement-animation` ↔ NEKO біжить; `conflict-highlight` ↔ число цілі блимає; `restart-level`; `world-map` + `level-select` + `level-unlock` + `sequential-levels`; `leaderboard`; `achievements-window`, `settings-window`, `game-screen`.
- **Нема** → пропозиції карток:
  - `+arithmetic-path` «Значення змінюється на кожній фігурі шляху; ціль — точне число» · game-logic/constraints · 📎.
  - `+rail-slider` «Фігура їде рейкою, коли поруч сигнал» · entities/move · 📎.
  - `+parity-prime-bonus` «Бонус за парні / непарні / прості значення» · game-logic/score · 🌱.
  - `+magnet-pull`, `+rocket-piece`, `+piece-extension` — подієві фігури прогону (кандидати, коли знайдуться ще ігри).
  - `+insight-puzzles` «Необовʼязкові пазли-пояснення ідеї» · levels/bank · 🌱.

## Пропозиції до словників
- `+effect:apply_op` — застосувати арифметичну дію фігури до поточного значення (Electrogical, NYT Digits).
- `+cond:is_prime` — число просте (фішки очок).
- `+ui:piece-tray` — лоток непокладених фігур з перебором колесом.
- `+feature:insight-puzzles` — необовʼязкові пазли, що пояснюють механіку.
- `+card:arithmetic-path`, `+card:rail-slider`, `+card:parity-prime-bonus` — див. «Мапа на каталог».

## Джерела
- ⭐ [Steam: Electrogical](https://store.steampowered.com/app/2501650/Electrogical/) — опис (EN/JA): пазл + чотири дії, «+1 or −1 to find the target number», 250+ пазлів, мишка, підказки, сюжет про «Power Distribution Dungeons» і NEKO; JSON appdetails — категорії (Leaderboards), 4 досягнення, «piece placement, number manipulation, score selection».
- [Famitsu](https://www.famitsu.com/article/202610/91465) — старт «通電», точне число на цілі, приклад −1 → +4 → +2, NEKO йде в бік виступу, бездротова / ковзна / поворотна фігури, автовідповідь, логи колег.
- [Steam News API](https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=2501650&count=30&maxlength=4000) — патчі v1.0.1–v1.4.0: ПКМ, блимання цілі, рейки, магніт, ракета, розширення 2×2/3×3, фішки парні/непарні/прості, Chapter 2, Insight Hint Puzzles.
- [Stackup](https://www.stackup.org/post/review-electrogical) — огляд раннього доступу: фігури з числом або знаком, дивні форми, автоматичне розвʼязання.

## Непевне
- (?) Чи плата — звичайна квадратна сітка і чи фігури багатоклітинні; джерела кажуть лише «дивні форми» фігур і плати.
- (?) Початкове значення старту і чи шлях може розгалужуватись; напрям «у бік виступу» — лише за Famitsu.
- (?) Точна дія магніту, ракети, фігур-розширень і «повторної активації» — відомі з патчноутів лише назвами.
- (?) Як саме нараховуються очки в челенджах (фішки, «Prime Number Combo (Diff.)», квадрати 2×2/3×3) і чи мають очки звичайні етапи («aim for a high score in each stage»).
- (?) Спосіб розміщення (перетягування чи клік) і наявність undo.
- (?) EQUALINE — чи це гра того самого автора.
