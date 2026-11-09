---
title: Griddle Words
slug: griddle-words
aka: [Griddle, Griddle+]
family: word-number
also: []
klass: puzzle
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: none
  goal: collect
year: 2025
platforms: [iOS]
links:
  - {kind: other, url: "https://apps.apple.com/app/griddle-words/id6755901046", best: true, note: "App Store: щоденна ручна сітка, свайп у 8 напрямках, знайти 100 % обовʼязкових слів, «плануй, щоб очистити поле», бонус-слова, серії, лідерборди, Griddle+"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=griddle+words+game", note: "пошук; геймплей"}
stage: v1
coverage: 40
mechanics: [daily-puzzle, swipe-gestures, path-drawing, word-validation, collect-all, completion-detection, streak-stats, leaderboard, save-progress, +clear-board-order, +bonus-words, +friend-codes, +puzzle-archive]
proposes: ["+cond:on_word_list", "+feature:friend-codes", "+feature:puzzle-archive"]
author: opus
date: 2026-11-09
---

# Griddle Words — щоденна сітка літер: знайди всі задані слова в такому порядку, щоб очистити поле

## Суть
Щодня — одна ручної роботи сітка літер. Гравець свайпом проводить шлях по сусідніх літерах (горизонтально, вертикально, по діагоналі) і складає слова; мета — знайти **усі обовʼязкові** слова. Опис наголошує «plan ahead to clear the board»: використані літери, судячи з усього, зникають, тож порядок знаходження слів важить (?). Додаткові «бонус-слова» піднімають рахунок.

## Поле і час
- Квадратна сітка літер, розмір не вказано (?); одна задача на добу, нова опівночі.
- Часу нема — пазл статичний, хід = одне знайдене слово.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Літера | tile | символ | частина шляху-слова; після використання, ймовірно, прибирається (?) |
| Обовʼязкове слово | mark | — | має бути знайдене для 100 % |
| Бонус-слово | pickup | очки | приховане зайве слово, дає бали |
| Шлях свайпу | zone | ланцюг сусідніх клітин | 8 напрямків |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(swipe, path)` → ЯКЩО `custom: «клітини шляху сусідні, 8 напрямків»` and `custom: «слово з обовʼязкового списку»` → ТО `custom: «слово зараховано»`, `clear(path)` (?).
- КОЛИ `input(swipe, path)` → ЯКЩО `in_dictionary(word)` and `custom: «не обовʼязкове»` → ТО `score(n)` — бонус-слово.
- КОЛИ `custom: «лишились літери, з яких не скласти решту слів»` → ТО `custom: «поле не очистити — треба інший порядок»` (?).
- КОЛИ `custom: «знайдено 100 % обовʼязкових слів»` → ТО `win`, `custom: «+1 до серії»`.
- Перемога: усі обовʼязкові слова, поле очищене · Поразка: нема явної (?) · Рахунок: обовʼязкові + бонус-слова.

## Керування і ввід
- Свайп пальцем по літерах (тач); відпустити — подати слово.

## Вікна, меню, HUD
- `game-screen`: сітка, прогрес знайденого (`progress-bar`), рахунок (`score`) (?).
- `stats-window` — серії · `leaderboard` — глобальні, між друзями за friend-кодом, приватні групи (з версії 1.5).
- `end-screen` — результат дня (?) · `shop-window` — Griddle+ (архів, без реклами).

## Фічі поза полем
- `mode-daily`, `streaks`, `stats`, `leaderboard-online`; `+feature:friend-codes`; `+feature:puzzle-archive` (Griddle+); Practice Mode (згадано в нотатках версії).

## Варіації й родичі
- [squaredle](squaredle.md) — те саме «8 напрямків + знайти всі слова», але літери не зникають; [spelltower](spelltower.md) — використані літери зникають, решта падає; [boggle](boggle.md), [word-search](word-search.md).
- **Осі варіацій**: літери — лишаються / зникають / падають · ціль — усі слова зі списку / найбільше очок · порядок — неважливий / важливий для очищення.

## Цікавинки для курсу
- Свайп-шлях по 8-сусідству з перевіркою слова — 📎.
- Порядок знаходження, що визначає, чи очиститься поле (пошук з поверненням) — 🥈 (перевірка розвʼязності дня).

## Мапа на каталог
- Є: `daily-puzzle` · `swipe-gestures` / `path-drawing` ↔ свайп по літерах · `word-validation` · `collect-all` ↔ 100 % слів · `completion-detection` · `streak-stats` · `leaderboard` · `save-progress`.
- **Нема** → пропозиції карток:
  - `+clear-board-order` «Використані клітини зникають; порядок дій визначає, чи очиститься поле» · game-logic/win · 🥈.
  - `+bonus-words` «Необовʼязкові слова дають очки понад ціль» · game-logic/score · 🌱.
  - `+friend-codes` «Друзі за кодом, лідерборд між ними» · interface/results · 📎.
  - `+puzzle-archive` «Архів минулих щоденних» · levels/bank · 🌱.

## Пропозиції до словників
- `+cond:on_word_list` — слово з заданого списку рівня (не лише зі словника).
- `+feature:friend-codes` · `+feature:puzzle-archive`.

## Джерела
- ⭐ [App Store: Griddle Words](https://apps.apple.com/app/griddle-words/id6755901046) — опис: щоденна ручна сітка, свайп у 8 напрямках, «plan ahead to clear the board», 100 % обовʼязкових слів, бонус-слова, серії, лідерборди, friend codes, Griddle+; One Thum Software, iOS 18+.
- YouTube: пошук «griddle words game».

## Непевне
- (?) Головне: чи зникають використані літери і чи є гравітація — опис каже лише «очистити поле», механіку з нього виведено.
- (?) Розмір сітки, чи кожна літера належить рівно одному обовʼязковому слову, підказки, ціна помилки.
- (?) Рік — найраніша видима версія 1.5.0 «21 квітня» без року; 2025 — оцінка (id застосунку дуже новий).
