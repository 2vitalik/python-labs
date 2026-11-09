---
title: Terry The Skeleton
slug: terry-the-skeleton
aka: [Terry the Skeleton]
family: roguelike
also: [maze-arcade]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: partial
  random: setup
  goal: score
year: 2019
platforms: [web (HTML5), PICO-8]
links:
  - {kind: itch, url: "https://amidos2006.itch.io/terry-the-skeleton", best: true, note: "грати в браузері + повні правила: гравець у реальному часі, вороги — фазами за таймером, підсвічені клітини атак, ривок до стіни"}
  - {kind: itch, url: "https://itch.io/jam/procjam2019/rate/513278", note: "сторінка PROCJAM 2019: «Realtime turn-based #Broughlike», коментарі (лицарі, лучники, маги, жерці в першій кімнаті)"}
  - {kind: itch, url: "https://amidos2006.itch.io/berry-the-scientist", note: "Berry The Scientist — альтернативна версія: до 3 ходів гравця на хід ворогів, без годинника"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=terry+the+skeleton+amidos2006+pico-8", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [move-4dir, inertia-slide, piece-capture, hp-damage, destroy-all-enemies, sequential-levels, move-timer, telegraphed-intents, telegraph-marker, path-preview, mode-indicator, move-counter, keyboard-controls, +realtime-player-timed-enemies, +move-mode-toggle, +attack-then-move-phase, +heal-on-level, +fewest-enemy-steps-score]
proposes: ["+effect:toggle_mode(a)", "+ui:landing-stars", "+ui:turn-timer-bar", "+axis:time=realtime-vs-turn"]
author: opus
date: 2026-11-09
---

# Terry The Skeleton — броуглайк, де скелет ходить у реальному часі, а вороги — фазами за таймером

## Суть
Маленька PICO-8-гра з PROCJAM 2019 (Ahmed Khalifa, Amidos2006): скелет Террі зачищає кімнати на клітинному полі. Гравець рухається **в реальному часі**, а вороги — **покроково за таймером**: коли він спливає, вороги спершу бʼють по заздалегідь підсвічених клітинах, потім рухаються. Террі вбиває, просто входячи у ворога, і має два режими руху — крок на 1 клітину або ривок до стіни. Мета — пройти гру за найменшу кількість кроків ворогів.

## Поле і час
- Кімната — квадратна сітка клітин; убив усіх ворогів — перехід до наступної кімнати.
- Два годинники: гравець ходить вільно в реальному часі; ворожий хід настає за таймером (смуга внизу екрана). Таймер стартує лише після першого руху.
- Порядок циклу: **хід гравця → атака ворогів → рух ворогів**.
- `info: partial`: поле видно цілком, а намір ворогів показано підсвіченими клітинами атаки (як телеграф у Into the Breach).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Террі | player | HP, режим руху (колір очей) | крок на 1 клітину або ривок до стіни; вбиває, входячи у ворога; +1 HP за новий рівень |
| Ворог (лицар, лучник, маг, жрець) | enemy | простий патерн руху, чітка зона атаки | у фазі атаки бʼє по своїх підсвічених клітинах, у фазі руху — рухається за патерном |
| Підсвічена клітина | mark | — | клітина, куди вдарять вороги наступної фази атаки |
| Стіна | static | — | непрохідна; зупиняє ривок |
| Зірочка-приземлення | mark | — | показує, де Террі опиниться після дії; нема зірочки — рух у той бік неможливий |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(arrow)` → ЯКЩО `mode(walk)` and `free(cell)` → ТО `move(terry, dir)`.
- КОЛИ `input(arrow)` → ЯКЩО `mode(dash)` → ТО `slide(terry, dir)` (до стіни).
- КОЛИ `input(x | z)` → ТО `custom: «перемкнути режим: крок ↔ ривок»`, `custom: «колір очей Террі показує режим»`.
- КОЛИ `input(arrow)` → ЯКЩО `occupied(cell, enemy)` → ТО `disappear(enemy)` (вбивство входом у ворога).
- КОЛИ `input(arrow)` → ЯКЩО `custom: «у цьому напрямку нема зірочки»` → ТО `block`; атакувати сусіднього ворога все одно можна.
- КОЛИ `input(arrow)` → ЯКЩО `first_time` → ТО `timer(start)`.
- КОЛИ `timer(turn)` → ТО `custom: «фаза атаки ворогів, потім фаза руху»`.
- КОЛИ `phase_start(enemy_attack)` → ЯКЩО `custom: «Террі стоїть на підсвіченій клітині»` → ТО `damage(terry, n)`.
- КОЛИ `phase_start(enemy_move)` → ТО `move(enemy, pattern)`, `counter(enemy_steps, +1)`, `mark(next_attack_cells, highlight)`.
- КОЛИ `custom: «таймер майже вичерпано»` → ТО `custom: «Террі блимає»`.
- КОЛИ `all_gone(enemy)` → ТО `next_level`, `heal(terry, 1)`.
- КОЛИ `hp_zero(terry)` → ТО `lose`.
- Перемога: пройти всі кімнати. Поразка: HP = 0. Рахунок: кількість кроків ворогів за всю гру — менше = краще.

## Керування і ввід
- Стрілки — крок або ривок залежно від режиму; `X` / `Z` — перемкнути режим.
- Ввід реального часу: між ворожими фазами можна робити кілька дій (обмежує лише таймер).

## Вікна, меню, HUD
- `game-screen`: кімната, `+ui:turn-timer-bar` (смуга таймера ворожого ходу внизу), HP, `+ui:landing-stars` (обертові зірочки — куди приземлишся), підсвічені клітини атак (`telegraph-marker`), колір очей як `mode-indicator`.
- `end-screen` — фінал із кількістю кроків ворогів (?).

## Фічі поза полем
- Speedrun-формат: тег `speedrun`, рахунок у «кроках ворогів», а не в секундах.
- Навмисно високий старт складності: за словами автора, гравець «уже майже в кінці гри».

## Варіації й родичі
- **Berry The Scientist** (той самий автор, альтернативна версія): без годинника, до **трьох** ходів гравця на кожен хід ворогів — та сама гра як чистий покроковий броуглайк.
- Родичі в корпусі: [crypt-of-the-necrodancer](crypt-of-the-necrodancer.md) (вороги в такт, гравець має вкластись у ритм), [mosaic-broughlike](mosaic-broughlike.md) і [magpie-broughlike](magpie-broughlike.md) (броуглайки), [868-hack](868-hack.md), [shogun-showdown](shogun-showdown.md) (телеграфовані атаки).
- Осі варіацій: **годинник** (нема / таймер на хід ворогів / такт музики) · **ходів гравця на хід ворогів** (1 / 3 / скільки встигнеш) · **рух** (крок / ривок до стіни / перемикач) · **рахунок** (час / ходи ворогів).

## Цікавинки для курсу
- Гібридний час: гравець у реальному часі, вороги — дискретними фазами за таймером, що стартує з першим рухом — 📎.
- Телеграф атак: вороги підсвічують клітини, по яких ударять, і бʼють перед рухом — 🌱 (картка `telegraph-marker` є).
- Перемикач режиму руху (крок / ривок до стіни) з превʼю приземлення — 🌱.
- Рахунок у «кроках ворогів» як міра швидкості проходження — 🌱.
- Порівняння Terry / Berry: один параметр «ходів гравця на хід ворогів» перетворює екшн на покрокову гру — 📎.

## Мапа на каталог
- Є: `move-4dir` (стрілки) · `inertia-slide` (ривок до стіни) · `piece-capture` (вхід у ворога = вбивство) · `hp-damage` · `destroy-all-enemies` · `sequential-levels` (кімнати) · `move-timer` (таймер ворожого ходу) · `telegraphed-intents` + `telegraph-marker` · `path-preview` (зірочки) · `mode-indicator` (колір очей) · `move-counter` (кроки ворогів) · `keyboard-controls`.
- **Нема** → пропозиції карток:
  - `+realtime-player-timed-enemies` «Гравець у реальному часі, вороги — за таймером» · game-logic/opponent · 📎 · слот {period}.
  - `+move-mode-toggle` «Перемикач режиму руху (крок / ривок)» · entities/move · 🌱.
  - `+attack-then-move-phase` «Вороги спершу бʼють, потім ходять» · game-logic/opponent · 🌱.
  - `+heal-on-level` «+1 HP за новий рівень» · levels/progression · 🌱.
  - `+fewest-enemy-steps-score` «Рахунок — кількість ходів ворогів» · game-logic/score · 🌱.

## Пропозиції до словників
- `+effect:toggle_mode(a)` — перемкнути режим руху/дії сутності.
- `+ui:landing-stars` — маркери «куди приземлишся» для кожного напрямку; `+ui:turn-timer-bar` — смуга часу до ходу ворогів.
- `+axis:time=realtime-vs-turn` — гравець і вороги живуть у різних моделях часу.

## Джерела
- ⭐ [itch.io: Terry The Skeleton](https://amidos2006.itch.io/terry-the-skeleton) — гра в браузері й правила автора: реальний час проти покрокових ворогів, порядок фаз, підсвічені клітини, режими руху, зірочки, колір очей, +1 HP за рівень, рахунок у кроках ворогів.
- [PROCJAM 2019](https://itch.io/jam/procjam2019/rate/513278) — жанр «Realtime turn-based #Broughlike», коментарі гравців про першу кімнату.
- [Berry The Scientist](https://amidos2006.itch.io/berry-the-scientist) — варіант із трьома ходами гравця на хід ворогів.

## Непевне
- (?) Типи ворогів (лицар, лучник, маг, жрець) — лише з коментаря гравця на сторінці джему; їх патерни руху й атаки не описані.
- (?) Скільки HP знімає удар ворога і скільки HP на старті — не вказано.
- (?) Що саме генерується процедурно (кімнати, склад ворогів) — сторінки не пояснюють, хоч гра зроблена для PROCJAM.
- (?) Чи може ривок закінчитись атакою ворога на шляху — не описано.
- (?) Кількість кімнат/рівнів і вигляд фінального екрана — не вказано.
