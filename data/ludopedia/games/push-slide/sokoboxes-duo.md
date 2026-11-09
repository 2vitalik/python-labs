---
title: Sokoboxes Duo
slug: sokoboxes-duo
aka: [Sokoboxes]
family: push-slide
also: []
klass: avatar
axes:
  field: square
  time: turn
  opponent: coop
  info: full
  random: none
  goal: state
year: 2023
platforms: [Windows]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/2107780/Sokoboxes_Duo/", best: true, note: "опис: два працівники, 115 duo + 522 solo рівнів, 1–2 контролери, перемикання або гра разом, повтор розвʼязку"}
  - {kind: official, url: "https://sokoboxes.com/", note: "сайт автора: архів історії Sokoban, статті"}
  - {kind: other, url: "https://sokoboxes.com/info/", note: "базові правила Sokoban, Duo серед «Sokoban Variants»"}
  - {kind: other, url: "https://www.vgdb.co/games/sokoboxes-duo", note: "картка гри; «buddy, never an obstacle», запис кроків і повтор"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Sokoboxes+Duo+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [move-4dir, keyboard-controls, push-object, impassable-cells, party-switch, deadlock-detection, unsolvable-states, move-counter, level-bank, level-select, difficulty-levels, replay, save-progress, achievements-window, character-select, +multi-pusher, +shared-screen-coop]
proposes: ["+feature:control-split", "+card:multi-pusher", "+card:shared-screen-coop"]
author: opus
date: 2026-11-09
---

# Sokoboxes Duo — Sokoban на двох працівників: рівні, які сам не розвʼяжеш, бо кожному з двох дісталась своя роль

## Суть
Класичний [sokoban](sokoban.md) (штовхати ящики на цілі, без тягнення, по одному), але на duo-рівнях на складі **два** працівники. Рівні побудовано так, що один не впорається: другий персонаж — «завжди помічник, ніколи не перешкода», кожен має незамінну роль. Грати можна самому з перемиканням між персонажами або вдвох на 1–2 контролерах. Окремо — сотні solo-рівнів звичайного Sokoban.

## Поле і час
- Квадратна сітка складу: підлога, стіни, ящики, цілі; кількість ящиків = кількості цілей.
- Хід = крок одного працівника; без вводу нічого не рухається. Вдвох персонажі, за оглядом, можуть рухатися незалежно/«одночасно» — це просто чергування кроків від двох контролерів (?).
- Один екран без скролу (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Працівник 1 / 2 (Penguin, Bear, Neko) | player | активний / ні | рух 4 напрямки; штовхає ящик, якщо за ним вільно |
| Ящик | object | — | зсувається на 1 від поштовху; не тягнеться; по одному |
| Ціль | terrain | — | місце для ящика |
| Стіна | static | — | непрохідна |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir, worker)` → ЯКЩО `free(next_cell)` → ТО `move(worker, dir)`, `counter(steps, +1)`.
- КОЛИ `contact(worker, box)` → ЯКЩО `free(cell_behind)` → ТО `push`, `move(worker, dir)`.
- КОЛИ `contact(worker, box)` → ЯКЩО `occupied(cell_behind, box)` або `cell(cell_behind, wall)` → ТО `block`.
- КОЛИ `contact(worker, other_worker)` → ТО `block` (працівник не штовхає напарника) (?).
- КОЛИ `contact(worker, box)` → ЯКЩО `occupied(cell_behind, other_worker)` → ТО `block` (?).
- КОЛИ `input(switch)` → ТО `custom: «перемкнути активного працівника»` (соло-керування duo-рівнем).
- КОЛИ `all_on(box, target)` → ТО `win`, `custom: «зберегти кількість кроків і розвʼязок»`.
- Перемога: усі ящики на цілях. · Поразка: нема; глухий кут → undo/рестарт (?). · Рахунок: кількість кроків (рекорд рівня).

## Керування і ввід
- Соло: один контролер/клавіатура, кнопка перемикання персонажа.
- Вдвох: 2 контролери — кожен веде свого працівника (по черзі або «разом»); або один контролер, який передають.
- Undo / рестарт — (?) (на Steam-сторінці не згадано).

## Вікна, меню, HUD
- `main-menu`: Duo / Solo (?).
- `mode-select`: duo-рівні або solo-рівні; кількість контролерів (?).
- `level-select` / `puzzle-select`: рівні від Beginner до Ultimate, позначки розвʼязаних (?).
- `character-select`: Penguin, Bear, Neko (?).
- `game-screen`: склад; HUD — `move-counter`, хто активний (`mode-indicator`) (?).
- `replay-window`: перегляд свого розвʼязку для покращення кількості кроків.
- `achievements-window` (Steam).
- Комікс-сюжет між рівнями (`dialogue-window`) (?).

## Фічі поза полем
- `mode-coop` локально (shared/split screen за тегами Steam).
- `puzzle-bank`: 115 duo (84 — Aymeric du Peloux, 31 — інші) і 522 solo (223 — du Peloux, 262 — Evgeny Grigoriev, 37 — інші).
- `difficulty-presets` як сортування рівнів Beginner → Ultimate.
- `stats`: кроки розвʼязку на рівень; `replay` розвʼязку; `cloud-save`, `achievements`.

## Варіації й родичі
- [sokoban](sokoban.md) — базові правила; [kwirk](kwirk.md) — кілька аватарів із перемиканням, але кожен сам по собі.
- Осі варіацій:
  - **кількість штовхачів**: 1 (Sokoban) / 2 з обовʼязковою співпрацею (Duo) / N з перемиканням (XOR, The Lost Vikings);
  - **хто керує**: один гравець перемикає / два гравці кожен свого;
  - **чи штовхає напарника**: ні (перешкода, (?)) / так (ланцюг);
  - **навіщо другий**: вийти мають усі (Kwirk) / другий потрібен, щоб дістати ящик, який один загнав би в кут (Duo).

## Цікавинки для курсу
- Два аватари на одному полі, ввід із двох джерел, кожен крок перевіряє і ящики, і напарника — 🌱.
- Розвʼязувач для двох працівників: стан = позиції обох + ящиків, BFS/A*; простір станів росте квадратично — 🥇.
- Детектор глухого кута, що враховує другого працівника (кут не мертвий, якщо є другий штовхач з іншого боку) — 🥈.
- Запис розвʼязку як рядка ходів обох + replay — 📎.

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls`; `push-object`; `impassable-cells`; `party-switch` ↔ соло-перемикання; `deadlock-detection` + `unsolvable-states`; `move-counter` ↔ кроки; `level-bank` + `level-select` + `difficulty-levels` ↔ Beginner–Ultimate; `replay` ↔ повтор розвʼязку; `save-progress`; `achievements-window`; `character-select`.
- **Нема** → пропозиції карток:
  - `+multi-pusher` «Кілька штовхачів на одному полі, рівень вимагає обох» · entities/move · 🥉 · слот {n_workers, can_push_worker}.
  - `+shared-screen-coop` (вже пропонована) — двоє гравців на одному екрані, кожен свого аватара.

## Пропозиції до словників
- `+feature:control-split` — один гравець перемикає персонажів або кожен гравець веде свого на тому самому рівні.
- `+card:multi-pusher`, `+card:shared-screen-coop`.

## Джерела
- ⭐ [Steam: Sokoboxes Duo](https://store.steampowered.com/app/2107780/Sokoboxes_Duo/) — суть duo-рівнів, кількість і автори рівнів, 1–2 контролери, персонажі, запис кроків і повтор розвʼязку, дата 20.06.2023, автор Carlos Montiers Aguilera, видавець IKERGAMES.
- [sokoboxes.com](https://sokoboxes.com/) і [/info/](https://sokoboxes.com/info/) — правила Sokoban, Duo як варіант.
- [VGDB](https://www.vgdb.co/games/sokoboxes-duo) — опис, «buddy, never an obstacle».
- YouTube: пошук «Sokoboxes Duo gameplay».

## Непевне
- (?) Чи працівник може штовхнути напарника або ящик, за яким стоїть напарник — не знайдено; у правилах — як у звичайному Sokoban (перешкода).
- (?) Огляд згадує, що вдвох «можна рухатися одночасно» й діставати ящики з кутів, — чи є спільний поштовх (обидва з одного боку), не перевірено.
- (?) Undo, рестарт, редактор, імпорт рівнів, меню й HUD — на сторінках не описані; вікна вище — типові для жанру.
- (?) Платформа лише Windows (вимоги «OS: 10, 64-bit»).
