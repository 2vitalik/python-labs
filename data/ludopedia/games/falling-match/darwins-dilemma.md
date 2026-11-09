---
title: Darwin's Dilemma
slug: darwins-dilemma
aka: []
family: falling-match
also: [push-slide]
klass: cursor
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: runtime
  goal: state
year: 1990
platforms: [Mac, X68000, FM Towns, PC-98]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Darwin%27s_Dilemma", best: true, note: "стаб: зіставляй істот, після кількох збігів вони «еволюціонують»; автор, платформи"}
  - {kind: other, url: "http://www.homeoftheunderdogs.net/game.php?id=3075", note: "Home of the Underdogs: штовхати однакових істот разом, предок Evolution, прототип IconQuest"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=darwin%27s+dilemma+mac+1990", note: "пошук; геймплей"}
stage: v1
coverage: 40
mechanics: [tile-merge, push-object, cell-click, sequential-levels, event-points, score-records, +evolution-chain]
proposes: ["+card:evolution-chain"]
author: opus
date: 2026-11-09
---

# Darwin's Dilemma — штовхай однакових істот одна до одної; після кількох збігів вони еволюціонують у нових

## Суть
Mac-пазл 1990 року (André Ouimet, Inline Design), ранній предок merge-ігор. Гравець **штовхає** однакових істот одну до одної; після достатньої кількості збігів істоти «еволюціонують» у новий вид, і вже його треба зіставляти далі — так гравець просувається вгору еволюційним ланцюгом. Сучасники порівнювали гру з Life Конвея і зі старшою грою Evolution; прототип — безкоштовна IconQuest (та сама механіка, піктограми замість істот).

## Поле і час
- Клітинне поле з істотами (?): розмір, стіни, перешкоди — не підтверджено.
- Хід — штовхнути істоту (?); чи є таймер на рівень — (?).
- Рівні з ланцюгом еволюції; що саме є метою рівня — (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Істота | tile | вид = сходинка ланцюга еволюції | штовхається; збігається з однаковою |
| Еволюціонована істота | tile | наступна сходинка | зʼявляється після достатньої кількості збігів; зіставляється далі |
| Поле / стіни | static | — (?) | обмежують рух (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(push creature, dir)` → ТО `push(creature)` (дальність — на 1 чи до упору — (?)).
- КОЛИ `contact(creature, other)` → ЯКЩО `same(creature, other, species)` → ТО `custom: «збіг: зараховано»`, `counter(matches, +1)`.
- КОЛИ `counter(matches, >=, n)` → ТО `transform(creature → next_species)` — еволюція.
- КОЛИ `custom: «досягнуто верхньої сходинки»` → ТО `win` (?).
- Перемога / поразка / рахунок — (?): джерела описують лише «штовхати однакових → еволюція → далі».

## Керування і ввід
- Миша (Mac): обрати істоту й напрям штовхання (?).

## Вікна, меню, HUD
- `game-screen`: поле з істотами (?), рахунок (?).
- Друкований «Field Guide to Evolution» у коробці — довідник видів (аналог `codex-window` на папері).

## Фічі поза полем
- `levels-sequential` (?); `leaderboard-local` (?).
- Порти на японські ПК: X68000, FM Towns, PC-98.

## Варіації й родичі
- Попередники: Evolution (старша гра, «простіша»), IconQuest (freeware-прототип).
- Нащадки за ідеєю «однакові → новий рівень»: [triple-town](triple-town.md), [suika-game](suika-game.md), [threes](threes.md), [2048](2048.md).
- **Осі варіацій**: як зводиш однакових (штовхання / свайп усього поля / кидання / постановка) · коли еволюція (одразу на злитті / після N збігів) · що далі (той самий ланцюг / розгалуження).

## Цікавинки для курсу
- Ланцюг еволюції як таблиця «вид → наступний вид» з лічильником збігів — 🌱.
- Штовхання з перевіркою збігу на зіткненні — 🌱 / 📎.
- Генератор рівнів, де ланцюг досяжний до вершини — 🥈.

## Мапа на каталог
- Є: `tile-merge` (однакові дають наступний) · `push-object` (штовхання) · `cell-click` (?) · `sequential-levels` (?) · `event-points` (?) · `score-records` (?).
- **Нема** → `+evolution-chain` «Ланцюг еволюції: N збігів → наступний вид» · entities/state · 🌱.

## Пропозиції до словників
- `+card:evolution-chain` — збіги однакових накопичуються, вид піднімається на сходинку (Darwin's Dilemma; Triple Town — без лічильника).

## Джерела
- ⭐ [Wikipedia: Darwin's Dilemma](https://en.wikipedia.org/wiki/Darwin%27s_Dilemma) — суть (зіставляй → еволюція), автори, платформи, Games 100 (1992).
- [Home of the Underdogs](http://www.homeoftheunderdogs.net/game.php?id=3075) — «штовхати однакових істот разом», порівняння з Evolution і Life, прототип IconQuest.
- YouTube: пошук «darwin's dilemma mac 1990».

## Непевне
- Джерела — лише два короткі описи; MobyGames (403), Macintosh Garden (TLS-помилка) не відкрились, WebSearch вичерпано.
- (?) Форма поля, дальність штовхання, скільки збігів треба на еволюцію, перешкоди й таймер.
- (?) Мета рівня і поразка; система очок.
- (?) Клас `cursor` і вісь `time: turn` — припущення за описом «штовхати».
