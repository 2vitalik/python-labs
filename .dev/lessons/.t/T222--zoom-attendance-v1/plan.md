# T222 · Відвідування із Zoom v1: забір, звʼязка зі студентами, сторінки — план

`2026-10-14` · ⚙️ задача · ще не почата: чекає відповіді на [T220](../T220-Q--lessons-v1-questions.md) Q8 і облікових даних

Контекст:
- дослідження й дизайн — [T221](../T221-C--zoom-attendance.md); заняття на сайті — [T218](../T218--lessons-v1/report.md); зіставлення імен — `core/api/core/lesson_people.py`;
- запуск — окремою сесією: «реалізуй T222».

## Від Vitalik перед стартом

- Server-to-Server OAuth-застосунок у Zoom Marketplace (або user-level, якщо адміністратор не дасть): `Account ID`, `Client ID`, `Client Secret` — у `.env` сайту й локально (`ZOOM_ACCOUNT_ID`, `ZOOM_CLIENT_ID`, `ZOOM_CLIENT_SECRET`), не в чат.
- Скоупи застосунку: `meeting:read:list_past_participants:admin`, `meeting:read:past_meeting:admin` (екземпляри), за бажанням `cloud_recording:read:list_recording_files:admin`.
- ID зустрічі (постійне посилання) або UUID конкретного проведення; чи записи йдуть у хмару.
- Вибір порогу «був»: ≥ 25 % тривалості чи ≥ 20 хв (або інший).

## Кроки

- [ ] `core/api/core/zoom.py` — клієнт: токен за `account_credentials` (кеш на годину), `instances(meeting_id)`, `participants(uuid)` з пагінацією, `recordings(uuid)`; усе через `httpx`, помилки Zoom — у `HTTPException` з текстом.
- [ ] Модель `Attendance` (`attendance`): `lesson`, `name`, `nick`, `segments`, `seconds`, `late`, `meeting_uuid`, `fetched_at`; злиття сегментів одного імені; ведучий не рахується.
- [ ] `POST /api/lessons/{slug}/zoom` (адмін, агент): `{meeting: id|uuid, date?}` → екземпляр за датою заняття → учасники → `attendance` (заміна рядків заняття); відповідь — підсумок (усього, упізнано, невідомі); за прапорцем `sources: true` — VTT/чат/лінк на запис у джерела й `links`.
- [ ] `GET /api/lessons/{slug}/attendance` — рядки з `person()` за `aliases`/ПІБ (той самий `match`), невідомі окремо; для студента — лише опубліковане заняття й лише аватарки/хвилини.
- [ ] `GET /api/attendance` (адмін): матриця студенти × заняття, хвилини, частка; фільтри група/вид.
- [ ] `bin/zoom pull <slug> --meeting <id|uuid> [--sources]` — той самий маршрут через токен агента.
- [ ] Сторінка заняття: блок «👥 Були» (аватарки за групами, хвилини, бліді під порогом; адміну — невідомі з «хто це?», кнопка «Оновити із Zoom»).
- [ ] `/attendance` (адмін): теплокарта в стилі `WeekHeat`, підсумки на студента, клік → заняття/студент; пункт меню або посилання з `/lessons`.
- [ ] Смоук із підробленим клієнтом Zoom (без мережі): сегменти, поріг, невідомі, права.
- [ ] Доки: README вузла, CHANGELOG; T221 → «Інтегровано».
