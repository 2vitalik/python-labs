---
title: Wetrix
slug: wetrix
aka: [Wetrix+]
family: falling-match
also: [build-sim]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: score
year: 1998
platforms: [N64, PC, Game Boy Color, Dreamcast]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Wetrix", best: true, note: "фігури Upper/Downer, вода, вогняні кулі, міни, лід, землетрус, злив-лічильник, режими, split-screen"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=wetrix+n64+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [gravity-fall, height-levels, piece-rotate-flip, keyboard-controls, event-points, combo-multiplier, score-records, difficulty-levels, mode-select, simultaneous-versus, garbage-attack, game-pause, end-screen, next-queue, +terrain-raise-lower, +water-flow-sim, +leak-meter-lose, +evaporate-for-points, +earthquake-flatten, +handicap-start]
proposes: ["+effect:raise(cells, n)", "+effect:lower(cells, n)", "+effect:flow(water)", "+trigger:leak(water, edge)", "+ui:drain-meter", "+ui:earthquake-meter", "+axis:field=heightmap", "+card:water-flow-sim"]
author: opus
date: 2026-11-09
---

# Wetrix — фігури будують рельєф на плиті, вода збирається в озера, вогонь випаровує її в очки; витік через край — програш

## Суть
На квадратну плиту-ландшафт падають фігури, але вони не складаються в ряди: Uppers піднімають рельєф (будують стінки), Downers опускають його. Зверху падає вода; якщо її не втримують стінки, вона витікає з країв у злив. Вогняні кулі випаровують озера — це головне джерело очок, міни пробивають дірки, лід заморожує воду. Повний злив — кінець гри; зависокий рельєф викликає землетрус, що його вирівнює.

## Поле і час
- Квадратна сітка-«висотна мапа» (heightmap) у 3D з ізометричним видом: кожна клітина має висоту землі і рівень води. Плита висить у повітрі — вода з краю стікає вниз у злив.
- Real-time: фігури й вода падають з неба; гравець зсуває й обертає тінь фігури над плитою до падіння. Pro-режим — швидший темп.
- Вода тече в нижчі сусідні клітини й заповнює западини, обмежені стінками (озера).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Upper | player | форма: прямокутник, квадрат, T | при падінні піднімає рельєф під собою; будує стінки озер |
| Downer | player | форма | опускає рельєф (знімає стінки, поглиблює) |
| Вода (бульбашки) | player | обсяг | падає в точку; тече вниз; за краєм — у злив |
| Вогняна куля (Fireball) | player | — | випаровує воду в озері; очки за обсяг; зменшує злив |
| Міна (Mine / bomb) | player | — | пробиває дірку в рельєфі |
| Кубик льоду (Ice Cube) | player | — | заморожує воду (лід) |
| Клітина рельєфу | terrain | висота | вода стоїть, якщо сусіди вищі |
| Озеро | zone | обсяг води | область води в западині; ціль вогняних куль |
| Злив (drain) | zone | рівень 0..max | наповнюється витеклою водою; повний → кінець гри |
| Землетрус | hazard | лічильник висоти | рельєф зависокий → землетрус швидко вирівнює ландшафт |
| Веселка | zone | — | зʼявляється при випаровуванні (?) — бонус/заливання річок |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(move)` → ТО `move(piece_shadow, dir)` над плитою; КОЛИ `input(rotate)` → ТО `rotate(piece, 90)`.
- КОЛИ `tick` → ТО `fall(piece)`; КОЛИ `input(drop)` → ТО `speed(piece, ×k)`.
- КОЛИ `contact(upper, terrain)` → ТО `custom: «raise — висота клітин під фігурою +1»`.
- КОЛИ `contact(downer, terrain)` → ТО `custom: «lower — висота клітин під фігурою −1»`.
- КОЛИ `contact(water, terrain)` → ТО `custom: «flow — вода розтікається в нижчих сусідів, доки рівень не вирівняється»`.
- КОЛИ `custom: «вода досягла краю плити без стінки»` → ТО `counter(drain, +volume)`.
- КОЛИ `counter(drain, ==, max)` → ТО `game_over`.
- КОЛИ `contact(fireball, lake)` → ТО `custom: «випаровує воду озера»`, `score(n)` за обсяг, `counter(drain, −n)`.
- КОЛИ `after(contact(fireball, lake))` → ЯКЩО `chain(n)` → ТО `multiplier(×k)` (?) — кілька способів рахунку й множників.
- КОЛИ `contact(mine, terrain)` → ТО `set_cell(cells, hole)`; вода тече в дірку → `counter(drain, +volume)` (?).
- КОЛИ `contact(ice_cube, lake)` → ТО `transform(water, ice)` — заморожена вода не тече (?).
- КОЛИ `counter(height, >, limit)` → ТО `custom: «землетрус — рельєф швидко вирівнюється»`.
- Versus: КОЛИ `custom: «рівень води в метрі на кольоровій зоні»` → ТО `send_garbage` — атака суперника відповідно до кольору (4 кольорові зони); випаровування озера вогнем цей метр не знижує.
- Перемога: нема (на очки) · Поразка: злив повний · Рахунок: за випаровану воду з множниками; таблиця рекордів.

## Керування і ввід
- Стік/хрестовина — переміщення тіні фігури над плитою; кнопки — поворот, прискорене падіння; камера/обертання плити (?).
- Вода й вогонь теж керовані: їх можна навести на потрібне озеро до падіння.

## Вікна, меню, HUD
- `main-menu` → `mode-select`: Classic · Pro · Practice · Challenges (1/5 хв, 100/500 фігур) · Handicap · 2P.
- `game-screen`: 3D-плита, тінь фігури, `next-piece-preview` (?), `score`, `custom: «drain-meter — злив-метр»`, `custom: «earthquake-meter»` (?), `multiplier`.
- `end-screen` → `leaderboard` (high-score список).
- `pause-menu`; split-screen у 2P.

## Фічі поза полем
- Режими: `mode-classic`, швидший Pro, `tutorial` (Practice — базові правила), `mode-time-attack` (1 і 5 хвилин), «вижити 100/500 фігур», `mode-versus` (split-screen 2 гравці).
- Handicap-старт: напівповний злив, шар льоду, піднята земля, випадкова земля, випадкові дірки (`custom-difficulty`).
- `leaderboard-local`.

## Варіації й родичі
- Wetrix+ (Dreamcast, 1999) — перевидання; Aqua Aqua (PS2, 2000) — сиквел без суттєвих змін ядра.
- Родичі: Tetris (падіння фігур), Tetrisphere (3D), будівельні симулятори з водою (From Dust; `build-sim`).
- **Осі варіацій**: що робить фігура (займає клітини / змінює висоту) · ціль (очистити ряди / втримати й випарувати воду) · поразка (стек до верху / витік у злив) · середовище (сухе / рідина).

## Цікавинки для курсу
- Висотна мапа + симуляція води «тече вниз, вирівнює рівень» на сітці — 🥈 (клітинний автомат рідини з обсягом).
- Пошук озер як басейнів (flood fill за рівнем води, «priority-flood») — 🥇.
- Злив-метр як «життя» гри з наповненням від витоку — 🌱.
- Фігура змінює поле (+1/−1 висоти) замість займати клітини — 📎.
- Землетрус за порогом висоти — 🌱.
- Ізометричний 3D-рендер висотної мапи — 🥉.

## Мапа на каталог
- Є: `gravity-fall` · `height-levels` (висота клітин) · `piece-rotate-flip` · `keyboard-controls` · `event-points` · `combo-multiplier` · `score-records` · `difficulty-levels` (Pro, handicap) · `mode-select` · `simultaneous-versus` · `garbage-attack` (кольоровий метр) · `game-pause` · `end-screen` · `next-queue`.
- **Нема** → пропозиції карток:
  - `+terrain-raise-lower` «Фігура піднімає/опускає рельєф» · entities/interact · 📎.
  - `+water-flow-sim` «Рідина на висотній мапі» · entities/move · 🥈 · слоти {flow_rate}.
  - `+leak-meter-lose` «Програш: метр витоку повний» · game-logic/lose · 🌱.
  - `+evaporate-for-points` «Очки за знищений обсяг» · game-logic/score · 🌱.
  - `+earthquake-flatten` «Вирівнювання за порогом висоти» · entities/state · 🌱.
  - `+handicap-start` «Гандикап-старт (зіпсоване поле)» · game-logic/difficulty · 🌱.

## Пропозиції до словників
- `+effect:raise(cells, n)` / `+effect:lower(cells, n)` — зміна висоти клітин (Wetrix; рельєф у build-sim).
- `+effect:flow(water)` — рідина розтікається за висотою (Wetrix, Powder Toy-подібні).
- `+trigger:leak(water, edge)` — рідина витекла за край поля.
- `+ui:drain-meter` — метр витоку/злива як життя (пор. `drop-meter` з Klax); `+ui:earthquake-meter` — шкала висоти до землетрусу.
- `+axis:field=heightmap` — сітка з висотою клітин (рельєф), без шарів-обʼєктів.
- `+card:water-flow-sim` — див. вище.

## Джерела
- ⭐ [Wikipedia: Wetrix](https://en.wikipedia.org/wiki/Wetrix) — Uppers (прямокутник, квадрат, T), Downers, вода, витік у злив, вогняні кулі (очки за випаровування, зменшують злив), міни, лід, землетрус, режими Classic/Pro/Practice/Challenges/Handicap, 2P з кольоровим метром, платформи, Zed Two, Aqua Aqua.

## Непевне
- (?) Числа: розмір плити, обсяги злива, пороги землетрусу, формули множників — не бачив.
- (?) Веселка — у Wikipedia лише підпис до картинки («заповнює річки»); її роль у рахунку не перевірено.
- (?) Качка: у Wikipedia лише 3D-модель гумової качки в розробці; чи є вона ігровою сутністю — не перевірено.
- (?) Лід: як замерзла вода поводиться далі (тане? блокує?), міна: чи вода в дірці йде в злив.
- (?) Як саме атакує суперника колір метра у 2P (що прилітає) — не описано.
- (?) Керування камерою, превʼю наступної фігури — з памʼяті.
