---
title: Gridspech
slug: gridspech
aka: []
family: thinky
also: [pencil-logic]
klass: puzzle
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: none
  goal: constraints
year: 2023
platforms: [web]
links:
  - {kind: itch, url: "https://krackocloud.itch.io/gridspech", best: true, note: "грати в браузері; керування (клік/протяжка, ПКМ — замок, Space — перевірка, A/D — рівні), devlog, коментарі"}
  - {kind: play, url: "https://gridspech.baublejar.com/", note: "повноекранна версія (краще на мобільному); у її JS — валідатори символів і 101 рівень, збірка 2026.3.22"}
  - {kind: other, url: "https://www.electrondance.com/puzzleworks-10-gridspech/", note: "огляд Electron Dance (2023): Witness-подібне навчання без тексту, порівняння з Understand і Taiji"}
  - {kind: other, url: "https://krackocloud.itch.io/gridspech/devlog/475096/postmortem", note: "постмортем: лінійна прогресія, перші 4 світи — 2 символи, солвер друга"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Gridspech+puzzle+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 75
mechanics: [cell-click, satisfy-constraints, completion-detection, markup-validity, conflict-highlight, connectivity-check, neighbor-count-clue, wrap-edges, keyboard-controls, sequential-levels, level-select, level-unlock, save-progress, restart-level, settings-window, about-window, volume-control, theme-select, sound-effects, +tile-toggle, +drag-paint-line, +player-lock-tile, +rule-teaching-by-example, +region-constraints, +endpoint-path, +one-king-per-region, +region-symbol-count, +novel-solution-alert]
proposes: ["+cond:unbranched_path", "+cond:one_per_region", "+feature:novel-solution-report", "+ui:player-lock-mark", "+axis:rules", "+axis:control", "+card:endpoint-path", "+card:one-king-per-region", "+card:region-symbol-count", "+card:novel-solution-alert", "+card:player-lock-tile"]
author: opus
date: 2026-11-19
---

# Gridspech — фарбуй плитки так, щоб виконались правила символів, яких гра не пояснює

## Суть
Браузерна Witness-подібна головоломка krackocloud (2023): сітка плиток, клік перемикає колір плитки, а символи на плитках — обмеження на звʼязні регіони одного кольору. Правила не пишуться ніде: кожен світ (A–I) вводить один новий елемент серією рівнів від тривіального до складного, і гравець виводить правило з прикладів та з підсвітки помилок після перевірки. Символів чотири види — кінець (end), корона (king), міна 1–3 (mine), звʼязка 1–2 (join); пізніше додаються переходи через край (wrap) і третій колір. Ядро — один ввід «перемкни плитку» і модульний набір валідаторів регіонів.

## Поле і час
- Прямокутна сітка від 3×1 до 8×8 плиток (дані рівнів у JS); частина клітин — діри: плитки нема, сусідство рветься.
- Сусідство — 4 напрямки. У світах H–I плитки мають стрілки-переходи (↑↓←→): сусід у цьому напрямку — наступна наявна плитка через діри й край поля, по колу.
- Стан плитки — колір: 0 (непідсвічена) або 1; у світі I — три кольори (0 / 1 / 2).
- Регіон — звʼязна область плиток одного кольору, зокрема й кольору 0.
- Час статичний: стан перевіряється лише за кнопкою Check; порушені символи підсвічуються на 1 с, штрафу нема.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Плитка | tile | колір 0 / 1 (/ 2 у світі I) | клік — наступний колір по колу; протяжка — колір першої плитки |
| Задана плитка | static | колір, смугаста позначка замка | не змінюється; частина умови рівня |
| Плитка під замком гравця | mark | діагональна риска | ПКМ ставить/знімає; клік її не змінює; Reset може зберегти замок (налаштування) |
| Діра | static | — | плитки нема: не сусід, розриває регіони |
| Перехід через край (wrap) | terrain | напрями ↑↓←→ | сусідство в цьому напрямку перескакує діри й край поля |
| Регіон | zone | колір | звʼязна (4-сусідство + wrap) область одного кольору |
| Кінець (end, два ромби) | mark | — | регіон його кольору — лінія без розгалужень і дотиків, що веде до іншого кінця |
| Корона (king) | mark | колір своєї плитки | у кожному регіоні цього кольору рівно одна корона цього кольору |
| Міна 1 / 2 / 3 (1–3 квадратики) | mark | N | рівно N із 4 сусідів підсвічені (колір ≠ 0) |
| Звʼязка 1 / 2 (зчеплені фігури) | mark | N | у регіоні плитки рівно N інших символів будь-якого виду |

## Правила (КОЛИ → ЯКЩО → ТО)
Ввід:
- КОЛИ `input(click, tile)` → ЯКЩО `not state(tile, locked)` і `not state(tile, player_lock)` → ТО `set_value(tile, (v+1) mod кольорів)`, `sound(click)`.
- КОЛИ `input(drag, tile)` → ЯКЩО ті самі умови → ТО `set_value(tile, колір першої плитки протяжки)`.
- КОЛИ `input(right_click, tile)` → ЯКЩО `not state(tile, locked)` → ТО `set_state(tile, player_lock)` (перемикач).
- КОЛИ `input(reset)` → ТО `set_value(усі незадані, 0)`.
- КОЛИ `input(reset)` → ЯКЩО `not mode(preserve_player_locks)` → ТО `clear_state(усі, player_lock)`.

Перевірка (КОЛИ `input(check)`), регіони — `connected` по 4-сусідству з wrap; порушений символ отримує стан `broken`:
- Кінець: КОЛИ `input(check)` → ЯКЩО `not custom: «рівно один сусід свого кольору, і далі лінія без розгалужень доходить до іншого кінця»` → ТО `set_state(end, broken)`; будь-яка зайва суміжна плитка того ж кольору — розгалуження.
- Корона: КОЛИ `input(check)` → ЯКЩО `not custom: «кожен регіон кольору корони містить рівно одну корону цього кольору»` → ТО `set_state(усі корони цього кольору, broken)`.
- Міна N: КОЛИ `input(check)` → ЯКЩО `adjacent_count(tile, lit, !=, N)` → ТО `set_state(mine, broken)`.
- Звʼязка N: КОЛИ `input(check)` → ЯКЩО `count(symbols_in_region(tile), !=, N+1)` → ТО `set_state(join, broken)`.
- Плитка без символу обмежень не має.
- КОЛИ `all_constraints_met` → ТО `win` («GOOD»), `sound(solved)`, `custom: «розвʼязок зберігається рядком, поле блокується»`, `unlock(next)`.
- КОЛИ `all_constraints_met` → ЯКЩО `custom: «розвʼязок не збігся з жодним авторським»` → ТО `message("Novel solution discovered! Please send a screenshot to the dev.")`.
- КОЛИ `constraint_broken` → ТО `flash(порушені символи)` на 1 с, `sound(error)`; нова спроба без штрафу.

Прогресія:
- КОЛИ `counter(solved_in_world, >=, mandatory)` → ТО `unlock(next_world)`, `message("<світ> unlocked!")`.
- КОЛИ `custom: «розвʼязано обовʼязкові рівні світу I»` → ТО `message("All main levels completed!")`, `unlock(congrats)`.
- Перемога: усі символи рівня виконано одночасно. · Поразка: нема. · Рахунку нема.

## Керування і ввід
- ЛКМ / тап по плитці — наступний колір (0→1→0; у світі I 0→1→2→0); протяжка — фарбує плитки під курсором кольором першої.
- ПКМ — замок гравця на плитці; на тачі замка нема (лише права кнопка миші, підтвердив і розробник).
- Space або кнопка-кільце — Check; R — Reset (неактивна, доки поле не змінено); A/← і D/→ — попередній / наступний рівень; Q/Esc — у меню.
- Undo нема — лише Reset. Після розвʼязку поле не редагується; відкритий знову розвʼязаний рівень показує збережений розвʼязок.

## Вікна, меню, HUD
- `level-select` (стартовий екран): світи A–I рядками кнопок-рівнів (закритий / розвʼязаний / extra); закритий світ — замок і «розвʼязано / потрібно» з попереднього; кнопки About і Settings; підпис «build 2026.3.22»; після головних рівнів — кнопка-нагорода → Congrats.
- `game-screen`: сітка; верхня панель — Main menu (Q/Esc), Reset (R), Previous (A/←), Next (D/→); під сіткою — кільце Check (Space) → «GOOD». HUD-лічильників нема.
- Тости на `game-screen`: «<світ> unlocked!», «Right-click to lock tiles» (рівень A11), «All main levels completed!».
- `settings-window`: Volume −/+, «Always use white color theme», «Force unlock all levels», «When resetting, preserve player-locked tiles», «Clear save data» → `confirm-dialog` («Are you sure you want to delete your progress?», «This is irreversible!»).
- `about-window`: де гра живе (baublejar, itch), ko-fi, кредити звуків.
- `end-screen` (Congrats): «Congrats! You made it to the end of Gridspech. Thank you for playing!!».
- Системний alert «Novel solution discovered!…».
- `editor-window` — у коді є (інструменти: переміщення, діра, замок, wrap, усі символи), гравцям не відкритий (?).
- Переходи: level-select → (рівень) game-screen → (GOOD) наступний рівень / тост розблокування → … → Congrats; level-select ↔ settings-window / about-window.

## Фічі поза полем
- Прогресія: 101 рівень у 9 світах (A 14 · B 9 · C 9 · D 11 · E 14 · F 9 · G 11 · H 14 · I 10). Світ відкривається, коли розвʼязано обовʼязкові рівні попереднього (A — усі 14; далі B 5 · C 7 · D 9 · E 8 · F 5 · G 9 · H 9 · I 6); решта — extra.
- Новий елемент на світ: A–B кінці · C–D корона · E міна 1 · F міни 2–3 · G звʼязки · H переходи wrap · I третій колір.
- `autosave` у localStorage: розвʼязки рівнів рядками й налаштування; «Clear save data» стирає.
- `restart-level` (Reset) зі збереженням замків за налаштуванням; undo, підказок, публічного редактора нема.
- Детектор «нового розвʼязку»: прийнятий розвʼязок порівнюється з авторськими, незнайомий — alert із проханням надіслати скриншот; автор так латав рівні (поза грою — солвер друга).
- Доступність: примусова біла тема, повне керування з клавіатури, мобільна версія без замків; «Force unlock all levels» — налаштування замість чітів.

## Варіації й родичі
- У корпусі: [Taiji + The Witness](taiji-witness-panels.md) (плитки вкл/вимк + символи регіонів, навчання без тексту), [Islands of Insight](islands-of-insight.md), [LOK Digital](lok-digital.md), [Understand](understand.md) (вгадати приховане правило).
- Паперові предки: Numberlink / Arukone (кінці, зʼєднані лінією; тут лінія — регіон одного кольору), сапер (міна рахує підсвічених сусідів), Nurikabe / Heyawake (обмеження на регіони кольору).
- Версії: itch 2023 («Gridspech is done!», 10.01.2023) → оновлення серпня 2024 (частину рівнів прибрано, решту перероблено) → збірка 2026.3.22 на baublejar.
- **Осі варіацій:** ввід — перемкнути плитку (Gridspech, Taiji) / провести лінію (Witness); кольорів — 2 / 3; що рахує символ — підсвічених сусідів (міна; у Taiji квітка — сусідів свого кольору) / символи в регіоні (звʼязка) / корони на регіон (корона); сусідство — звичайне / з переходами через край; перевірка — кнопкою (Gridspech) / одразу.

## Цікавинки для курсу
- Flood fill регіонів кольору з дірами й переходами через край — 🥉.
- Валідатори «символ → функція(сітка, плитка)», що повертають порушені плитки для підсвітки — 🥈 (модульна система правил).
- Кінець: прохід лінією без розгалужень до іншого кінця, зайва суміжна плитка того ж кольору — помилка — 📎.
- Корона: рівно одна корона свого кольору на кожен регіон цього кольору (мапа «плитка → власник») — 📎.
- Протяжка фарбуванням + замок гравця на плитці — 📎.
- Детектор нового розвʼязку (рядок поля проти списку еталонів) — 🌱; повний солвер рівня з відсіканням (2ⁿ / 3ⁿ станів) — 🥇.
- Генератор рівнів з єдиним розвʼязком — 👑.

## Мапа на каталог
- Є: `cell-click` ↔ клік по плитці; `satisfy-constraints` + `completion-detection` + `markup-validity` ↔ Check; `conflict-highlight` ↔ підсвітка порушених символів; `connectivity-check` ↔ регіони; `neighbor-count-clue` ↔ міна N; `wrap-edges` ↔ переходи через край; `keyboard-controls` ↔ Space/R/A/D/Q; `sequential-levels` + `level-select` + `level-unlock` ↔ світи A–I з квотами; `save-progress` ↔ localStorage; `restart-level` ↔ Reset; `settings-window`, `about-window`, `volume-control`, `theme-select` (біла тема), `sound-effects` (клік, помилка, розвʼязок).
- **Нема** → пропозиції карток:
  - `+tile-toggle` (Taiji) — слот {states: 2|3}.
  - `+drag-paint-line` (nonogram) — тут вільна протяжка, не лише рядок.
  - `+player-lock-tile` «Замок гравця на клітині, клік її не змінює» · interface/input · 🌱.
  - `+rule-teaching-by-example`, `+region-constraints` (Taiji) — повтор.
  - `+endpoint-path` «Два кінці, зʼєднані лінією-регіоном без розгалужень» · game-logic/constraints · 📎.
  - `+one-king-per-region` «Рівно один символ-власник на регіон кольору» · game-logic/constraints · 📎.
  - `+region-symbol-count` «Скільки символів у регіоні» · game-logic/constraints · 📎.
  - `+novel-solution-alert` «Гра помічає розвʼязок, якого не знав автор» · levels/solvability · 🌱.

## Пропозиції до словників
- `+cond:unbranched_path` — від клітини йде лінія одного кольору без розгалужень і дотиків до іншої клітини-кінця (родич `path_exists`).
- `+cond:one_per_region` — у кожному регіоні кольору рівно один такий символ (корона).
- `+feature:novel-solution-report` — прийнятий, але невідомий авторові розвʼязок → прохання надіслати.
- `+ui:player-lock-mark` — позначка «плитку замкнено гравцем» (відмінна від заданої умовою).
- `+axis:rules` — `discovered` (правила фіксовані, але не пояснені); `+axis:control` — `toggle`.
- `+card:endpoint-path`, `+card:one-king-per-region`, `+card:region-symbol-count`, `+card:novel-solution-alert`, `+card:player-lock-tile` — див. «Мапа на каталог».

## Джерела
- ⭐ [itch.io: Gridspech](https://krackocloud.itch.io/gridspech) — грати; керування; devlog (2022–2024); коментарі про корони, ромби, секції A–I, відсутність undo й замків на тачі.
- [gridspech.baublejar.com](https://gridspech.baublejar.com/) — повноекранна збірка 2026.3.22; у JS — функції перевірки end/king/mine/join, сусідство з wrap, 101 рівень, квоти світів, тексти меню.
- [Electron Dance: Puzzleworks #10](https://www.electrondance.com/puzzleworks-10-gridspech/) — огляд 2023: навчання без тексту, «кожне обмеження звужує простір», порівняння з Understand і Taiji.
- [Devlog: postmortem](https://krackocloud.itch.io/gridspech/devlog/475096/postmortem) — лінійна прогресія, перші 4 світи на 2 символах, солвер проти «нових розвʼязків».
- YouTube: [пошук «Gridspech puzzle gameplay»](https://www.youtube.com/results?search_query=Gridspech+puzzle+gameplay).

## Непевне
- (?) Опис — за поточною збіркою 2026.3.22; у версії 2023 рівні й нумерація були інші (коментарі згадують C11, якого тепер нема), огляд 2023 називає символи «корона, кайт, єпископ».
- (?) Назви символів — з коду (end / king / mine / join), візуал — з їхніх SVG; які кольори має колір 1 / 2 у кожній темі, не перевірено.
- (?) Редактор: режим є в коді, клавіша E оголошена, але в обробнику клавіш гри не викликається — гравцям, схоже, недоступний.
- (?) Точний текст позначки рівня («E13» тощо) і поведінка тостів — висновок із коду, гру не запускав.
