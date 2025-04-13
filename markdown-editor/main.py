import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import markdown
import tempfile
import os
import webbrowser
from tkinter.font import Font

class MarkdownEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("WYSIWYG Markdown Editor")
        self.root.geometry("1000x700")

        self.current_file = None
        self.preview_visible = False
        self.preview_file = None
        self.setup_ui()

    def setup_ui(self):
        # Создаем панель инструментов
        toolbar = ttk.Frame(self.root)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Кнопки панели инструментов (с иконками)
        file_buttons = [
            ("📂", "Открыть", self.open_file),
            ("💾", "Сохранить", self.save_file),
            ("🖫", "Сохранить как", self.save_file_as),
            ("👁", "Предпросмотр", self.toggle_preview),
        ]

        for icon, text, command in file_buttons:
            btn = ttk.Button(toolbar, text=f"{icon} {text}", command=command)
            btn.pack(side=tk.LEFT, padx=2, pady=2)

        # Разделитель
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, padx=5, fill=tk.Y)

        # Кнопки форматирования (только иконки)
        format_buttons = [
            ("#️⃣", "Заголовок 1", lambda: self.insert_markdown("# ", "")),
            ("##️⃣", "Заголовок 2", lambda: self.insert_markdown("## ", "")),
            ("###️⃣", "Заголовок 3", lambda: self.insert_markdown("### ", "")),
            ("𝐁", "Жирный", lambda: self.insert_markdown("**", "**")),
            ("𝐼", "Курсив", lambda: self.insert_markdown("*", "*")),
            ("🔗", "Ссылка", lambda: self.insert_markdown("[", "](url)")),
            ("</>", "Код", lambda: self.insert_markdown("`", "`")),
            ("☰", "Список", self.insert_list),
            ("❝", "Цитата", self.insert_quote),
            ("---", "Разделитель", lambda: self.insert_markdown("\n---\n", "")),
        ]

        for icon, tooltip, command in format_buttons:
            btn = ttk.Button(toolbar, text=icon, command=command, width=3)
            btn.pack(side=tk.LEFT, padx=1, pady=2)
            self.create_tooltip(btn, tooltip)

        # Разделитель
        ttk.Separator(self.root, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)

        # Основной фрейм для редактора
        self.editor_frame = ttk.Frame(self.root)
        self.editor_frame.pack(fill=tk.BOTH, expand=True)

        # Текстовый редактор
        self.text_editor = tk.Text(
            self.editor_frame,
            wrap=tk.WORD,
            font=Font(family="Arial", size=12),
            undo=True
        )
        self.text_editor.pack(fill=tk.BOTH, expand=True)

        # Настройки прокрутки
        scrollbar = ttk.Scrollbar(self.text_editor)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar.config(command=self.text_editor.yview)
        self.text_editor.config(yscrollcommand=scrollbar.set)

        # Привязываем обновление предпросмотра
        self.text_editor.bind("<KeyRelease>", self.update_preview)

        # Статус-бар
        self.status_bar = ttk.Label(self.root, text="Готов", relief=tk.SUNKEN)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def create_tooltip(self, widget, text):
        """Создает всплывающую подсказку для виджета"""
        tooltip = tk.Toplevel(widget)
        tooltip.withdraw()
        tooltip.overrideredirect(True)

        label = ttk.Label(tooltip, text=text, background="#ffffe0", relief="solid", padding=3)
        label.pack()

        def enter(event):
            x = widget.winfo_rootx() + 10
            y = widget.winfo_rooty() + widget.winfo_height() + 5
            tooltip.geometry(f"+{x}+{y}")
            tooltip.deiconify()

        def leave(event):
            tooltip.withdraw()

        widget.bind("<Enter>", enter)
        widget.bind("<Leave>", leave)

    def insert_markdown(self, prefix, suffix):
        """Вставляет Markdown-теги вокруг выделенного текста"""
        try:
            # Проверяем, есть ли выделение
            if self.text_editor.tag_ranges(tk.SEL):
                start = self.text_editor.index(tk.SEL_FIRST)
                end = self.text_editor.index(tk.SEL_LAST)
                selected = self.text_editor.get(start, end)

                # Удаляем выделение и вставляем форматированный текст
                self.text_editor.delete(start, end)
                self.text_editor.insert(start, prefix + selected + suffix)

                # Выделяем вставленный текст (без префикса/суффикса)
                self.text_editor.tag_add(tk.SEL,
                                         f"{start} + {len(prefix)}c",
                                         f"{end} + {len(prefix) + len(suffix)}c")
            else:
                # Если нет выделения, просто вставляем префикс и суффикс
                cursor_pos = self.text_editor.index(tk.INSERT)
                self.text_editor.insert(cursor_pos, prefix + suffix)

                # Устанавливаем курсор между префиксом и суффиксом
                self.text_editor.mark_set(tk.INSERT, f"{cursor_pos} + {len(prefix)}c")
        except Exception as e:
            # Если что-то пошло не так, просто вставляем текст в позицию курсора
            cursor_pos = self.text_editor.index(tk.INSERT)
            self.text_editor.insert(cursor_pos, prefix + suffix)
            self.text_editor.mark_set(tk.INSERT, f"{cursor_pos} + {len(prefix)}c")
            self.status_bar.config(text=f"Ошибка форматирования: {str(e)}")

        self.text_editor.focus_set()

    def insert_list(self):
        """Вставляет маркированный список"""
        self.insert_markdown("- ", "")

    def insert_quote(self):
        """Вставляет цитату"""
        self.insert_markdown("> ", "")

    def update_preview(self, event=None):
        """Обновляет предпросмотр Markdown"""
        if self.preview_visible:
            try:
                # Создаем временный HTML-файл
                markdown_text = self.text_editor.get("1.0", tk.END)
                html = markdown.markdown(markdown_text)

                # Добавляем базовый CSS для лучшего отображения
                html = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="utf-8">
                    <title>Markdown Preview</title>
                    <style>
                        body {{ font-family: Arial, sans-serif; line-height: 1.6; padding: 20px; max-width: 800px; margin: 0 auto; }}
                        h1, h2, h3 {{ color: #333; }}
                        code {{ background: #f4f4f4; padding: 2px 5px; border-radius: 3px; }}
                        pre {{ background: #f4f4f4; padding: 10px; border-radius: 5px; overflow-x: auto; }}
                        blockquote {{ border-left: 3px solid #ccc; padding-left: 15px; color: #666; }}
                    </style>
                </head>
                <body>
                    {html}
                </body>
                </html>
                """

                # Сохраняем во временный файл
                if self.preview_file is None:
                    self.preview_file = tempfile.NamedTemporaryFile(
                        suffix=".html",
                        delete=False,
                        mode='w',
                        encoding='utf-8'
                    )

                with open(self.preview_file.name, 'w', encoding='utf-8') as f:
                    f.write(html)

                # Открываем в браузере
                webbrowser.open(f"file://{os.path.abspath(self.preview_file.name)}")

            except Exception as e:
                self.status_bar.config(text=f"Ошибка предпросмотра: {str(e)}")

    def toggle_preview(self):
        """Переключает видимость предпросмотра"""
        self.preview_visible = not self.preview_visible
        if self.preview_visible:
            self.update_preview()
            self.status_bar.config(text="Предпросмотр открыт в браузере")
        else:
            if self.preview_file:
                try:
                    os.unlink(self.preview_file.name)
                    self.preview_file = None
                except:
                    pass
            self.status_bar.config(text="Предпросмотр закрыт")

    def open_file(self):
        """Открывает файл Markdown"""
        file_path = filedialog.askopenfilename(
            filetypes=[("Markdown Files", "*.md"), ("Text Files", "*.txt"), ("All Files", "*.*")]
        )

        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                    self.text_editor.delete("1.0", tk.END)
                    self.text_editor.insert("1.0", content)
                self.current_file = file_path
                self.status_bar.config(text=f"Открыт: {file_path}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось открыть файл:\n{str(e)}")

    def save_file(self):
        """Сохраняет файл Markdown"""
        if self.current_file:
            try:
                content = self.text_editor.get("1.0", tk.END)
                with open(self.current_file, "w", encoding="utf-8") as file:
                    file.write(content)
                self.status_bar.config(text=f"Сохранено: {self.current_file}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{str(e)}")
        else:
            self.save_file_as()

    def save_file_as(self):
        """Сохраняет файл Markdown с указанием имени"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".md",
            filetypes=[("Markdown Files", "*.md"), ("Text Files", "*.txt"), ("All Files", "*.*")]
        )

        if file_path:
            try:
                content = self.text_editor.get("1.0", tk.END)
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(content)
                self.current_file = file_path
                self.status_bar.config(text=f"Сохранено: {file_path}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{str(e)}")

    def __del__(self):
        """Удаляем временный файл предпросмотра при закрытии"""
        if self.preview_file:
            try:
                os.unlink(self.preview_file.name)
            except:
                pass

def main():
    root = tk.Tk()
    app = MarkdownEditor(root)
    root.mainloop()

if __name__ == "__main__":
    main()
