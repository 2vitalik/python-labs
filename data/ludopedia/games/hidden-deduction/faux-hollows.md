---
title: Faux Hollows (Final Fantasy XIV)
slug: faux-hollows
aka: [Faux Hollows]
family: hidden-deduction
also: []
klass: cursor
axes:
  field: square
  time: turn
  opponent: none
  info: hidden
  random: setup
  goal: score
year: 2020
platforms: [PC (Windows, macOS), PlayStation, Xbox — мінігра всередині Final Fantasy XIV]
links:
  - {kind: wiki, url: "https://ffxiv.consolegameswiki.com/wiki/Faux_Hollows", best: true, note: "правила: 6×6, 5 заблокованих, 4 патерни × 4 повороти, 11 відкриттів, фігури і листки, retelling, доступ раз на тиждень, досягнення"}
  - {kind: play, url: "https://faux.joshuaen.com", note: "спільнотний розвʼязувач на даних спільноти"}
  - {kind: other, url: "https://github.com/JoshuaEN/ffxiv-faux-hollows", note: "код розвʼязувача: стани клітин, патерни, 4 місця лиса на патерн, статистика стратегій ≤11 ходів"}
  - {kind: other, url: "https://docs.google.com/spreadsheets/d/1mUyCzlzDmdXMwaSTUgWXtEA45oJNn-iB4_bVM43zf58/edit#gid=49331949", note: "таблиця спільноти (u/Ylandah): усі патерни заблокованих панелей і місця Commander (не відкривалась)"}
  - {kind: wiki, url: "https://ffxiv.consolegameswiki.com/wiki/Patch_5.3", note: "патч 5.3 «Reflections in Crystal», 11.08.2020"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=FFXIV+Faux+Hollows+guide", note: "пошук; гайди"}
stage: v1
coverage: 70
mechanics: [cell-click, move-limit, event-points, level-solver, shop-window, achievements-window, game-screen, +shape-bank, +pattern-library, +fixed-pattern-deduction, +weekly-attempt, +expected-moves-solver]
proposes: ["+trigger:shape_uncovered", "+cond:pattern_candidates", "+ui:uncover-counter", "+feature:weekly-challenge", "+card:fixed-pattern-deduction", "+card:weekly-attempt", "+card:expected-moves-solver"]
author: opus
date: 2026-11-09
---

# Faux Hollows — 6×6 закритих панелей, 11 відкриттів: знайди сховані 2×3, 2×2 і 1×1 за видимим патерном блоків

## Суть
Мінігра Final Fantasy XIV (патч 5.3, 2020) — нагорода за unreal-трайл раз на тиждень. Поле 6×6, пʼять панелей заблоковані й видні одразу; під рештою сховані три фігури: мечі 2×3 (або 3×2), скриня/подарунок 2×2 і лис-Commander 1×1. Гравець має **11 відкриттів**; кожна відкрита фігура дає «листки» (Faux Leaves), і що менша фігура, то дорожча. Чисел-підказок нема: інформацію дають заблоковані панелі (вони визначають, який із 16 патернів зараз) і відкриті порожні клітини — тобто це сольний «Морський бій» по скінченній бібліотеці розкладок.

## Поле і час
- Сітка 6×6 = 36 панелей; 5 заблоковані; 4 базові патерни заблокованих панелей × 4 повороти = 16 полів.
- Фігури не можуть накривати заблоковані панелі; можливі розкладки обмежені списком, який спільнота зібрала вручну.
- Хід = відкрити одну панель; ліміт — 11 ходів; часу нема.
- Шари: прихований стан панелі (порожньо / мечі / скриня / лис / блок) + відкрито чи ні.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Закрита панель | static | — | відкривається за 1 хід з 11 |
| Заблокована панель | static | 5 на поле, видно з початку | не відкривається; фігура на ній не лежить; задає патерн |
| Порожня панель | mark | — | «змарнований» хід, але звужує розкладки |
| Dual Blades (мечі) | object | 2×3 або 3×2 | є завжди; 15 листків + retelling |
| Coffer (скриня) | object | 2×2 | 35 листків; на полі або вона, або Gift Box |
| Gift Box (подарунок) | object | 2×2 | 25 листків |
| Faux Commander (лис) | object | 1×1 | 100 листків; лише у фіксованих місцях — 4 можливі на патерн, залежать від розкладки мечів і скрині |
| Лічильник відкриттів | resource | 11 | −1 за кожну відкриту панель |
| Faux Leaves | resource | — | валюта обміну в Idyllshire |
| Retelling | pickup | ≤1 на тиждень | ще одна спроба unreal-трайлу і Faux Hollows до кінця тижня |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `level_start` → ТО `custom: «обрати один із 16 патернів блоків і розкладку фігур з дозволених»`, `reveal(blocked)`.
- КОЛИ `input(uncover, c)` → ЯКЩО `counter(uncovers, >, 0)` and `not cell(c, blocked)` → ТО `reveal(c)`, `counter(uncovers, -1)`.
- КОЛИ `input(uncover, c)` → ЯКЩО `cell(c, blocked)` → ТО `block`.
- КОЛИ `custom: «усі панелі фігури відкрито»` → ТО `currency(+листки)`: мечі 15 · подарунок 25 · скриня 35 · лис 100.
- КОЛИ `custom: «мечі відкрито повністю»` → ЯКЩО `custom: «retelling цього тижня ще не отримано»` → ТО `give(player, retelling)`.
- КОЛИ `counter(uncovers, ==, 0)` → ТО `game_over` (спробу завершено).
- Обмеження розкладки: `fits(shape, cells)` без блоків; лис — лише в одному з 4 місць свого патерну.
- Доступ: КОЛИ `custom: «пройдено unreal-трайл і поговорено з Faux Commander»` → ЯКЩО `custom: «цього тижня ще не грав або є retelling»` → ТО `window(game-screen)`; скидання — щовівторка.
- Перемога: формально нема — мета набрати якомога більше листків за 11 ходів. · Поразка: нема. · Рахунок: листки за відкриті фігури.

## Керування і ввід
- Курсор/геймпад: вибрати панель і підтвердити відкриття. Позначок, undo і підказок у грі нема.
- Стратегія: заблоковані панелі ідентифікують патерн (розвʼязувачу досить ввести 1–3 з них), далі — шукати мечі (retelling) або скриню й місця лиса.

## Вікна, меню, HUD
- `dialogue-window` — розмова з Faux Commander в Idyllshire: вхід у мінігру, обмін листків.
- `game-screen`: дошка 6×6 з ілюстраціями, лічильник ходів (`uncover-counter`).
- `end-screen` (?) — підсумок спроби з листками.
- `shop-window` — обмін Faux Leaves на нагороди (маунти, мініони, частина — лише звідси).
- `achievements-window` (загальна система гри): Friend or Faux I–IV — 1, 5, 20, 50 ігор; титули «Partner in Teatime», «Vrai Ami / Vraie Amie».

## Фічі поза полем
- Доступ раз на тиждень за пройдений unreal-трайл (`weekly-challenge`), retelling — додаткова спроба (≤1 на тиждень).
- Розблокування квестом «Fantastic Mr. Faux» (рівень 80, Idyllshire).
- `achievements` і титули.
- Спільнотні інструменти: таблиця всіх патернів і місць лиса, веб-розвʼязувач з порадою «яку панель відкрити».

## Варіації й родичі
- [battleship](battleship.md) — сховані прямокутні фігури й постріли без чисел; [voltorb-flip](voltorb-flip.md) — інша мінігра-«сапер» у великій RPG з нагородою-валютою; [minesweeper](minesweeper.md) — числа замість патернів.
- Інші мінігри FFXIV з прихованим полем — Mini Cactpot (3×3 числа, 4 відкриття) (?).
- Осі варіацій: **підказка** — числа / відгук «влучив/мимо» / лише видимі блоки + скінченна бібліотека розкладок (тут); **бюджет** — до перемоги / N відкриттів (11); **нагорода** — за знищення всіх / за кожну фігуру, менша — дорожча.

## Цікавинки для курсу
- Дедукція по скінченній бібліотеці патернів: фільтр кандидатів після кожного відкриття — 📎.
- Розвʼязувач «мінімум середньої кількості ходів по всіх шляхах» (перебір станів) — 🥇.
- Вибір стратегії «мечі заради retelling проти лиса за 100» як очікувана цінність — 🥉.
- Генератор: патерн блоків × поворот + розкладка трьох фігур без накладань і з фіксованими місцями лиса — 📎.
- Тижневий доступ і бонусна спроба як мета-обмеження — 🌱.

## Мапа на каталог
- Є: `cell-click` ↔ відкриття; `move-limit` ↔ 11 ходів; `event-points` ↔ листки за фігури; `level-solver` ↔ спільнотний розвʼязувач; `shop-window` ↔ обмін листків; `achievements-window`; `game-screen`.
- Корпус уже пропонує: `+shape-bank` (набір фігур, кожна рівно раз), `+pattern-library`.
- **Нема** → пропозиції карток:
  - `+fixed-pattern-deduction` «Розкладка з відомого скінченного списку; видимі блоки й відкриття фільтрують кандидатів» · game-logic/constraints · 📎.
  - `+weekly-attempt` «Одна спроба на тиждень + бонусна» · levels/bank · 🌱.
  - `+expected-moves-solver` «Порада ходу за мінімумом середньої кількості ходів» · levels/solvability · 🥇.

## Пропозиції до словників
- `+trigger:shape_uncovered` — усі клітини прихованої фігури відкрито (Faux Hollows, «потоплено» в Battleship).
- `+cond:pattern_candidates` — скільки розкладок ще сумісні з відкритим (для порад і автопозначок).
- `+ui:uncover-counter` — лишилось відкриттів (не `move-counter`: рахує вниз від ліміту).
- `+feature:weekly-challenge` — доступ раз на тиждень із бонусною спробою (уже пропонований корпусом).
- `+card:fixed-pattern-deduction`, `+card:weekly-attempt`, `+card:expected-moves-solver` — див. «Мапа на каталог».

## Джерела
- ⭐ [Console Games Wiki: Faux Hollows](https://ffxiv.consolegameswiki.com/wiki/Faux_Hollows) — 6×6, 5 заблокованих, 4 патерни з поворотами (16), 11 відкриттів, таблиця фігур і листків, retelling, доступ і скидання щовівторка, розблокування, досягнення.
- [Faux Hollows solver](https://faux.joshuaen.com) — розвʼязувач на даних u/Ylandah.
- [GitHub: ffxiv-faux-hollows](https://github.com/JoshuaEN/ffxiv-faux-hollows) — README («11 moves», 1–3 блоки визначають патерн, 4 місця лиса на патерн, шанси стратегій), `docs/solve-methods` (фігури 2×3/2×2/1×1, блоки не перекриваються), `tile-states.ts` (Unknown/Empty/Blocked/Present/Sword/Fox), `NOTES.md` (порожня панель — змарнований хід).
- [Таблиця спільноти](https://docs.google.com/spreadsheets/d/1mUyCzlzDmdXMwaSTUgWXtEA45oJNn-iB4_bVM43zf58/edit#gid=49331949) — патерни й місця Commander (лінк зі сторінки вікі; не відкривалась).
- [Console Games Wiki: Patch 5.3](https://ffxiv.consolegameswiki.com/wiki/Patch_5.3) — 11.08.2020, Faux Hollows у списку нового контенту.

## Непевне
- (?) Чи листки дають лише за повністю відкриту фігуру — вікі пише «uncover illustrations and earn faux leaves» без уточнення; розвʼязувач цілиться в повне відкриття.
- (?) Як часто лис є на полі: вікі — «рідко зʼявляється», розвʼязувач рахує 4 місця на кожен патерн і ~95 % шанс «мечі + лис».
- (?) Чи гра сама показує решту поля після 11-го ходу та як виглядає екран підсумку.
- (?) Mini Cactpot як родич — з памʼяті, не перевірено.
- Клас фігур `object` умовний: це нерухомі сховані цілі, як кораблі в Battleship.
