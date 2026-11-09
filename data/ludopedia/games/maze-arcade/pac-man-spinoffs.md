---
title: Pac-Man spin-offs (Pac & Pal, Baby Pac-Man, Mega Tunnel Battle)
slug: pac-man-spinoffs
aka: [Pac & Pal, Pac-Man & Chomp Chomp, Baby Pac-Man, Pac-Man Mega Tunnel Battle, Mega Tunnel Battle Chomp Champs]
family: maze-arcade
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: hidden
  random: runtime
  goal: collect
year: 1982
platforms: [arcade, Google Stadia, Switch, PC, PS4, PS5, Xbox Series]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Pac_%26_Pal", best: true, note: "карти-перевертні, Міру несе предмети в центр, промінь-оглушення, бонус-етап з картами"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Baby_Pac-Man", note: "лабіринт без енерджайзерів + фізичний пінбол під екраном"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Pac-Man_Mega_Tunnel_Battle", note: "до 64 гравців, свій лабіринт у кожного, Stadia → Chomp Champs"}
  - {kind: other, url: "https://gamingtrend.com/wakka-wakka-on-the-wild-side-pac-man-mega-tunnel-battle-review/", note: "огляд MTB: ворота між лабіринтами, «шторм», бонуси, глядачі"}
  - {kind: other, url: "https://siliconera.com/?p=1028009", note: "огляд Chomp Champs: ворота закриваються, життя, режими"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=pac+%26+pal+arcade+gameplay", note: "пошук; Pac & Pal"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=baby+pac-man+pinball+gameplay", note: "пошук; Baby Pac-Man"}
stage: v1
coverage: 60
mechanics: [move-auto, collect-all, item-pickup, touch-death, temporary-modes, projectile-shot, mode-indicator, event-points, sequential-levels, progress-acceleration, online-multiplayer, ai-opponent, realtime-ai, +flip-card-reveal, +item-thief-race, +stun-beam, +hiding-zone, +bonus-card-stage, +video-pinball-hybrid, +mode-earns-powerups, +chute-switch-mode, +own-maze-per-player, +gate-between-fields, +storm-score-cut, +spectator-gives-items, +eat-rival-when-powered]
proposes: ["+trigger:flip", "+effect:stun_beam", "+role:thief", "+ui:card-row", "+window:pinball-table", "+feature:spectator-powerups", "+axis:input-hardware", "+card:item-thief-race", "+card:video-pinball-hybrid"]
author: opus
date: 2026-11-09
---

# Pac-Man spin-offs — три відгалуження класики: карти й суперниця-злодійка, пінбол замість енерджайзерів, 64 лабіринти з воротами

## Суть
Базова механіка — у `pac-man.md` (лабіринт, привиди, енерджайзер). Цей файл описує лише те, що три відгалуження **змінили**. Pac & Pal (1983) прибирає «зʼїсти все»: треба перевертати карти й встигати зʼїдати відкриті предмети раніше, ніж їх утягне в центр нейтральна Міру. Baby Pac-Man (1982) ховає енерджайзери в справжній пінбол під екраном: зайдеш у жолоб унизу лабіринту — гра переходить на стіл із кулькою. Mega Tunnel Battle (2020) — королівська битва до 64 гравців, де в кожного свій лабіринт, а ворота між лабіринтами час від часу відчиняються.

### Що змінено відносно Pac-Man
| Гра | Поле | Що треба зібрати | Енерджайзер | Новий актор | Кінець рівня / партії |
|---|---|---|---|---|---|
| Pac-Man | 1 лабіринт | усі точки | 4 на рівень, привиди сині — їх їдять | — | точки скінчились |
| Pac & Pal | 1 лабіринт з картами | усі **предмети** за картами | 2 карти «S»: Пекмен синіє, кнопка стріляє променем, що **оглушує** привидів | Міру — несе предмети в центр, нешкідлива | предметів не лишилось |
| Baby Pac-Man | лабіринт + фізичний пінбол | точки | на старті **0**; заробляються мішенями пінбола | кулька, фліпери | як Pac-Man; жолоби в пінбол знову відкриваються після очищення лабіринту або втрати життя |
| Mega Tunnel Battle | до 64 лабіринтів, по одному на гравця | очки (точки, привиди, фрукти) | їсти привидів **і** непосилених суперників поруч | інші гравці, бонуси-предмети | останній живий; «шторм» відсікає найменші рахунки |

## Поле і час
- **Pac & Pal:** один лабіринт; замість точок — розкладені «сорочкою догори» карти; за картою відкривається предмет за дверцятами. Під центральною коробкою — помаранчева зона: привиди там повільніші, а Пекмен і привиди в ній невидимі (видно лише очі привидів).
- **Baby Pac-Man:** 13-дюймовий екран над укороченим горизонтальним пінбол-столом. Внизу лабіринту — два вертикальні жолоби: вхід у жолоб ставить відео на паузу і передає гру на стіл. Аутлейнів нема — кулька губиться лише між фліперами.
- **Mega Tunnel Battle:** у кожного гравця свій лабіринт; з часом відчиняються ворота в сусідні лабіринти (можуть різко зачинитись і замкнути). Очищений лабіринт перезаповнюється, а Пекмен і привиди пришвидшуються. Таймер «шторму» підганяє раунд.
- Усі три — real-time.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Пекмен | player | — | як у `pac-man.md`: безперервний рух, ввід змінює напрям |
| Карта (Pac & Pal) | switch | лицем донизу / відкрита | наїзд перевертає → відмикає предмет за дверцятами |
| Предмет (Galaxian, Rally-X, труба, сніговик, міні-Пекмен) | pickup | вигляд косметичний | однаковий ефект — очки; зникає, якщо Міру донесе його в центр |
| Карта «S» (Pac & Pal) | pickup | 2 на лабіринт | Пекмен синіє й росте, кнопка — промінь |
| Промінь (Pac & Pal) | projectile | — | оглушує привида на короткий час |
| Міру / Mil (Pac & Pal) | neutral | — | бере відкритий предмет і несе до центральної коробки; Пекмен проходить крізь неї |
| Помаранчева зона (Pac & Pal) | zone | — | сповільнює привидів, ховає Пекмена й привидів |
| Привиди | enemy | — | дотик неоглушеного → −1 життя |
| Бонус-карти (Pac & Pal, бонус-етап) | pickup | 8 «$», 1 Міру, 1 Блінкі | «$» — очки; Міру ×2; Блінкі — кінець етапу |
| Точка (Baby, MTB) | pickup | — | як у Pac-Man |
| Жолоб (Baby) | gate | відкритий / закритий | вхід → режим пінбола; після втрати кульки закривається |
| Кулька й фліпери (Baby) | object | фізика пінбола | мішені дають енерджайзери, нові фрукти, швидкість тунелів |
| Енерджайзер (Baby) | pickup | 0 на старті | зʼявляється в лабіринті за мішені пінбола |
| Інший гравець (MTB) | enemy | посилений / ні | у своєму або чужому лабіринті; посилений їсть непосилених |
| Ворота між лабіринтами (MTB) | gate | відчинені / зачинені | періодично відчиняються, можуть зачинитись з гравцем усередині |
| Бонус-предмет (MTB) | pickup | можна притримати | прискорення, «запах» — привиди тікають, «запаморочення» — завмирання ворогів, деякі — погані |
| Фрукт (MTB) | pickup | дорожчає | періодичний бонус очок |

## Правила (КОЛИ → ЯКЩО → ТО)
Pac & Pal:
- КОЛИ `enter(pac, card)` → ТО `reveal(card)`, `custom: «відмикає предмет за дверцятами»` (`+trigger:flip`).
- КОЛИ `contact(pac, item)` → ТО `pickup`, `score(n)`.
- КОЛИ `spawned(item)` → ТО `custom: «Міру бере предмет і несе до центральної коробки»`; КОЛИ `reach(miru, center_box)` → ТО `disappear(item)`.
- КОЛИ `contact(pac, miru)` → ТО `custom: «проходить крізь, без наслідків»`.
- КОЛИ `contact(pac, s_card)` → ТО `set_state(pac, powered, t)`, `transform(pac → big_blue)`.
- КОЛИ `input(button)` → ЯКЩО `state(pac, powered)` → ТО `spawn(beam)`; КОЛИ `contact(beam, ghost)` → ТО `stun(ghost, n)`.
- КОЛИ `contact(pac, ghost)` → ЯКЩО `not state(ghost, stunned)` → ТО `lives(−1)`.
- КОЛИ `enter(ghost, orange_zone)` → ТО `speed(ghost, −)`, `hide(pac, ghost)` (видно очі привидів).
- КОЛИ `all_gone(item)` → ТО `next_level`; ЯКЩО `counter(items_lost_to_miru, ==, 0)` → ТО `score(bonus)`.
- Бонус-етап (рівень 3 і кожен 4-й після): КОЛИ `enter(pac, card)` → ТО `reveal(card)`: «$» — `score(n)`; Міру — `multiplier(×2)`; Блінкі — `custom: «етап закінчується одразу»`, ЯКЩО `count(hidden_cards, ==, 0)` → `score(bonus)`.
Baby Pac-Man:
- КОЛИ `enter(pac, chute)` → ЯКЩО `state(chute, open)` → ТО `custom: «відео на паузі, гра переходить на пінбол»` (`window(+pinball-table)`).
- КОЛИ `contact(ball, target)` → ТО `counter(energizers, +1)` | `custom: «новий фрукт»` | `speed(pac_in_tunnel, +)` — переносяться в лабіринт.
- КОЛИ `custom: «кулька впала між фліперами»` → ТО `window(game-screen)`, `set_state(chutes, closed)`.
- КОЛИ `all_gone(dot)` або `died(pac)` → ТО `clear_state(chutes, closed)`.
- КОЛИ `counter(lives, ==, 0)` → ТО `game_over`.
Mega Tunnel Battle:
- КОЛИ `all_gone(dot)` (свій лабіринт) → ТО `custom: «лабіринт перезаповнюється»`, `speed(pac+ghosts, +)`.
- КОЛИ `contact(pac, power_pellet)` → ТО `set_state(pac, powered, t)`, `set_state(ghosts, frightened)`, `custom: «найближчі непосилені суперники вразливі»`.
- КОЛИ `contact(pac_a, pac_b)` → ЯКЩО `state(pac_a, powered) and not state(pac_b, powered)` → ТО `custom: «B зʼїдено»` (−життя / вибування).
- КОЛИ `timer(gates)` → ТО `set_state(gates, open)`; потім `set_state(gates, closed)` — хто не встиг, лишається в чужому лабіринті.
- КОЛИ `timer(storm)` → ЯКЩО `custom: «вибуло замало гравців»` → ТО `custom: «вибувають гравці з найменшими очками»`; лабіринти вибулих стираються.
- КОЛИ `contact(pac, powerup)` → ТО `pickup` (можна притримати), `use` → `speed` / `custom: «привиди тікають»` / `stun(rivals+ghosts, n)`.
- Перемога: Pac & Pal, Baby — рекорд очок; MTB — останній живий (Elimination) або місце в таблиці (Ranked). Поразка: життя скінчились / зʼїли.

## Керування і ввід
- **Pac & Pal:** 4-позиційний джойстик + **одна кнопка** (промінь, лише посиленим).
- **Baby Pac-Man:** джойстик для лабіринту, дві кнопки фліперів для пінбола; плунжер (?). До 2 гравців по черзі.
- **Mega Tunnel Battle:** геймпад/клавіатура онлайн; кнопка використати притриманий бонус (?).

## Вікна, меню, HUD
- Pac & Pal: `game-screen` — лабіринт з картами, рядок предметів рівня (`+ui:card-row`) (?); `attract-demo`; бонус-етап — окремий екран з 10 картами.
- Baby Pac-Man: `game-screen` (відео) + `+window:pinball-table` (фізичний стіл, табло на кабінеті); перехід відео ↔ стіл через жолоб/зливання кульки.
- MTB: `main-menu` → `mode-select` (Elimination / Ranked / Challenge / практика (?)) → `lobby-window` → `game-screen` (свій лабіринт, таймер шторму, кількість живих, слот бонусу) → `end-screen` (місце, XP); `shop-window` / `avatar-picker` — косметика (капелюхи, окуляри, теми лабіринтів); режим глядача — вид на все поле згори.

## Фічі поза полем
- Pac & Pal: бонус-етапи як ритм рівнів.
- Baby Pac-Man: прогрес енерджайзерів/фруктів/тунелів переноситься між режимами — `meta-progression` у межах партії.
- MTB: `online-multiplayer` до 64 · `+feature:spectator-powerups` — глядачі обирають, які бонуси зʼявляться гравцю · `xp-level` + `unlockables` (косметика за валюту) · Challenge-режим з цілями («зʼїж 5 привидів», «вторгнись у 3 лабіринти») · Ranked-таблиця. Stadia-версію закрито 2023; Chomp Champs (2024) закрито наприкінці 2025.

## Варіації й родичі
- Pac & Pal → Pac-Man & Chomp Chomp (північноамериканська версія Midway з собакою з мультфільму замість Міру, не вийшла).
- MTB → Chomp Champs (2024, мультиплатформа, система життів).
- Родичі в корпусі: `pac-man` (база), `super-pac-man` (ключі й двері замість точок — інша заміна «що збирати»), `pac-man-battle-royale` (посилений їсть суперників на одному полі), `pac-man-256`, `pac-man-championship-edition` (перезаповнення й прискорення).
- **Осі варіацій «що змінити в Pac-Man»:** ціль збору (точки / предмети за картами / ключі); джерело посилення (на полі / заробляється в іншому режимі); дія посилення (їсти / оглушувати / їсти суперників); суперник за предмети (нема / NPC-злодій / інші гравці); кількість полів (1 / по одному на гравця з воротами).

## Цікавинки для курсу
- Карти-перевертні: збір через «відкрий → встигни взяти» — 📎.
- NPC-злодій, що несе відкритий предмет до бази, — гонка з нейтральним агентом — 🥉.
- Посилення як дальня зброя-оглушувач замість «їсти» — 📎.
- Зона, що ховає сутностей і сповільнює ворогів — 🌱.
- Два режими гри, що обмінюються ресурсами (відео ↔ пінбол), — 🥉 (перемикання сцен зі збереженням стану).
- Кілька полів з воротами, що періодично відчиняються, — 🥈 (мультиполе, переходи між лабіринтами).
- «Шторм» відсікає найменші рахунки — 📎.

## Мапа на каталог
- Є: `move-auto` · `collect-all` (предмети / точки) · `item-pickup` · `touch-death` · `temporary-modes` (посилення) · `projectile-shot` (промінь) · `mode-indicator` · `event-points` · `sequential-levels` (бонус-етапи) · `progress-acceleration` (MTB) · `online-multiplayer` · `ai-opponent` + `realtime-ai`.
- **Нема** → пропозиції карток:
  - `+flip-card-reveal` «Карта відкривається наїздом» · entities/interact · 📎.
  - `+item-thief-race` «NPC несе предмет на базу — встигни раніше» · entities/move · 🥉.
  - `+stun-beam` «Промінь-оглушувач» · entities/combat · 📎.
  - `+hiding-zone` «Зона ховає сутностей» · interface/render · 🌱.
  - `+bonus-card-stage` «Бонус-етап з картами і стоп-картою» · levels/progression · 🌱.
  - `+video-pinball-hybrid` «Другий режим гри заробляє бонуси для першого» · game-logic/economy · 🥉.
  - `+mode-earns-powerups` «Посилення заробляються поза полем» · game-logic/economy · 📎.
  - `+chute-switch-mode` «Вхід у клітину перемикає режим гри» · interface/menus · 📎.
  - `+own-maze-per-player` «У кожного гравця своє поле» · game-logic/opponent · 🥉.
  - `+gate-between-fields` «Ворота між полями гравців» · levels/progression · 🥈.
  - `+storm-score-cut` «Вибування найменших рахунків за таймером» · game-logic/lose · 📎.
  - `+spectator-gives-items` «Глядачі обирають бонуси гравцю» · game-logic/opponent · 🥉.
  - `+eat-rival-when-powered` «Посилений їсть суперників» (уже запропонована в `pac-man-battle-royale.md`).

## Пропозиції до словників
- `+trigger:flip` — сутність перевернуто/відкрито наїздом (карта); можна виразити `enter` + `reveal`, але подія потрібна для ланцюгів.
- `+effect:stun_beam` — постріл, що оглушує, а не вбиває (можна `spawn(beam)` + `stun`; лишаю як кандидат на складене слово).
- `+role:thief` — NPC, що забирає предмети з поля (Міру; злодій у Chip's Challenge забирає з інвентаря).
- `+ui:card-row` — рядок відкритих/лишених предметів рівня.
- `+window:pinball-table` — окремий режим-сцена з іншою фізикою.
- `+feature:spectator-powerups` — глядачі впливають на гру.
- `+axis:input-hardware` — фізичні елементи кабінету (фліпери, кулька) поряд з екраном.
- `+card:item-thief-race`, `+card:video-pinball-hybrid` — див. вище.

## Джерела
- ⭐ [Wikipedia: Pac & Pal](https://en.wikipedia.org/wiki/Pac_%26_Pal) — карти, предмети, Міру, «S»-карти і промінь, помаранчева зона, бонус-етап, Chomp Chomp, ~300 автоматів.
- [Wikipedia: Baby Pac-Man](https://en.wikipedia.org/wiki/Baby_Pac-Man) — жолоби, мішені пінбола (енерджайзери, фрукти, тунелі), злив між фліперами, ~7000 автоматів.
- [Wikipedia: Pac-Man Mega Tunnel Battle](https://en.wikipedia.org/wiki/Pac-Man_Mega_Tunnel_Battle) — 64 гравці, свої лабіринти, посилення проти суперників, дати й платформи.
- [GamingTrend: огляд MTB](https://gamingtrend.com/wakka-wakka-on-the-wild-side-pac-man-mega-tunnel-battle-review/) — перезаповнення й прискорення, ворота, шторм, бонуси, глядачі.
- [Siliconera: огляд Chomp Champs](https://siliconera.com/?p=1028009) — ворота закриваються, життя, Elimination/Ranked, косметика.
- YouTube: пошуки «pac & pal arcade gameplay», «baby pac-man pinball gameplay».

## Непевне
- (?) Чи є в лабіринті Pac & Pal звичайні точки, кількість життів, очки за предмети.
- (?) Скільки триває оглушення променем і чи можна їсти оглушених привидів.
- (?) Baby Pac-Man: розкладка мішеней, чи є плунжер, скільки енерджайзерів дає мішень.
- (?) MTB: оригінал (Stadia) — зʼїли = вибув; Chomp Champs — з життями; огляд Siliconera каже, що посилення діє лише у своєму лабіринті й що зʼїсти привида в чужому — смерть — суперечливо, не перевірено.
- (?) MTB: точна геометрія — сусідство лабіринтів сіткою чи довільне, тривалість відкритих воріт.
