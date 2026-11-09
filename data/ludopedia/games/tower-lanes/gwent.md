---
title: Gwent (Гвинт)
slug: gwent
aka: [Гвинт, "Gwent: The Witcher Card Game", Witcher 3 Gwent]
family: tower-lanes
also: []
klass: cursor
axes:
  field: 1d
  time: turn
  opponent: online
  info: hidden
  random: setup
  goal: score
year: 2015
platforms: [PC, PS4, Xbox One, iOS, Android, macOS]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Gwent:_The_Witcher_Card_Game", best: true, note: "окрема гра: 2 ряди, best-of-3, пас, провізія, фракції, режими"}
  - {kind: fandom, url: "https://thewitcher3.wiki.fextralife.com/Gwent", note: "Гвинт у Witcher 3: 3 ряди, погода по рядах, Horn, Decoy, Scorch, здібності, фракції"}
  - {kind: other, url: "https://cdn-l-thewitcher.cdprojektred.com/media/TW3/Pdf/GwentManuals/en-Manual-Gwent-ONLINE.pdf", note: "офіційний мануал CDPR (PDF; текст не витягнуто)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=witcher+3+gwent+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [pocket, inventory-limit, ai-opponent, online-multiplayer, rating-system, mode-select, pass-turn, +lane-grid, +deck-draw, +best-of-three-rounds, +row-power-sum, +row-weather, +row-multiplier, +adjacent-bond, +mulligan-redraw, +deck-builder, +card-collection]
proposes: ["+trigger:card_played", "+trigger:both_passed", "+effect:draw", "+effect:discard", "+effect:return_to_hand", "+effect:destroy_strongest", "+role:card", "+role:lane", "+ui:row-power", "+ui:round-gems", "+window:deck-builder"]
author: opus
date: 2026-11-09
---

# Gwent — карткова дуель на рядах: сила ряду сумується, погода й ріг діють на цілий ряд

## Суть
Карткова гра зі світу «Відьмака»: спершу міні-гра у The Witcher 3 (2015), потім окрема онлайн-гра (бета 2017, реліз 2018). Гравці по черзі кладуть по одній картці-юніту в свій ряд; рахунок раунду — сума сили на столі. Матч — найкраща з трьох партій, раунд закінчується, коли обидва спасували. Для корпусу цікава **рядна структура**: тип юніта визначає ряд, а ефекти (погода, Commander's Horn, Morale Boost) бʼють або множать **увесь ряд**.

## Поле і час
- У кожного гравця **3 ряди** (Witcher 3): Close Combat · Ranged · Siege; в окремій гві — **2 ряди** (Melee · Ranged), облоговий ряд прибрано.
- Ряд — лінія без фіксованих слотів; порядок у ряду важить (Tight Bond — сусідство).
- Біля кожного ряду — слот спецкартки (Commander's Horn: один на ряд); погода — спільна зона на обох гравців.
- Покроково: хід = одна картка або пас; хто спасував — до кінця раунду не ходить.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Картка-юніт | piece (`+role:card`) | сила, ряд, здібність | лягає у свій ряд; сила йде в суму |
| Ряд | zone (`+role:lane`) | тип (ближній/дальній/облога) | сумує силу; на нього діють погода й ріг |
| Hero | piece | — | імунний до погоди, спецкарток і здібностей |
| Agile | piece | 2 ряди | можна покласти в ближній або дальній; після цього не рухається |
| Tight Bond | piece | — | поруч з однойменною — обидві ×2 (у джерелах також «× кількість») |
| Morale Boost | piece | — | +1 іншим юнітам свого ряду |
| Muster | piece | — | викладає з колоди всі картки з тим самим імʼям |
| Medic | piece | — | одразу грає юніт зі свого скиду (не героя, не спецкарту) |
| Spy | piece | — | кладеться на бік суперника (сила йому), ти добираєш 2 |
| Biting Frost / Impenetrable Fog / Torrential Rain | hazard | ряд | сила всіх юнітів ряду обох гравців = 1 |
| Clear Weather | object | — | знімає всю погоду |
| Commander's Horn | object | 1 на ряд | ×2 сила свого ряду |
| Decoy | object | — | міняється з юнітом на столі, той повертається в руку |
| Scorch | object | — | знищує найсильнішу(і) картку(и) на столі |
| Лідер | piece | 1 раз за матч | особлива дія фракції (напр. Foltest грає Fog) |
| Рука / колода / скид | zone | 10 карт у руці | рука на весь матч, добір рідкісний |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `game_start` → ТО `custom: «підкидання монети — хто перший»`, кожному `custom: «effect draw ×10»`; один раз `choose(2 картки)` → скинути й добрати.
- КОЛИ `input(play, unit)` → ЯКЩО `turn_of(player)` and `custom: «ряд відповідає типу»` → ТО `place(unit, row)`, `end_turn`.
- КОЛИ `input(pass)` → ТО `pass_turn`, `custom: «гравець вибуває з раунду»`.
- КОЛИ `custom: «обидва спасували або нема карт»` → ТО `custom: «раунд виграє більша сума сили»`; КОЛИ `counter(rounds_won, ==, 2)` → ТО `win`.
- КОЛИ `input(play, weather_row)` → ТО `set_state(row_both_sides, weather)`: сила не-героїв = 1.
- КОЛИ `input(play, clear_weather)` → ТО `clear_state(all_rows, weather)`.
- КОЛИ `input(play, horn, row)` → ЯКЩО `not occupied(horn_slot, horn)` → ТО `multiplier(×2)` для не-героїв ряду.
- КОЛИ `card_played(tight_bond)` → ЯКЩО `same(a, b, name)` and `custom: «у тому ж ряду»` → ТО `custom: «сила обох ×2»`.
- КОЛИ `card_played(morale_boost)` → ТО `custom: «+1 іншим юнітам ряду»`.
- КОЛИ `card_played(spy)` → ТО `place(spy, opponent_row)`, `custom: «effect draw ×2»`.
- КОЛИ `card_played(muster)` → ТО `custom: «викласти з колоди всі однойменні»`.
- КОЛИ `card_played(medic)` → ТО `custom: «зіграти юніт зі скиду»`.
- КОЛИ `input(play, decoy, unit)` → ЯКЩО `not state(unit, hero)` → ТО `swap(decoy, unit)`, `custom: «unit → рука»`.
- КОЛИ `input(play, scorch)` → ТО `custom: «знищити найсильніші не-героїчні картки на столі»`.
- КОЛИ `custom: «кінець раунду»` → ТО `custom: «стіл → скид»`; Monsters — `custom: «один випадковий юніт лишається»`; Northern Realms — після виграного раунду `custom: «добір 1»`; Nilfgaard — `custom: «нічия = перемога»`.
- Перемога: 2 виграні раунди · Поразка: 2 програні · Рахунок: сума сили рядів у раунді.

## Керування і ввід
- Миша/тач: вибір картки з руки → клік по ряду (Agile — вибір з двох) → картка лягає; спецкартка — на слот ряду або на ціль (Decoy).
- Кнопка «Пас»; дія лідера — окрема кнопка, раз за матч.

## Вікна, меню, HUD
- `game-screen`: два набори рядів, сума сили біля кожного ряду (`+ui:row-power`) і загальна, `+ui:round-gems` (виграні раунди/життя), `pocket` (рука), лічильник колоди, лідер, `turn-indicator`.
- `+window:deck-builder`: колода ≥ 25 карт (≥ 13 юнітів) і ліміт провізії 150 + бонус лідера; бронзові ×2, золоті ×1 (окрема гра).
- `mode-select`: Ranked / Casual / сезонний режим (окрема гра); у Witcher 3 — партія з NPC.
- `end-screen` з рахунком раундів · `profile-window` з рівнями й престижем.

## Фічі поза полем
- `+card-collection` (картки виграються в NPC у Witcher 3 / крафт і бочки в окремій грі (?)).
- `rank-tiers`: ранги 30 → 1 → Pro Rank, щомісячні сезони зі скиданням на 2 ранги; `xp-level` 1–60 + престиж.
- Спін-офи з тим самим двіжком: Thronebreaker (кампанія), Gwent: Rogue Mage (роглайт без раундів).

## Варіації й родичі
- Родичі в сімʼї: [inscryption](inscryption.md) (4 смуги, атака по смузі), [marvel-snap](marvel-snap.md) (3 локації, сума сили), [wildfrost](wildfrost.md), [monster-train](monster-train.md).
- **Осі варіацій**: рядів 3 / 2 · ряд визначає тип карти / вільний вибір (Agile) · погода — дебаф ряду обох сторін / власний ефект ряду · раунди best-of-3 з рукою на весь матч / одна партія.

## Цікавинки для курсу
- Рядна сума з модифікаторами (погода = 1, ріг ×2, Morale +1, Tight Bond ×n) і правильним порядком застосування — 🥉.
- Пас і рука на весь матч: стратегія «віддати раунд, зберегти карти» — 📎 (правила), AI-суперник — 🥈.
- Decoy / Spy / Muster / Medic — малі ефекти з руху карт між зонами (рука, колода, скид, стіл) — 📎.
- Конструктор колоди з лімітом провізії — 🥉.

## Мапа на каталог
- Є: `pocket` ↔ рука · `inventory-limit` ↔ 10 карт · `pass-turn` ↔ пас · `ai-opponent` · `online-multiplayer` · `rating-system` ↔ ранги · `mode-select`.
- **Нема** → пропозиції карток:
  - `+lane-grid`, `+deck-draw`, `+deck-builder`, `+card-collection` — уже пропоновані сімʼєю (Inscryption, Marvel Snap).
  - `+best-of-three-rounds` «Матч з раундів до 2 перемог» · game-logic/win · 🌱.
  - `+row-power-sum` «Сума сили ряду» · game-logic/score · 🌱.
  - `+row-weather` «Ефект на весь ряд обох сторін» · entities/state · 📎.
  - `+row-multiplier` «Множник ряду» · entities/state · 🌱.
  - `+adjacent-bond` «Однойменні поруч підсилюють одна одну» · entities/state · 📎.
  - `+mulligan-redraw` «Скинути N і добрати на старті» · game-logic/opponent · 🌱.

## Пропозиції до словників
- `+trigger:card_played`, `+effect:draw`, `+effect:discard`, `+role:card`, `+role:lane`, `+window:deck-builder` — підтвердження з Inscryption/Marvel Snap.
- `+trigger:both_passed` — обидва гравці спасували (кінець раунду).
- `+effect:return_to_hand` — картка зі столу назад у руку (Decoy).
- `+effect:destroy_strongest` — знищити сутність(і) з максимальним параметром (Scorch).
- `+ui:row-power` — сума сили біля ряду; `+ui:round-gems` — індикатор виграних/програних раундів.

## Джерела
- ⭐ [Wikipedia: Gwent: The Witcher Card Game](https://en.wikipedia.org/wiki/Gwent:_The_Witcher_Card_Game) — 2 ряди (облогу прибрано), best-of-3, рука з 10 з колоди 25, пас, провізія 150, фракції й лідери, ранги, релізи.
- [Fextralife: Gwent (Witcher 3)](https://thewitcher3.wiki.fextralife.com/Gwent) — 3 ряди, погода по рядах, Horn/Decoy/Scorch, здібності юнітів, перки фракцій, лідери, redraw 2.
- [CDPR: мануал Gwent (PDF)](https://cdn-l-thewitcher.cdprojektred.com/media/TW3/Pdf/GwentManuals/en-Manual-Gwent-ONLINE.pdf) — офіційні правила; текст не вдалося витягти.

## Непевне
- (?) Множник Tight Bond: ×2 обом чи × кількість однойменних — джерела розходяться.
- (?) Чи «життя» (2 кристали) у Witcher 3 і в окремій грі однакові; правила нічиєї для не-Nilfgaard.
- (?) Мінімум колоди у Witcher 3 (22 юніти?) — Fextralife наводить колоди 27–40.
- (?) Skellige Storm та ефекти погоди окремої гри — не перевірено.
