# Елементи інтерфейсу (HUD і контролі)

Усе ⏳ (каталог має підзони interface/hud, interface/input, interface/render з частиною карток — див. `catalog-cards.md`). Елемент = віджет на вікні, монетка за елемент окремо від функції за ним (T82). Пропонувати через `+ui:`.

## Стан гри (індикатори)

- `lives` · `hp-bar` · `shield-bar` · `energy-bar` · `hunger-bar`.
- `score` · `hi-score` · `combo-meter` · `multiplier` · `coins`.
- `timer-countdown` · `timer-elapsed` · `turn-counter` · `move-counter` · `par-moves` (оптимум/найкраще).
- `level-number` · `wave-counter` · `next-wave-preview` · `progress-bar` (квота зібраного, % території).
- `remaining-counter` — лишилось мін/точок/ворогів/фішок.
- `objective-text` — поточна ціль словами.
- `turn-indicator` — хто ходить · `player-clock` — годинник кожного гравця · `captured-pieces`.
- `message-log` — журнал подій (роглайк) · `move-list` — нотація ходів.
- `stat-panel` — характеристики (сила, захист) · `equipment-slots` · `skill-bar` з іконками cooldown · `action-points`.

## Поле і підсвітки

- `grid-lines` · `cell-coordinates` (A1…) · `minimap` · `fog-overlay`.
- `selection-highlight` · `legal-move-highlight` · `path-preview` (куди піде) · `threat-range` (зона ураження) · `telegraph-marker` (куди вдарить ворог наступного ходу: Into the Breach).
- `cursor` · `drag-ghost` · `ghost-piece` (тінь, куди впаде: Tetris) · `next-piece-preview` · `hold-slot`.
- `danger-line` (межа програшу) · `spawn-indicator`.
- `pencil-marks` (кандидати в клітині) · `conflict-highlight` (порушені обмеження) · `mistake-counter`.
- `tooltip` (навести — пояснення) · `popup-text` (+100, Combo×3) · `toast` (повідомлення, що зникає).
- `legend` — що означають символи (консоль!) · `hint-marker` — підсвічена підказкою клітина.

## Контролі

- `undo-button` · `redo-button` · `restart-button` · `pause-button` · `hint-button` · `check-button` (перевірити розмітку) · `auto-solve-button`.
- `speed-slider` · `zoom-control` · `step-button` (один тік) · `fast-forward`.
- `mode-toggle` (олівець/ручка, прапорець/відкрити) · `tool-palette` (редактор) · `element-picker`.
- `inventory-bar` (швидкі слоти) · `item-hotkeys` · `ability-buttons`.
- `direction-pad` (екранні стрілки для тач) · `swipe-zone` · `virtual-joystick`.
- `end-turn-button` · `resign-button` · `offer-draw-button`.
- `chat-box` · `emote-wheel` (мультиплеєр).

## 🔥 Підтверджено корпусом (2026-11-02, 114 ігор)

`move-counter` ×6 · `conflict-highlight` ×4 · `energy-bar` ×3 · `inventory-bar` ×3 · `pocket` ×3 (нове: рука/взяті фігури) · `next-tile-preview` ×3 · `path-preview` ×3 · `action-text` ×3 · `instruction-highlight` ×3 (нове: поточна команда програми) · `hint-text` · `par-moves` · `garbage-meter` · `opponent-boards` · `player-portraits` · `line-clue`. Рішення — [analysis/01-vocab-harvest.md](../analysis/01-vocab-harvest.md).
