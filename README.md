# WYSIWYG Markdown Editor

![Editor Screenshot](screenshot.png)

Простой WYSIWYG-редактор Markdown с предпросмотром, написанный на Python с использованием Tkinter.

## Возможности

- 📝 Редактирование текста с подсветкой синтаксиса
- 🔍 Режим предпросмотра (рендеринг Markdown в HTML)
- 🖇️ Быстрое форматирование с помощью панели инструментов:
    - Заголовки (H1-H3)
    - Жирный, курсив, код
    - Списки, цитаты, разделители
    - Ссылки
- 💾 Сохранение и загрузка файлов (.md, .txt)
- 📁 Работа с несколькими файлами
- 🎨 Простое и интуитивное управление

## Установка

1. Убедитесь, что у вас установлен Python 3.8 или новее
2. Установите необходимые зависимости:

```bash
pip install markdown
```

3. Запустите редактор:

```bash
python markdown_editor.py
```
## Использование

1. **Панель инструментов** - содержит кнопки для основных операций:
    - Открыть/сохранить файл
    - Форматирование текста
    - Переключение предпросмотра

2. **Редактор** - основная область для ввода текста с Markdown-разметкой

3. **Предпросмотр** - автоматически обновляемый просмотр отформатированного текста (открывается в браузере)

4. **Горячие клавиши:**
    - Ctrl+O - открыть файл
    - Ctrl+S - сохранить файл
    - Ctrl+Shift+S - сохранить как
    - Ctrl+P - предпросмотр

5. **Скриншоты**
    - Редактор
    - Предпросмотр

## Особенности реализации

- Использует стандартную библиотеку Tkinter для GUI
- Преобразование Markdown в HTML через python-markdown
- Временные файлы для предпросмотра автоматически удаляются
- Поддержка Unicode-символов для иконок

## Лицензия

MIT License. Смотрите файл LICENSE.

