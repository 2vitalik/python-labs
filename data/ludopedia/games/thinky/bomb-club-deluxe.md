---
title: Bomb Club Deluxe
slug: bomb-club-deluxe
aka: [Bomb Club]
family: thinky
also: []
klass: cursor
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: none
  goal: state
year: 2022
platforms: [PC, Mac, Linux, iOS (Bomb Club), Android (Bomb Club)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1771440/Bomb_Club_Deluxe/", best: true, note: "опис, трейлер, 11 скриншотів: острови-сітка, рука бомб і капелюхів, Nitronomicon, мапа"}
  - {kind: official, url: "http://bombclubdeluxe.sos-webcomic.com/", note: "сайт гри: бомби Laser / Black Hole / Magma / Smoke, капелюхи, опційні рівні; трейлери"}
  - {kind: other, url: "http://bombclubdeluxe.sos-webcomic.com/presskit.html", note: "прескіт: «розстав бомби, щоб усі вибухнули одним ланцюгом», капелюхи, феєрверки для рахунку; 20+ бомб, 12 капелюхів, 200+ рівнів"}
  - {kind: other, url: "http://bombclub.sos-webcomic.com/releases.html", note: "патчі мобільного Bomb Club: рівні Triple Trouble з таймером і фазами, перетягування, прискорення ланцюга, двері мапи"}
  - {kind: steam, url: "https://store.steampowered.com/app/1873060/", note: "безкоштовне демо: уся перша зона"}
  - {kind: other, url: "https://www.pocketgamer.com/bomb-club/bomb-club-lets-you-bomb-everything-in-a-chain-reaction-of-explosions-out-now-on/", note: "мобільний Bomb Club (липень 2021): Blaze Bomb хрестом і над проміжками, F2P"}
  - {kind: youtube, url: "https://www.youtube.com/watch?v=9Z3Ovn-baZk", note: "трейлер (вбудований на офіційному сайті)"}
stage: v1
coverage: 35
mechanics: [chain-detonation, blast-wave, drag-drop-piece, cursor-place, pocket, world-map, level-unlock, codex-window, tutorial-window, event-points, restart-level, game-screen, map-window, settings-window, language-picker, achievements-window, save-progress, background-music, +single-chain-clear, +bomb-hat-modifier, +linked-detonation, +gap-crossing-blast, +optional-objectives, +fast-forward, +colorblind-palette]
proposes: ["+trigger:blast_reached", "+role:modifier", "+card:bomb-hat-modifier", "+card:single-chain-clear", "+feature:drag-offset"]
author: opus
date: 2026-11-19
---

# Bomb Club Deluxe — розстав бомби й капелюхи з руки на острівцях так, щоб усе на полі вибухнуло одним ланцюгом

## Суть
На полі з острівців плит уже стоять бомби; гравець перетягує на клітини бомби з руки й надіває на бомби капелюхи, а потім запускає ланцюгову реакцію. Мета — щоб за один ланцюг вибухнули всі бомби на полі; феєрверки на клітинах — додаткові очки. Кожен тип бомби вражає своєю фігурою (Blaze — хрестом до найближчої бомби в чотирьох напрямках, Laser — променем), а капелюх додає бомбі ефект (бант звʼязує бомби з однаковим бантом). Понад 20 бомб, дюжина капелюхів і 200+ рівнів на нелінійній мапі; ПК-версія мобільного Bomb Club (2021) з новими рівнями й діалогами.

## Поле і час
- Квадратна сітка, розбита на острівці плит; між острівцями — проміжки (gaps) без підлоги. Вид ізометричний 3D; праворуч кнопка камери (?).
- Дві фази: розстановка (без часу, скільки завгодно) → ланцюг (анімація, яку можна прискорити).
- Типи рівнів різні; відомий тип «Triple Trouble» — з таймером і фазами (з патчу мобільної версії).
- Склад руки задає рівень (на кадрах — від 2 до 6 карток бомб і капелюхів).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Basic Bomb | object | — | звичайна бомба; фігура вибуху (?) |
| Baby Bomb | object | — | рожева, із соскою; дія (?) |
| Laser Bomb | object | — | промінь уздовж ряду в обидва боки, над острівцями (за кадром) (?) |
| Blaze Bomb | object | — | хрест: вражає найближчу бомбу вгору, вниз, ліворуч, праворуч; над проміжками летить, крізь бомби — ні |
| Seed · Quake · Ice · Blow-up Bomb | object | — | назви зі списку Nitronomicon; дія (?) |
| Black Hole · Magma · Smoke Bomb | object | — | назви з опису; дія (?) |
| Nightmare Bomb | object | спить / ні | патч 1.1 зробив помітнішим, коли вона спить; правило (?) |
| Велика бомба з числом | object | число (5) | (?) |
| Бомби-черепи | object | — | з діалогу: «бомби, які ми не можемо підірвати»; правило (?) |
| Бант (Bow) | supply | колір | надівається на бомбу; підірвано одну — вибухають усі з таким самим бантом |
| Hard hat | supply | стос | каски ставляться стосом на бомбу; дія (?) |
| Party hat · Top hat · корона · нічний ковпак | supply | — | капелюхи-модифікатори; дія (?) |
| Феєрверк | pickup | — | стоїть на клітині; «запустити феєрверки» — більше очок |
| Плита острова | terrain | — | клітина, куди ставлять бомби |
| Проміжок | static | — | клітина без підлоги; бомбу не поставити (?), Blaze б'є над ним |
| Рука | supply | склад рівня | картки бомб і капелюхів на мотузці-шнурі внизу екрана |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag)` → ЯКЩО `free(cell)` → ТО `place(player, bomb)` — бомба з руки стає на плиту.
- КОЛИ `input(drag)` → ЯКЩО `occupied(cell, bomb)` → ТО `custom: «капелюх надівається на бомбу й додає їй ефект»`.
- КОЛИ `input(detonate)` → ТО `custom: «ланцюг запущено»` (?) як саме.
- КОЛИ `contact(blast, bomb)` → ТО `explode(shape)` — фігура залежить від типу бомби.
- КОЛИ `custom: «вибухає Blaze»` → ТО `custom: «по удару в найближчу бомбу в кожному з 4 напрямків; над проміжками летить, крізь бомби — ні»`.
- КОЛИ `custom: «вибухає Laser»` → ТО `custom: «промінь через увесь ряд в обидва боки»` (?).
- КОЛИ `destroyed(bomb)` → ЯКЩО `state(bomb, bow)` → ТО `explode(shape)` для всіх бомб з бантом того ж кольору.
- КОЛИ `contact(blast, firework)` → ТО `score(+n)` (?).
- КОЛИ `settled` (ланцюг завершився) → ЯКЩО `count(bomb, ==, 0)` → ТО `win`, `next_level`; інакше `custom: «рівень не пройдено — переставити й спробувати знову»`.
- КОЛИ `counter(timer, ==, 0)` → ЯКЩО `mode(triple_trouble)` → ТО `custom: «рівень закінчується»` (?).
- КОЛИ `input(restart)` → ТО `restart`.
- Перемога: після одного ланцюга на полі не лишилось бомб · Поразка: лишилась хоч одна — переставити (?) · Рахунок: феєрверки (?).

## Керування і ввід
- Перетягування бомб і капелюхів з руки на клітини (миша, тач); налаштування зсуву предмета під/над пальцем.
- Запуск ланцюга (?); кнопка прискорення ланцюга — одне натискання або гаряча клавіша (патч 1.1).
- Кнопки праворуч на полі: меню (≡), камера (?), рестарт; книга Nitronomicon — у лівому нижньому куті.
- Контролера нема (GamingOnLinux: на Steam Deck — емуляція миші й тач).

## Вікна, меню, HUD
- `game-screen`: острівці посередині; внизу — рука (картки на мотузці зі шнуром); зліва внизу — книга; праворуч — кнопки; угорі ліворуч — лічильник зі значком (?).
- `codex-window` Nitronomicon: книга з вкладками (бомби, капелюхи, третя з черепом — (?)); ліворуч список, праворуч — анімована картинка й опис з виділеними словами.
- `map-window`: кольорові регіони-острови з вузлами-рівнями на лініях; бульбашка над вузлом — нова бомба чи капелюх; ворота між регіонами відчиняються («Open again» — переглянути сцену); кнопки: вихід, налаштування, (?) колекція.
- `dialogue-window`: діалоги Maggie, Ian, Jon і Blake поверх поля; пропускаються.
- `settings-window`: зсув предмета при перетягуванні, швидкість прискорення, bloom, висококонтрастний інтерфейс, мова EN/FR.
- `tutorial-window`: підказки навчання в перших рівнях.
- `achievements-window` (Steam).

## Фічі поза полем
- 200+ рівнів на нелінійній `world-map` з опційними рівнями й викликами для досвідчених.
- Історія з діалогами, які можна пропустити; Nitronomicon (`codex`).
- `speed-control` ланцюга; `high-contrast`; Steam: «Color Alternatives», «Camera Comfort».
- `cloud-save`, `achievements`; `localization` EN/FR.
- Демо — уся перша зона; мобільний Bomb Club (2021) — free-to-play з покупками.

## Варіації й родичі
- [Bombuzal](bombuzal.md) — ланцюгова детонація аватаром у реальному часі; тут — розстановка курсором і один ланцюг; там теж є звʼязані бомби (`+linked-detonation`).
- [Bomberman](../maze-arcade/bomberman.md) — хрест вибуху й ланцюг бомб у аркаді.
- **Осі варіацій**: хто запускає ланцюг — аватар / курсор / таймер; фігура вибуху — сусіди / хрест до першої бомби / промінь через ряд / площа; модифікатори — капелюхи-ярлики / нема; мета — усе одним ланцюгом / очки / вижити.

## Цікавинки для курсу
- Ланцюг як черга подій (BFS): кожна вибухла бомба додає в чергу вражені — 📎.
- Хрест «до найближчої бомби» з прольотом над проміжками (Blaze) — 🌱.
- Капелюхи як модифікатори поверх типу (декоратор): бант звʼязує групу одного кольору — 🥉.
- Розвʼязувач розстановки руки: перебір розміщень бомб і капелюхів по вільних клітинах з перевіркою «усе одним ланцюгом» — 🥈.
- Енциклопедія елементів у грі (Nitronomicon) з даних → вікно — 📎.

## Мапа на каталог
- Є: `chain-detonation` ↔ ланцюг · `blast-wave` ↔ хрест Blaze · `drag-drop-piece`, `cursor-place`, `pocket` ↔ рука й перетягування · `world-map`, `level-unlock`, `map-window` ↔ мапа · `codex-window` ↔ Nitronomicon · `tutorial-window` · `event-points` ↔ феєрверки · `restart-level` · `game-screen`, `settings-window`, `language-picker`, `achievements-window`, `save-progress`, `background-music`.
- **Нема** → пропозиції карток:
  - `+single-chain-clear` «Очистити поле одним ланцюгом» · game-logic/win · 📎.
  - `+bomb-hat-modifier` «Модифікатор, який надівають на сутність (капелюх)» · entities/state · 🥉 · слот {modifier}.
  - `+gap-crossing-blast` «Вибух летить над проміжками, але не крізь бомби» · entities/combat · 🌱.
  - `+linked-detonation`, `+optional-objectives`, `+fast-forward`, `+colorblind-palette` — уже пропоновані в корпусі.

## Пропозиції до словників
- `+trigger:blast_reached` — вибух дістав клітину з бомбою чи феєрверком (повтор пропозиції з Bombuzal).
- `+role:modifier` — капелюх: не клітина й не обʼєкт поля, а модифікатор іншої сутності.
- `+card:bomb-hat-modifier`, `+card:single-chain-clear` — див. Мапу на каталог.
- `+feature:drag-offset` — зсув предмета над/під пальцем при перетягуванні (доступність тачу).

## Джерела
- ⭐ [Steam: Bomb Club Deluxe](https://store.steampowered.com/app/1771440/Bomb_Club_Deluxe/) — опис (бомби, капелюхи Party / Hard / Top, Nitronomicon, 200+ рівнів), 11 скриншотів: сторінка Blaze Bomb, діалог про бант, рука, мапа.
- [Офіційний сайт](http://bombclubdeluxe.sos-webcomic.com/) і [прескіт](http://bombclubdeluxe.sos-webcomic.com/presskit.html) — «Place your bombs on a grid … one single chain reaction; put hats … launch the fireworks to increase your score».
- [Мобільний Bomb Club](http://bombclub.sos-webcomic.com/) і [патчі](http://bombclub.sos-webcomic.com/releases.html) — Triple Trouble, перетягування, прискорення, двері мапи, Nitronomicon.
- [Pocket Gamer](https://www.pocketgamer.com/bomb-club/bomb-club-lets-you-bomb-everything-in-a-chain-reaction-of-explosions-out-now-on/) — мобільний запуск: 30 бомб, Blaze хрестом, капелюхи, 200+ рівнів.
- [GamingOnLinux](https://www.gamingonlinux.com/2022/03/bomb-club-deluxe-is-an-explosive-puzzle-game-out-now) — особливості з прескіту, Steam Deck без контролера.
- Steam News (appid 1771440) — патч 1.1: висококонтрастний інтерфейс, прискорення одним натисканням, сплячі Nightmare-бомби.
- YouTube: [трейлер](https://www.youtube.com/watch?v=9Z3Ovn-baZk).

## Непевне
- (?) Дія більшості бомб (Basic, Baby, Seed, Quake, Ice, Blow-up, Black Hole, Magma, Smoke, Nightmare) і капелюхів (Party, Hard, Top, корона, ковпак) — відомі лише назви й вигляд; текст бачив тільки для Blaze і банта.
- (?) Як запускається ланцюг — кліком по бомбі чи шнуром руки.
- (?) Laser — з кадру (промінь через ряд), не з тексту.
- (?) Велика бомба з числом, бомби-черепи, лічильник угорі ліворуч, третя вкладка книги.
- (?) Кількість бомб: «30» (Pocket Gamer, мобільна) проти «20+» (Steam, Deluxe).
- (?) Мобільний Bomb Club, схоже, знято з магазинів: пошук App Store за id порожній, Google Play — 404.
- (?) Чи поразка — будь-який залишок бомб; чи бувають рівні без руки.
