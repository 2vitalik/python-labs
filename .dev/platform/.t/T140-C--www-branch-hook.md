# T140 · Статика для VPS: bin/www збирає з коміту, pre-push-хук публікує гілку www

`2026-09-25` · 🔆 пояснення

Контекст: сайт переїжджає на VPS `vv3` (vps-infra [T61](../../../../My/vps-infra/.dev/apps/python-labs/.t/T61--python-labs/plan.md)); Node на сервері нема, тож Vite-збірка робиться на ноутбуці і їде окремою гілкою. Рішення й покроковий розбір (кожен рядок пояснено) — у vps-infra: [T59](../../../../My/vps-infra/.dev/vv/.t/T59-P--ci-www-branch.md) контракт, [T62](../../../../My/vps-infra/.dev/vv/.t/T62-B--www-producer.md) чому не GitHub Actions, [T63](../../../../My/vps-infra/.dev/vv/.t/T63--www-hook/report.md) реалізація (логи 01–04). Тут — що з цього живе в **цьому** репо і як ним користуватись.

## Що є в репо

- **`bin/www [commit]`** (32 рядки bash): бере дерево `app/vue` з **коміту** (дефолт `HEAD`) через `git archive`, розпаковує в tmp, підкладає symlink на `app/vue/node_modules`, `npm run build`, потім робить із `dist/` коміт **без батька** з повідомленням = повний sha джерела і `git push -f origin <commit>:refs/heads/www`. Робоче дерево не читається: незакомічені зміни в `app/vue` у гілку не потрапляють. Локальний `app/vue/dist/` не чіпається.
- **`bin/hooks/pre-push`** (10 рядків): на кожен `git push` у `main` викликає `bin/www <sha, що пушиться>` — гілка `www` оновлюється в ту саму мить, що й `main`. Якщо збірка або push `www` впали — push `main` скасовується.
- **Гілка `www` на GitHub** — службова: завжди **один** коміт (лише `index.html` + `assets/`), force-push замінює його; історія не росте, старі коміти прибирає `gc`. Subject коміту = sha `main`, з якого зібрано, — за цим сервер звіряє «код + статика з одного коміту».

## Як користуватись

- Нічого: `git push` у `main` робить усе сам. У виводі буде два блоки `To github.com:…` — спершу `www` (`forced update` — нормальне слово, не помилка), потім `main`.
- Новий клон / інша машина — раз: `git config core.hooksPath bin/hooks` (+ Node і `npm ci` у `app/vue`).
- Перевірити, що гілка свіжа: `git log -1 --format=%s origin/www` має дорівнювати `git rev-parse origin/main`.
- Якщо `www` відстала (push з `--no-verify`, клон без хука, `git push` без нових комітів): `bin/www origin/main`.

## Межі

- `node_modules` ноутбука мусить відповідати `package-lock.json` коміту: після зміни lock-файла на іншій машині — `npm ci`. Бракує залежності → збірка падає → push не проходить (гучно); стара версія → збереться тихо. «Як у CI» — `npm ci` у tmp замість symlink, +10–20 с на push.
- `.DS_Store` у `dist/` захисту нема — варто мати глобальний `core.excludesFile`.
- Серверна половина (гілка → `/srv/python-labs/www/`) — vps-infra, T58 крок 0b; до неї блок 5 T61 кладе гілку руками.

## Твої думки та питання

> 
