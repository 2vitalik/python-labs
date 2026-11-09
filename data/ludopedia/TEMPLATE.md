---
# Шапка — YAML, читається скриптами. Коментарі прибрати у файлі гри.
title: Назва гри                 # як її знають; UA-назва в дужках, якщо є усталена
slug: game-slug                  # = імʼя файла, lower-kebab, EN
aka: [Інша назва, Абревіатура]   # інші назви для пошуку: UA-переклад, регіональні назви, скорочення; нема — []
family: push-slide               # тека (taxonomy/families.md)
also: []                         # другорядні сімʼї, напр. [thinky]
klass: avatar                    # avatar | cursor | figure | puzzle | hybrid
axes:                            # vocab/classes.md; значення EN зі словника
  field: square                  # square | hex | graph | free | iso | layers | 1d | 3d
  time: turn                     # turn | realtime | static | rhythm | programmed
  opponent: none                 # none | ai | hotseat | online | coop
  info: full                     # full | hidden | partial
  random: none                   # none | setup | runtime | both
  goal: state                    # score | survive | state | constraints | race | territory | collect
year: 1982
platforms: [PC]                  # коротко: PC, web, mobile, NES, arcade, board …
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/…", best: true, note: "правила і історія"}
  - {kind: official, url: "https://…"}
  - {kind: steam, url: "https://store.steampowered.com/app/…"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=…", note: "пошук; геймплей"}
  - {kind: play, url: "https://…", note: "грати в браузері"}
  - {kind: fandom, url: "https://…", note: "вікі елементів (fandom, StrategyWiki)"}
  - {kind: other, url: "https://…", note: "FAQ, мануал, стаття; kind також: bgg, itch, strategywiki"}
stage: v1                        # v1 | v2 | v3
coverage: 70                     # % механіки, що ліг у структуру (сутності/правила/вікна зі словників), решта — текст
mechanics: [push-object, undo-redo, level-from-txt, +pull-object]   # slug-и каталогу; нове з «+»
proposes: ["+trigger:no-moves", "+window:level-password"]            # пропозиції до словників, з префіксом виду
author: opus                     # opus | fable | vitalik
date: 2026-11-02
---

# Назва — суть одним рядком

## Суть
2–5 речень: що робить гравець, у чому ядро, чим гра незвична. Без історії індустрії.

## Поле і час
Розмір/топологія поля, шари (поле+фон+обʼєкти), камера й видимість, що таке тік/хід, темп. Нестандартне (гекс, тор, кілька полів) — тут.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець | player | 1 життя | рух 4 напрямки, штовхає ящики |
| Ящик | object | — | зсувається на 1, якщо за ним вільно |
Роль — зі словника `vocab/roles.md`; параметри — лише ті, що пояснюють механіку; поведінка — коротко, формулою-реченням.

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `contact(player, box)` → ЯКЩО `free(cell_behind)` → ТО `push(box)`; інакше `block`.
- КОЛИ `all_on(box, target)` → ТО `win`.
- Перемога: … · Поразка: … · Рахунок: …
Слова — зі словників `vocab/triggers|conditions|effects.md` (✅ або ⏳); не лягає — `custom: «текст»` і рядок у «Пропозиції до словників».

## Керування і ввід
Що саме натискає гравець і що означає дія; режими вводу (виділення, drag, pencil marks, програмування ходів); черга ходів для кількох гравців.

## Вікна, меню, HUD
- Вікна: тип зі `vocab/windows.md` + що на ньому (`game-screen`: поле, лічильник ходів, кнопка undo).
- Меню і пункти: `main-menu`: Грати → `level-select`; Налаштування → `settings-window`; Вихід.
- HUD: елементи зі `vocab/ui-elements.md`.
- Переходи: A → B за дією.

## Фічі поза полем
Налаштування · режими · прогресія/рівні · збереження/статистика · undo/підказки/редактор/daily/мультиплеєр — зі `vocab/features.md`; що саме і як.

## Варіації й родичі
Відомі варіанти, клони, наступники; **осі варіацій**: «як це буває» (напр. штовхання: лише 1 ящик / ланцюг / тягнення).

## Цікавинки для курсу
3–7 механік, вартих стати завданням; ціна за шкалою монеток 🌱 wood · 📎 tin · 🥉 bronze · 🥈 silver · 🥇 gold · 👑 crown, одним рядком «чому саме стільки».

## Мапа на каталог
- Є в каталозі: `push-object` ↔ штовхання ящика; `undo-redo` ↔ …
- **Нема** → пропозиції карток: `+pull-object` «Тягнення» · entities/legality · 🥉 · слоти {…} — одним рядком кожна.

## Пропозиції до словників
- `+trigger:no-moves` — нема легальних ходів (2048, Sokoban-deadlock).
- `+window:level-password` — вхід на рівень за паролем (Chip's Challenge).
Префікси: `trigger` · `cond` · `effect` · `role` · `window` · `ui` · `feature` · `axis` · `card`.

## Джерела
- ⭐ [Назва](url) — що там є (правила, список елементів, відео з таймкодами).
- [Назва](url) — …

## Непевне
- (?) Що не вдалося перевірити або розходиться між джерелами.
