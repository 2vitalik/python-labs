---
title: Graveyard Keeper
slug: graveyard-keeper
aka: [Доглядач цвинтаря]
family: build-sim
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: score
year: 2018
platforms: [PC, macOS, Linux, Xbox One, PS4, Switch, iOS, Android]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Graveyard_Keeper", best: true, note: "геймплей: розчистка цвинтаря, могили і церква дають дохід, дерево технологій з трьома видами досвіду, DLC"}
  - {kind: steam, url: "https://store.steampowered.com/app/599140/Graveyard_Keeper/", note: "опис: керування цвинтарем, переробка тіл, крафт, алхімія, етичні вибори"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Graveyard+Keeper+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 40
mechanics: [cell-click, multi-cell-size, coverage-area, inventory, round-currency, save-game, +layered-cell-score, +rating-sum, +corpse-quality, +grave-slots, +tech-tree-colors, +house-evolution]
proposes: ["+cond:slot_free", "+effect:add_quality", "+effect:decay", "+ui:skull-rating", "+ui:grave-tooltip", "+card:layered-cell-score", "+card:rating-sum"]
author: opus
date: 2026-11-09
---

# Graveyard Keeper — могила як клітина з шарами: тіло + огорожа + надгробок дають черепи якості, а сума — рейтинг цвинтаря

## Суть
Фермерсько-крафтова гра з чорним гумором: доглядач розчищає занедбаний цвинтар, приймає тіла, ховає їх і прикрашає могили, а рейтинг цвинтаря разом із церквою приносить дохід. Сітковий шар, який тут описано, — **ділянки могил**: кожна могила складається з шарів (тіло, огорожа, надгробок), кожен шар додає позитивні («білі») або відʼємні («червоні») черепи, а якість цвинтаря — їх сума (?). Решта гри — крафт-ланцюги, дерево технологій, квести, підземелля, DLC — фон.

## Поле і час
- Цвинтар — ділянка світу з місцями під могили; спершу її треба розчистити від каменів, пнів, дерев і бурʼяну.
- Кожне місце могили — «клітина» з шарами: яма/тіло, огорожа (низ), надгробок (верх) (?).
- Час — реальний із днями тижня (?); тіла надходять з часом, проповідь у церкві — у свій день (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Доглядач | player | енергія (?), три види досвіду | копає, ховає, крафтить, ставить прикраси |
| Місце могили | zone | вільне/зайняте | приймає одне тіло і прикраси |
| Тіло | object | якість: білі і червоні черепи | у морзі можна розкрити й змінити якість (?); псується з часом (?) |
| Огорожа могили | object | якість | шар могили; додає черепи |
| Надгробок | object | якість | шар могили; додає черепи |
| Сміття (камінь, пень, бурʼян, дерево) | static | — | розчистити, щоб звільнити місце; дає ресурси |
| Церква | object | обладнання | проповідь → пожертви; залежить від рейтингу цвинтаря (?) |
| Рейтинг цвинтаря | mark | сума черепів | показник якості всього цвинтаря |
| Зомбі (DLC Breaking Dead) | ally | — | воскрешені тіла працюють на збиранні, крафті, перевезенні |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(clear, debris)` → ТО `disappear_b`, `give(player, resource)`; клітина стає вільною під могилу.
- КОЛИ `input(dig, grave_slot)` → ЯКЩО `free(grave_slot)` → ТО `set_cell(grave_slot, open_grave)`.
- КОЛИ `input(bury, body, open_grave)` → ТО `set_cell(grave_slot, grave)`, `custom: «черепи тіла додаються до могили»`.
- КОЛИ `input(place, fence|headstone, grave)` → ЯКЩО `custom: «відповідний шар могили вільний»` and `has(player, item)` → ТО `place(item)`, `custom: «черепи прикраси додаються до могили»`.
- Якість могили: `custom: «білі черепи − червоні черепи по всіх шарах»` (?).
- Рейтинг: КОЛИ `after(grave_changed)` → ТО `counter(graveyard_rating, sum_of_graves)`.
- КОЛИ `input(autopsy, body)` → ТО `custom: «вийняти органи / жир / кров — змінити черепи тіла»` (?), `give(player, parts)`.
- КОЛИ `timer(day)` → ЯКЩО `not state(body, preserved)` → ТО `custom: «якість тіла падає»` (?).
- КОЛИ `input(sermon)` → ЯКЩО `custom: «день проповіді»` (?) → ТО `currency(+donations)`; розмір пожертв — від рейтингу й церкви (?).
- КОЛИ `input(dispose, body)` → ТО `disappear_a` — тіло можна не ховати: спалити чи скинути (?).
- КОЛИ `counter(red_xp|blue_xp|green_xp, >=, cost)` → ТО `unlock(technology)`; нові прикраси й рецепти — з дерева технологій.
- Перемога: сюжетна (повернутися у свій світ через портал) · Поразка: нема · Рахунок: рейтинг цвинтаря і церкви.

## Керування і ввід
- Рух аватара клавішами/стиком; дія — по обʼєкту перед собою (копати, ховати, розчистити).
- Тіло несуть на собі й кладуть у яму; прикраси — через меню будівництва над могилою (?).
- Наведення на могилу — підказка з черепами (?).

## Вікна, меню, HUD
- `game-screen`: світ, HUD — `energy-bar` (?), `coins`, три лічильники досвіду (червоний/синій/зелений), `+ui:skull-rating` біля могили, `+ui:grave-tooltip`.
- `custom-window` — дерево технологій; `inventory-window`; меню крафту на верстатах.
- `main-menu`, `settings-window`, `save-slots` (?).
- Переходи: game-screen ↔ дерево технологій · game-screen ↔ інвентар · верстат → крафт.

## Фічі поза полем
- `save-game` (Steam Cloud), `achievements` (Steam).
- DLC: Breaking Dead (зомбі-працівники, автоматизація), Stranger Sins (таверна з репутацією), Game of Crone (табір біженців), Better Save Soul (гріхи тіл, нові способи підняти якість тіла, віддалене керування верстатами).

## Варіації й родичі
- Корпус: `stardew-farm` (ділянки й крафт), `caesar-3` (`house-evolution`: будинок росте від того, що поруч), `prison-architect-rooms` (якість кімнати від предметів у ній), `acnh-flowers` (рейтинг острова).
- Осі «оцінка клітини»: сума шарів самої клітини (Graveyard Keeper) / від сусідів (Civ VI, Backpack Hero) / від покриття сервісами (Caesar III, Cities: Skylines).
- Осі «рейтинг місця»: сума всіх клітин / середнє / мінімум.

## Цікавинки для курсу
- Клітина з кількома слотами-шарами, кожен додає ±бал — 🌱.
- Рейтинг місця як сума клітин з оновленням при зміні — 🌱.
- Якість предмета, що падає з часом, і «консервація» як стан — 📎.
- Дерево технологій з трьома валютами досвіду — 📎.

## Мапа на каталог
- Є: `cell-click` · `multi-cell-size` (могила з прикрасами) · `coverage-area` (церква/сервіси (?)) · `inventory` · `round-currency` · `save-game`.
- Повтор з proposals: `+house-evolution` (caesar-3) — місце покращується від складу, тут частково.
- **Нема** → пропозиції карток:
  - `+layered-cell-score` «Клітина зі слотами-шарами, кожен дає бали» · entities/state · 🌱.
  - `+rating-sum` «Рейтинг місця = сума клітин» · game-logic/score · 🌱.
  - `+corpse-quality` «Якість предмета з плюсами й мінусами, яку можна правити» · entities/state · 📎.
  - `+grave-slots` «Фіксовані місця під споруду» · entities/legality · 🌱.
  - `+tech-tree-colors` «Дерево технологій з кількома видами досвіду» · levels/progression · 📎.

## Пропозиції до словників
- `+cond:slot_free` — у клітині вільний слот потрібного шару.
- `+effect:add_quality` — додати ±бали якості до клітини/предмета.
- `+effect:decay` — якість падає з часом (є в index/proposals — повтор).
- `+ui:skull-rating` — значок якості з плюс- і мінус-одиницями над клітиною; `+ui:grave-tooltip` — склад якості при наведенні.
- `+card:layered-cell-score`, `+card:rating-sum` — див. вище.

## Джерела
- ⭐ [Wikipedia: Graveyard Keeper](https://en.wikipedia.org/wiki/Graveyard_Keeper) — Lazy Bear Games / tinyBuild, 15.08.2018; розчистка ділянки, могили й церква дають дохід і пожертви, дерево технологій (червоний/синій/зелений досвід), DLC.
- [Steam: Graveyard Keeper](https://store.steampowered.com/app/599140/Graveyard_Keeper/) — керування цвинтарем, переробка тіл, алхімія, етичні вибори.
- YouTube: пошук «Graveyard Keeper gameplay».

## Непевне
- (?) Уся формула якості могили (білі/червоні черепи тіла + огорожа + надгробок, сума — рейтинг) — з памʼяті; fandom і wiki.gg не відкрились (402/401), WebSearch вичерпано.
- (?) Розкриття тіла в морзі змінює черепи; псування тіла з часом і консервація.
- (?) Дні тижня й день проповіді; залежність пожертв від рейтингу.
- (?) Способи позбутися тіла без поховання (спалити, скинути в річку).
- (?) Чи місця могил — фіксовані слоти, чи будь-які клітини цвинтаря.
