# Фічі поза полем

Можливості гри, що не є механікою на полі: керування ходом гри, режими, прогресія, збереження, редактор, доступність. Частина вже картками каталогу (game-pause, save-game, cheat-codes, level-select, difficulty-levels, score-records…) — див. `catalog-cards.md`; тут — ширший словник ⏳. Пропонувати через `+feature:`.

## Керування ходом гри

- `pause` · `restart-level` · `undo` (кроків: 1 / N / ∞) · `redo` · `rewind` (безперервно назад у часі: Braid, Catrap) · `step-mode` (по тіку) · `speed-control` · `skip-animation`.
- `hint` (одна гарантована клітина/хід) · `auto-check` (миттєва перевірка помилок) · `auto-solve` · `show-solution` · `mistake-limit` (3 помилки = програш).
- `seed-display` · `seed-input` (повторити ту саму генерацію) · `share-code` (код рівня/стану) · `replay` · `ghost-run` (привид найкращого проходження).

## Режими

- `mode-classic` · `mode-time-attack` · `mode-endless` · `mode-zen` (без програшу) · `mode-puzzle` (задані ситуації) · `mode-marathon` · `mode-versus` · `mode-coop` · `mode-daily` · `mode-sandbox` · `mode-hardcore` (один сейв, смерть остаточна) · `mode-speedrun` (таймер, спліти) · `mode-practice` (будь-який рівень без умов).

## Прогресія

- `levels-sequential` · `level-unlock` · `world-map` (вузли-рівні на мапі) · `stars-rating` (1–3 зірки за рівень) · `par-target` (пройти за N ходів) · `collectibles` (секрети в рівнях) · `unlockables` (нові фігури/скіни/режими) · `achievements` · `streaks` (серії днів) · `rank-tiers` · `xp-level` · `meta-progression` (постійні апгрейди між забігами).

## Збереження і статистика

- `autosave` · `save-slots` · `continue` · `cloud-save` · `stats` (перемоги/час/серії/найдовша змійка) · `history` (список партій) · `leaderboard-local` · `leaderboard-online` · `export-import` (рівні, партії PGN/XSB).

## Складність і доступність

- `difficulty-presets` · `custom-difficulty` (розмір поля, кількість мін) · `assist-mode` (повільніше, безсмертя, пропуск) · `colorblind-palette` · `high-contrast` · `grid-toggle` · `animation-toggle` · `screen-shake-toggle` · `font-scale` · `remap-controls` · `one-hand-mode` · `touch-controls` · `gamepad-support` · `mouse-and-keyboard`.

## Контент і спільнота

- `level-editor` · `level-sharing` (код/файл/онлайн) · `user-levels-browser` · `level-rating` · `daily-puzzle` · `puzzle-bank` · `mod-support` · `custom-skins` · `custom-rules` (конструктор варіантів: шахові правила, розмір поля).

## Люди

- `hotseat` · `local-multiplayer` · `online-multiplayer` · `spectator` · `ai-opponent-levels` · `turn-timer` · `chat` · `invite-link`.

## Подача

- `tutorial` · `onboarding-hints` (підказки в перших рівнях) · `rules-page` · `codex` (бестіарій елементів) · `localization` · `sound-toggle` · `music-toggle` · `volume-sliders` · `theme-select` · `fullscreen` · `window-size`.

## 🔥 Підтверджено корпусом (2026-11-02, 114 ігор)

`undo` ×6 · `world-map` ×5 · `custom-rules` ×4 · `meta-progression` ×3 · `mode-coop` ×3 · `skip-level` ×3 (нове) · `operator-settings` ×3 (нове: DIP-налаштування власника автомата) · `auto-check` ×3 · `stars-rating` ×3 · `share-result` ×3 (нове: поділитись емодзі-сіткою) · `streaks` ×3 · `match-trophies` · `reverse-mode` · `snapshots`. Рішення — [analysis/01-vocab-harvest.md](../analysis/01-vocab-harvest.md).
