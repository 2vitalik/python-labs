---
title: Hands of Time (Final Fantasy XIII-2)
slug: hands-of-time
aka: [FFXIII-2 clock puzzle, Clock puzzle, Temporal Rift — The Hands of Time]
family: connect-rotate
also: [pencil-logic]
klass: puzzle
axes:
  field: graph
  time: static
  opponent: none
  info: full
  random: setup
  goal: collect
year: 2011
platforms: [PS3, Xbox 360, Windows]
links:
  - {kind: other, url: "https://ar5iv.arxiv.org/html/1203.1633", best: true, note: "N. Johnston, «The Complexity of the Puzzles of FFXIII-2»: формальні правила, граф, NP-повнота часткового варіанта"}
  - {kind: other, url: "https://njohnston.ca/2012/02/counting-and-solving-final-fantasy-xiii-2s-clock-puzzles/", note: "блог: правила, підрахунок розвʼязних годинників (OEIS A206344–6), MATLAB-розвʼязувач"}
  - {kind: other, url: "https://gamecreationblueprint.blogspot.com/2017/02/how-to-solve-final-fantasy-xiii-2.html", note: "фан-гайд: дві стрілки, таймер, стратегія старт/фініш"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Final_Fantasy_XIII-2", note: "гра загалом; темпоральні розломи з пазлами"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Final+Fantasy+XIII-2+Hands+of+Time+clock+puzzle", note: "пошук; проходження годинників"}
stage: v1
coverage: 75
mechanics: [wrap-edges, legal-move-highlight, visited-trail, no-moves-left, completion-detection, restart-level, time-out, level-solver, unsolvable-states, +jump-by-value, +hamiltonian-path, +solvable-generation]
proposes: ["+card:jump-by-value", "+card:hamiltonian-path", "+card:solvable-generation"]
author: opus
date: 2026-11-09
---

# Hands of Time — годинник із числами по колу: стань на число m, дві стрілки покажуть позиції на m уперед і назад; відвідай кожну позицію рівно раз

## Суть
У JRPG Final Fantasy XIII-2 (Square Enix, 2011) героїня й напарник подорожують епохами; у «темпоральних розломах» трапляються пазли, які треба розвʼязати, щоб розлом закрився: Hands of Time (годинник), Crystal Bonds і плиткові випробування (?). Тут витягнуто лише годинник. На циферблаті N чисел; гравець обирає стартове число m, після чого дві стрілки вказують на позиції за m кроків за годинниковою і проти неї — наступний крок лише на одну з них. Число, на яке стали, зникає; мета — пройти всі N позицій, жодну двічі. Математично це пошук гамільтонового шляху в орграфі, де з кожної вершини виходить не більше двох ребер.

## Поле і час
- Кільце з N вузлів (у грі N від 5 до 13 за Johnston; фан-гайд — 8–13); у кожному вузлі ціле від 1 до ⌊N/2⌋.
- Сусідство нестандартне: з вузла i з числом m — у (i+m) mod N та (i−m) mod N; кільце замкнене.
- Без тіків: кожен крок — дискретний вибір. На деяких годинниках вмикається таймер, щойно гравець стає на поле.
- Розлом складається з кількох годинників-етапів, що ростуть за розміром (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Циферблат | zone | N вузлів по колу | поле пазла |
| Вузол з числом | mark | m ∈ 1…⌊N/2⌋ | на нього можна стати, якщо на нього вказує стрілка; після кроку стає порожнім |
| Порожній вузол | mark | — | стати не можна |
| Дві стрілки | mark | крок m за / проти годинникової | показують два єдині легальні наступні вузли |
| Персонаж | player | — | стоїть на поточному вузлі, крокує на вибраний |
| Таймер (не на всіх) | mark | час | стартує з першим кроком на поле |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(step, node)` → ЯКЩО `first_time` → ТО `move(player, node)`, `set_state(node, empty)`, `custom: «стрілки стають на ±m від вузла»`.
- КОЛИ `input(choose, hand)` → ЯКЩО `not state(hand.target, empty)` → ТО `move(player, hand.target)`, `set_state(hand.target, empty)`, `custom: «m := число цього вузла, стрілки переставлено»`; інакше `block`.
- КОЛИ `custom: «стрілка переходить через 12-ту годину»` → ТО `wrap(hand)`.
- КОЛИ `no_moves(player)` → ЯКЩО `count(numbered_node, >, 0)` → ТО `lose`, `restart` (обидві стрілки на порожніх — заново).
- КОЛИ `all_gone(numbered_node)` → ТО `win`, `custom: «наступний годинник етапу або розлом закрито»`.
- КОЛИ `counter(time_left, ==, 0)` → ЯКЩО `count(numbered_node, >, 0)` → ТО `lose`.
- Перемога: кожну з N позицій вибрано рівно раз (N−1 крок після старту). Поразка: обидві стрілки на вже порожніх вузлах, коли ще лишились числа, або вийшов таймер.

## Керування і ввід
- Персонаж стає на будь-яке число — це старт; далі вибір лише з двох стрілок (стати на вузол, на який вона вказує).
- Повтор годинника — кнопкою на місці; фан-гайд радить на таймерних годинниках спершу переписати числа, а потім стартувати.

## Вікна, меню, HUD
- `game-screen` (сцена розлому): циферблат з числами, дві стрілки-підказки (`legal-move-highlight`), `timer-countdown` на таймерних годинниках.
- `end-screen` / повідомлення: годинник розвʼязано → наступний етап; розлом закрито → нагорода (фрагмент) (?).
- Решта вікон — спільні вікна RPG (меню, мапа), поза цим шаром.

## Фічі поза полем
- `restart-level` миттєвий повтор годинника; генерація годинників (за фан-гайдом — випадкова (?)).
- Нагорода за розлом — фрагмент колекції й доступ далі мапою (?).

## Варіації й родичі
- Варіант «не рівно m, а не більше m кроків» — гамільтонів шлях на графах кругових дуг, розвʼязний поліноміально (Damaschke 1993, Hung et al. 2009 — за статтею).
- «Часткові» годинники (частина вузлів порожня від початку) — NP-повні (зведення від гамільтонового шляху в орграфі з виходом 1–2, Plesník 1979).
- Корпус: [Hidato](../pencil-logic/hidato.md) (шлях 1…N через усі клітини) · [Knight's tour](../pencil-logic/n-queens-knights-tour.md) (гамільтонів шлях конем) · [LYNE](lyne.md) (один шлях через усі вузли фігури).
- Осі варіацій: **крок** — рівно m / до m · **напрями** — два (±m) / один · **поле** — кільце / сітка (Hidato) / шахівниця (тур коня) · **старт** — будь-який / заданий.

## Цікавинки для курсу
- Модель «кільце + число = два ребра» і перевірка ходу з `mod N` — 🌱.
- Розвʼязувач перебором з поверненням (N ≤ 13) — 📎; з евристиками «вузол без вхідних ребер — старт, без вихідних — фініш» — 🥉.
- Генератор лише розвʼязних годинників (перебір + відсів; для N = 9 розвʼязних 193995 з 262144) — 🥉.
- Підрахунок розвʼязних годинників з точністю до поворотів і віддзеркалень (OEIS A206346) — 🥈.
- Доведення/ілюстрація NP-повноти часткового варіанта через зведення — 👑.

## Мапа на каталог
- Є: `wrap-edges` (кільце) · `legal-move-highlight` (стрілки) · `visited-trail` (порожні вузли) · `no-moves-left` · `completion-detection` · `restart-level` · `time-out` · `level-solver` · `unsolvable-states` (замкнена петля до кінця).
- **Нема** → пропозиції карток:
  - `+jump-by-value` «Стрибок на число, записане в клітині» · entities/move · 🌱 · слот {dirs: ±}.
  - `+hamiltonian-path` «Відвідати кожну клітину рівно раз» · game-logic/win · 📎 — Hands of Time, Hidato, тур коня.
  - `+solvable-generation` «Генерація лише розвʼязних (не обовʼязково унікальних)» · levels/generation · 🥉.

## Пропозиції до словників
- `+card:jump-by-value`, `+card:hamiltonian-path`, `+card:solvable-generation` — див. «Мапа на каталог»; слова правил лягли у словник повністю.

## Джерела
- ⭐ [arXiv 1203.1633 (ar5iv)](https://ar5iv.arxiv.org/html/1203.1633) — формальні правила, модель орграфа, NP-повнота Partial Hands of Time, поліноміальний варіант «до m», відкриті питання; також Crystal Bonds.
- [Johnston: Counting and Solving FFXIII-2's Clock Puzzles](https://njohnston.ca/2012/02/counting-and-solving-final-fantasy-xiii-2s-clock-puzzles/) — N від 5 до 13, ⌊N/2⌋^N годинників, кількості розвʼязних, MATLAB `solve_clock.m`.
- [Фан-гайд (blogspot)](https://gamecreationblueprint.blogspot.com/2017/02/how-to-solve-final-fantasy-xiii-2.html) — дві стрілки, зникання чисел, повтор, таймер, евристики старту/фінішу.
- [Wikipedia: Final Fantasy XIII-2](https://en.wikipedia.org/wiki/Final_Fantasy_XIII-2) — гра, дати, платформи, розломи з пазлами.
- YouTube: пошук «Final Fantasy XIII-2 Hands of Time clock puzzle».

## Непевне
- (?) Чи годинники генеруються випадково (гайд gamerfuzion) чи задані вручну — не підтверджено.
- (?) Кількість етапів у розломі й розміри (гайд: 4 етапи «6, 8, 10, 12») і нагороди-фрагменти — з фан-гайдів, не перевірено.
- (?) Діапазон чисел: стаття — 1…⌊N/2⌋; фан-гайд — «від 1 до 6» при 8–13 числах; узгоджено, якщо N ≤ 13.
- (?) Складність оригінальної гри (без порожніх вузлів) — відкрите питання статті; NP-повним доведено лише частковий варіант. Черга писала «NP-складне» без уточнення.
- (?) Інші пазли розломів (Crystal Bonds, плитки) — не описані тут; Crystal Bonds за статтею розвʼязний поліноміально.
