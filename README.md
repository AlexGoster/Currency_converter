# Currency Converter

Tkinter-конвертер по локальным курсам rates.json. Курсы статические и не загружаются из финансовых сервисов. Ошибочные файлы, нулевые/отрицательные курсы и неконечные суммы отклоняются.

Требуется Python с Tkinter для GUI-проектов.

```bash
python main.py
```

Проверка:

```bash
python -m pip install -r requirements-dev.txt
python -m pytest
```

GUI-тесты создают настоящие виджеты в скрытых окнах.
