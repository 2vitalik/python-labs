---
title: Met Mag (Jikai Shōnen Met Mag)
slug: met-mag
aka: [磁界少年メット・マグ, Jikai Shounen Mettomag, Magnetic Boy Met Mag, 磁界少女マット・メグ, Jikai Shōjo Matto Meg]
family: grid-platformer
also: [push-slide]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: none
  goal: collect
year: 1987
platforms: [Famicom Disk System]
links:
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/%E7%A3%81%E7%95%8C%E5%B0%91%E5%B9%B4%E3%83%A1%E3%83%83%E3%83%88%E3%83%BB%E3%83%9E%E3%82%B0", best: true, note: "Mag (N) / Meg (S), чипи перевертають полюс, усі чипи — вихід, магнітні блоки притягують/відштовхують, транспортери, магнетит, вороги знімають очки"}
  - {kind: other, url: "https://gamesdb.launchbox-app.com/games/details/43236-jikai-shounen-met-mag", note: "опис: сфери міняють полюс червоний ↔ синій, стрілки кольору полюса"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Jikai+Shounen+Met+Mag+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 35
mechanics: [item-pickup, collect-all, reach-exit, key-and-door, teleport, event-points, sequential-levels, character-select, save-progress, +polarity-flip, +magnetic-attract-repel, +enemy-costs-points, +bonus-stage, +gender-select-same-rules]
proposes: ["+cond:same_pole", "+effect:attract", "+effect:repel", "+effect:flip_pole", "+card:polarity-flip", "+card:magnetic-attract-repel"]
author: opus
date: 2026-11-09
---

# Met Mag — хлопчик-магніт збирає чипи, кожен з яких перевертає його полюс, а магнітні блоки довкола притягують чи відштовхують його за цим полюсом

## Суть
Головоломка Thinking Rabbit (автори Sokoban) для Famicom Disk System під маркою DOG. Герой має магнітний полюс: Mag починає з N, героїня Meg — з S. Кожен підібраний чип перевертає полюс, а магнітні блоки на стадії притягують або відштовхують героя залежно від того, однакові полюси чи різні; цим рухають блоки й запускають механізми. Зібрав усі чипи — відчинився вихід.

## Поле і час
- Стадії-кімнати; за пошуковим описом StrategyWiki — 100 кімнат (?).
- Вид (збоку з гравітацією чи згори) у відкритих джерелах не названо (?) — тому `also: [push-slide]`.
- Real-time (вороги рухаються) (?).
- Дві «шкірки» однієї гри: Mag — наукова фантастика (ліфти, транспортери матерії), Meg — фентезі (чарівні дзеркала, двері); правила, стадії й сейв спільні.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Mag / Meg | player | полюс N або S | рух; полюс визначає взаємодію з усім магнітним |
| Маг-чип (сфера) | pickup | — | підібрав — полюс героя перевертається; усі зібрані — вихід відчинено |
| Магнітний блок | object | полюс | з героєм: притягання або відштовхування за поєднанням полюсів |
| Стрілка (за LaunchBox) | terrain | колір полюса, напрям | герой того самого кольору намагнічується; ефект залежить від напрямку стрілки (?) |
| Транспортер матерії / чарівні двері | static | реагує на полюс | переносить (?) залежно від полюса, як герой і блоки |
| Магнетит / Hiroyuki | object | магнітний | взаємодіє з героєм і блоками за полюсом |
| Ворог | enemy | вигляд різний у Mag і Meg | дотик не вбиває, а знімає очки |
| Вихід | gate | закритий / відкритий | відчиняється, коли зібрано всі чипи |
| Бонус-предмет | pickup | лише на бонусній стадії | +очки |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `level_start` → ЯКЩО `mode(mag)` → ТО `set_state(hero, pole_N)`; ЯКЩО `mode(meg)` → ТО `set_state(hero, pole_S)`.
- КОЛИ `picked(hero, chip)` → ЯКЩО `state(hero, pole_N)` → ТО `set_state(hero, pole_S)`; інакше `set_state(hero, pole_N)`.
- КОЛИ `custom: «герой поруч / на лінії з магнітним блоком»` (?) → ЯКЩО `same(hero, block, pole)` → ТО `custom: «відштовхування»`; інакше `custom: «притягання»`.
- КОЛИ `custom: «спрацювало притягання чи відштовхування»` → ТО `custom: «зсувається блок або сам герой; так запускаються механізми»` — хто саме рухається, джерела не уточнюють (?).
- КОЛИ `enter(hero|block, transporter)` → ЯКЩО `custom: «полюс підходить»` (?) → ТО `teleport` (?).
- КОЛИ `custom: «магнетит поруч із героєм чи блоком»` → ТО `custom: «притягується чи відштовхується за полюсом»`.
- КОЛИ `contact(hero, enemy)` → ТО `score(-n)` — не промах.
- КОЛИ `all_gone(chip)` → ТО `custom: «вихід відчинено»`.
- КОЛИ `enter(hero, exit)` → ЯКЩО `custom: «вихід відчинено»` → ТО `next_level`.
- КОЛИ `custom: «пройдено певну кількість стадій»` → ТО `custom: «вставляється бонусна стадія»`; КОЛИ `picked(hero, bonus_item)` → ТО `score(+n)`.
- Перемога стадії: усі чипи → вихід · Поразка: «промахи» і їхні причини не описані (?) · Рахунок: мінус за ворогів, плюс за бонус-предмети.

## Керування і ввід
- Геймпад Famicom; призначення кнопок у джерелах нема (?).

## Вікна, меню, HUD
- `character-select`: «Магнітний хлопчик Мет Маг» або «Магнітна дівчинка Мат Мег» — та сама гра, різний вигляд.
- `game-screen`: стадія, очки (?), полюс героя (?).
- Бонусна стадія — окремий тип стадії між звичайними.

## Фічі поза полем
- Спільний сейв обох версій (`save-progress`) на дискеті FDS.
- Вибір героя чи героїні — новинка для 1987 року (LaunchBox); на геймплей не впливає.

## Варіації й родичі
- Родичі в корпусі: `push-slide/kye` (магніти тягнуть блоки), [quadrax](quadrax.md); Thinking Rabbit — `push-slide/sokoban`.
- Осі варіацій: **хто рухається від магнітизму** (блок / герой / обидва); **як змінюється полюс** (підібраний предмет / кнопка / клітина); **ціна дотику ворога** (смерть / мінус очки).

## Цікавинки для курсу
- Полюс героя як стан, що перевертається кожним чипом: порядок збору — частина головоломки — 📎.
- Притягання / відштовхування блоків за порівнянням полюсів — 🥉 (рух сутностей без поштовху).
- Вихід, що відчиняється після «зібрано все», + спільний сейв двох «шкірок» — 🌱.
- Ворог, що знімає очки замість життя, — 🌱.

## Мапа на каталог
- Є: `item-pickup` · `collect-all` · `reach-exit` · `key-and-door` (вихід за чипами) · `teleport` (транспортери) · `event-points` · `sequential-levels` · `character-select` · `save-progress`.
- **Нема** → пропозиції карток:
  - `+polarity-flip` «Предмет перевертає полюс героя» · entities/state · 📎.
  - `+magnetic-attract-repel` «Магнітне притягання і відштовхування за полюсами» · entities/move · 🥉.
  - `+enemy-costs-points` «Дотик ворога — мінус очки, не життя» · game-logic/score · 🌱.
  - `+bonus-stage` «Бонусна стадія кожні N стадій» · levels/progression · 🌱.
  - `+gender-select-same-rules` «Вибір героя/героїні без зміни правил» · interface/menus · 🌱.

## Пропозиції до словників
- `+cond:same_pole(a, b)` — полюси однакові (окремо від загального `same`, бо читається як магнітизм).
- `+effect:attract(a, b)` / `+effect:repel(a, b)` — зсув до/від магнітного джерела.
- `+effect:flip_pole(a)` — перевернути полюс.
- `+card:polarity-flip`, `+card:magnetic-attract-repel` — див. вище.

## Джерела
- ⭐ [Wikipedia JA: 磁界少年メット・マグ](https://ja.wikipedia.org/wiki/%E7%A3%81%E7%95%8C%E5%B0%91%E5%B9%B4%E3%83%A1%E3%83%83%E3%83%88%E3%83%BB%E3%83%9E%E3%82%B0) — Thinking Rabbit / DOG, 03.07.1987, дві версії з одними правилами і сейвом, полюси N/S, чипи, вихід, магнітні блоки, транспортери, магнетит, вороги знімають очки, бонусна стадія.
- [LaunchBox: Jikai Shounen Met Mag](https://gamesdb.launchbox-app.com/games/details/43236-jikai-shounen-met-mag) — DOG / Square, вибір статі, сфери міняють полюс червоний ↔ синій, стрілки.
- StrategyWiki «Jikai Shōnen Mettomag» — бачив лише фрагмент у пошуку (100 кімнат, «сфери полюсу» перед виходом); сторінка віддає 403.
- YouTube: пошук «Jikai Shounen Met Mag gameplay».

## Непевне
- (?) Вид і гравітація: чи це платформер (`grid-platformer`), чи вид згори (`push-slide`) — у відкритих джерелах не сказано; сімʼю лишено за чергою.
- (?) Хто рухається від магнітизму — блок, герой чи обидва; на яку відстань діє магніт.
- (?) Стрілки LaunchBox і магнітні блоки JA-вікі — можливо, одна сутність, описана по-різному.
- (?) Як працюють транспортери; є «промахи» й життя чи лише очки; кількість стадій (100 — з пошукового фрагмента StrategyWiki).
- (?) Видавець: JA-вікі — DOG (Disk Original Group), LaunchBox і StrategyWiki — Square (DOG був маркою Square).
- Описано мало: coverage низький, бо відкриті джерела дають лише ядро правил.
