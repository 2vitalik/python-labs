---
title: Mathable
slug: mathable
family: word-number
also: [board-digital]
klass: cursor
axes:
  field: square
  time: turn
  opponent: hotseat
  info: partial
  random: runtime
  goal: score
year: 1987
platforms: [board, Android, iOS]
links:
  - {kind: wiki, url: "https://fr.wikipedia.org/wiki/Mathable", best: true, note: "FR: повні правила — 14×14, 106 плиток, старт 1-2-3-4, операції з двома сусідами в лінію, червоні клітини, ×2/×3, подвійний збіг, бонус 50"}
  - {kind: play, url: "https://play.google.com/store/apps/details?id=com.wookydigital.mathable", note: "цифрова версія (Android)"}
  - {kind: other, url: "https://boardgamegeek.com/geeksearch.php?action=search&q=Mathable&objecttype=boardgame", note: "пошук BGG (не прочитано: 403)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=mathable+board+game+how+to+play", note: "пошук; правила й партія"}
stage: v1
coverage: 75
mechanics: [hot-seat, turn-enforcement, ai-opponent, drag-drop-piece, event-points, score-records, legal-move-highlight, no-moves-left, completion-detection, end-screen, game-screen, help-window, +tile-rack, +tile-bag-draw, +premium-squares, +bingo-bonus, +tile-exchange, +move-generator, +equation-placement, +operator-squares, +double-equation-bonus]
proposes: ["+trigger:input", "+trigger:turn_end", "+trigger:no_moves", "+cond:legal", "+cond:equation_holds", "+cond:cell", "+effect:score", "+effect:give", "+effect:pass_turn", "+effect:multiplier", "+role:tile", "+role:zone", "+ui:tile-rack", "+ui:score-preview", "+ui:tiles-left", "+ui:legal-move-highlight", "+window:mode-select", "+feature:ai-opponent-levels", "+axis:session"]
author: opus
date: 2026-11-02
---

# Mathable — Scrabble з числами: поклади плитку, що є результатом дії над двома сусідами в лінію

## Суть
Гравці по черзі викладають числові плитки з руки (7 штук) на поле 14×14. Плитку можна поставити лише в клітину одразу за двома вже викладеними плитками, що стоять у лінію по горизонталі чи вертикалі, і лише якщо її число — результат додавання, віднімання, множення або точного ділення цих двох. Очки — номінал плитки з множниками клітин; плитка, що замикає дві рівності одночасно, рахується двічі. Це арифметичний Scrabble: «слово» — рівність із трьох плиток, «словник» — чотири дії.

## Поле і час
- Квадрат 14×14; у центрі на старті чотири «віртуальні» плитки 1, 2, 3, 4 (квадрат 2×2) — уже викладені.
- Шари: клітини з типом (звичайна / ×2 / ×3 / червона з операцією) + плитки з числами.
- Покроково, 2–4 гравці (≈45 хв); хід = викласти будь-скільки плиток або пас з обміном.
- Інформація часткова: рука суперника й мішок приховані, поле відкрите.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Числова плитка 1–10 | tile | 7 копій кожної (70) | ставиться, якщо є рівністю з двома сусідами в лінію |
| «Особлива» плитка | tile | 0, 11–21, 24, 25, 27, 28, 30, 32, 35, 36, 40, 42, 45, 48, 49, 50, 54, 56, 60, 63, 64, 70, 72, 80, 81, 90 (36 шт.) | ті самі правила; великі значення — переважно добутки |
| Стартові 1·2·3·4 | tile | віртуальні, у центрі | точка росту поля; очок не дають |
| Клітина ×2 / ×3 | zone | множник | очки плитки ×2 / ×3 |
| Червона клітина-операція | zone | + − × ÷ | плитку можна покласти, лише якщо рівність саме з цією дією; бонусна плитка з мішка |
| Рука (стійка) | container | 7 плиток | поповнюється з мішка після ходу |
| Мішок | container | 106 плиток мінус викладені | тягнення наосліп |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(place tile, cell)` → ЯКЩО `free(cell)` і є дві плитки a, b у лінію, що закінчуються біля cell, і `equation_holds(tile ∈ {a+b, |a−b|, a×b, max/min якщо ділиться націло})` → ТО викласти; інакше `block`.
- Порядок двох сусідів не важить: після 3 і 9 можна 12, 6, 27 або 3; після 12 і 5 — 17, 7 або 60 (ділення неточне — ні).
- КОЛИ `input(place tile)` → ЯКЩО `cell(target, operator_square)` → ТО дозволена лише рівність з дією клітини; ЯКЩО виконано → ТО `give(player, extra tile)`.
- КОЛИ `after(place)` → ТО `score(value × cell_multiplier)`.
- КОЛИ `after(place)` → ЯКЩО плитка одночасно задовольняє рівність по горизонталі й по вертикалі → ТО `score` рахується двічі (40 між 5·8 і 64−24 = 80 очок).
- КОЛИ `custom: «за хід викладено всі 7 плиток»` → ТО `score(+50)` — бонус «Mathable».
- Хід може містити кілька плиток, кожна з яких окремо утворює рівність (може спиратися на щойно викладені) (?).
- КОЛИ `input(pass)` → ТО можна обміняти 1–7 плиток з мішком, `pass_turn`.
- КОЛИ `turn_end` → ТО `give(player, tiles until 7)` з мішка.
- КОЛИ `custom: «рука порожня і мішок порожній»` або `no_moves(all)` → ТО `game_over`.
- Перемога: найбільше очок · Поразка: менше · Рахунок: Σ номіналів викладених плиток з множниками, подвійними збігами й бонусом 50.

## Керування і ввід
- Настільна: викласти плитку з руки на клітину; суперники перевіряють рівності.
- Цифрова версія: drag плитки з руки на поле, підсвітка дозволених клітин (?), кнопки Play / Pass / Exchange (?).
- Черга ходів за годинниковою стрілкою; hotseat або проти AI у застосунку (?).

## Вікна, меню, HUD
- (цифрова версія) `game-screen`: поле 14×14 з кольоровими клітинами, `tile-rack`, рахунки гравців, `tiles-left`, `score-preview` ходу.
- (цифрова версія) `mode-select`: проти комп'ютера / hotseat (?) / онлайн (?).
- (цифрова версія) `confirm-dialog` обміну плиток, `end-screen` з рахунками, `help-window` з правилами й прикладами операцій.

## Фічі поза полем
- `hotseat` 2–4 гравці; (цифрова версія) `ai-opponent-levels` (?).
- Видання: Jumbo (1987), Bojeux (2007), Wooky Entertainment (2009); варіанти назви — Mixmath (?).
- Віковий ценз 9+ — гра використовується як навчальна (усна лічба, таблиця множення).

## Варіації й родичі
- Scrabble (рука 7, мішок, премійні клітини, бонус за всю руку), Equate і Numble (рівності з плиток-цифр і знаків) (?), Nerdle (Wordle для рівностей).
- Krypto / «24» (отримати ціль діями над числами) — та сама арифметика без поля.
- **Осі варіацій:** звідки береться «слово» (2 сусіди в лінію / вся лінія — рівність, як Equate) · дія (будь-яка з 4 / задана клітиною) · рахунок (номінал / номінал × довжина / фіксовано) · знаки як плитки чи як клітини.

## Цікавинки для курсу
- Перевірка легальності: для клітини знайти пари сусідів у 4 напрямках і множину допустимих результатів — 🌱.
- Червоні клітини-операції як обмеження поверх загального правила — 🌱.
- Подвійний збіг (горизонталь + вертикаль) і множники клітин у рахунку — 📎.
- Мішок з таблицею розподілу, рука 7, обмін — 📎 (повторює Scrabble).
- AI-генератор ходів: перебір усіх клітин × плиток руки, жадібно за очками, з ланцюжком кількох плиток за хід — 🥉 (жадібний) / 🥇 (послідовності плиток).
- Аналіз розподілу 106 плиток: які результати досяжні з 1–10 і чому в наборі саме ці «особливі» числа — 📎.

## Мапа на каталог
- Є: `hot-seat` · `turn-enforcement` · `ai-opponent` (цифрова) · `drag-drop-piece` ↔ плитки з руки · `event-points` ↔ номінал плитки · `score-records` · `legal-move-highlight` (цифрова (?)) · `no-moves-left` ↔ кінець без ходів · `completion-detection` ↔ рука й мішок порожні · `end-screen` · `game-screen` · `help-window`.
- **Нема** → пропозиції карток:
  - `+tile-rack`, `+tile-bag-draw`, `+premium-squares`, `+bingo-bonus`, `+tile-exchange`, `+move-generator` — див. scrabble.md.
  - `+equation-placement` «Плитка = результат дії над двома сусідами в лінію» · entities/legality · 📎 · слоти {ops: [+,−,×,÷], exact_div: true}.
  - `+operator-squares` «Клітина задає дозволену операцію» · entities/legality · 🌱 · слоти {layout: file}.
  - `+double-equation-bonus` «Подвійний рахунок за дві рівності одразу» · game-logic/score · 🌱.

## Пропозиції до словників
- `+trigger:input`, `+trigger:turn_end` (⏳), `+trigger:no_moves` (⏳).
- `+cond:legal` (⏳); `+cond:equation_holds` — число = результат дії над двома сусідами; `+cond:cell` (⏳) — клітина-операція.
- `+effect:score`, `+effect:give` (добір, бонусна плитка), `+effect:pass_turn`, `+effect:multiplier` (⏳).
- `+role:tile`, `+role:zone` — клітини ×2/×3/операція.
- `+ui:tile-rack`, `+ui:score-preview`, `+ui:tiles-left` (див. scrabble.md), `+ui:legal-move-highlight` (⏳).
- `+window:mode-select` (⏳).
- `+feature:ai-opponent-levels` (⏳).
- `+axis:session` — `match`.

## Джерела
- ⭐ [Wikipédia (FR): Mathable](https://fr.wikipedia.org/wiki/Mathable) — повні правила з прикладами, склад 106 плиток, спецклітини, кінець гри, видавці.
- [Google Play: Mathable](https://play.google.com/store/apps/details?id=com.wookydigital.mathable) — цифрова версія.
- [BGG: пошук Mathable](https://boardgamegeek.com/geeksearch.php?action=search&q=Mathable&objecttype=boardgame) — не прочитано (403).
- YouTube: пошук «mathable board game how to play».

## Непевне
- EN-статті нема, офіційний mathable.com не резолвився, BGG — 403, WebSearch вичерпано; основа — FR-Wikipedia.
- (?) Автор (Jean-Paul Lemay?) і назва Mixmath — з брифу/памʼяті, FR-вікі їх не згадує.
- (?) Розкладка клітин ×2/×3/операцій на полі; чи дають червоні клітини множник.
- (?) Чи можна за хід викласти кілька плиток з опорою на щойно викладені — вікі каже «скільки зможеш».
- (?) Чи віднімання й ділення справді не залежать від порядку сусідів (приклади вікі — 3,9 → 6 і 3 — це підтверджують, але формулювання «в порядку, як стоять»).
- (?) Режими цифрової версії (AI, онлайн), Equate/Numble як родичі.
