# T218 · Заняття на сайті v1: моделі, API, сторінки, bin/lesson — план

`2026-10-14` · ⚙️ задача · звіт — [report.md](report.md)

Контекст:
- дизайн — [T182](../T182-P--lessons-design.md) §«План», етап 1; бриф Vitalik 2026-10-14 і його дельта — [T219](../T219-P--lessons-brief-v2.md); вибори — [T220](../T220-Q--lessons-v1-questions.md);
- взірці: методичка в Mongo з інлайн-редактором і `history` ([T128](../../platform/.t/T128--guide-editor-v1/report.md)), токен агента й `bin/guide` ([T153](../../platform/.t/T153--agent-guide-access/report.md)), картинки ods у Mongo (`Media`, [T170](../../ods/.t/T170--ods-base/report.md));
- сирі транскрипти ПЗ 1 курсу Python уже лежать у `data/transcripts/pz1/raw/` (zoom · plaud · tana · wispr) — тека додана в `.gitignore` цією сесією.

## Кроки

- [ ] `.gitignore`: `data/transcripts/` (імена студентів).
- [ ] Ядро, моделі: `Lesson` (slug = вид+номер: `pz1`, `lab2`; дата, час, назва, групи, посилання, старт відео, контекст, транскрипт, конспект, нотатки, чат, `published`, `rev`), `LessonFile` (сирі джерела · вкладення; байти в Mongo, як `Media` ods), `User.aliases` (імена в Zoom → студент).
- [ ] Ядро, API `/api/lessons`: список і заняття (`active`; чернетки — лише адміну й агенту), створити/змінити/видалити (адмін + агент, `rev` → 409, `history`), файли (завантажити · скачати · прибрати), «мовці» → студенти за `aliases` і ПІБ, призначити псевдонім.
- [ ] `bin/lesson`: `ls` · `new` · `pull` · `push` · `attach` · `publish` — тека `data/transcripts/<slug>/` як у skill `/lesson` (`raw/`, `meta.yml`, `context.md`, `transcript.md`, `summary.md`, `notes.md`, `chat.txt`).
- [ ] Ядро, сторінки: `/lessons` (перелік із чипами виду, 📝 🗣 🎬 📎), `/lessons/<slug>` (шапка з посиланнями й вкладеннями, конспект, згорнутий транскрипт як чат з аватарками й лінками на студентів, зміст, чат Zoom, адмінська картка джерел і мовців, інлайн-редактор конспекту й транскрипта, «Показати студентам»), `/lessons/new` і `/lessons/<slug>/edit` (форма).
- [ ] Сайти: маршрути й пункт меню «Заняття» у python і ods; `colls.lessons`; поле «Імена в Zoom» у картці студента.
- [ ] Смоук `tests/smoke_lessons.py`: доступ, чернетки, `rev`, файли, мовці, агент.
- [ ] Стенд: сторінка з реальним транскриптом (ods, заняття 1) — знімки; дев-база python: `pz1` із сирими джерелами через `bin/lesson -t dev`.
- [ ] Доки: README вузла, CHANGELOG, STATUS.
