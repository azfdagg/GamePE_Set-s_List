import os
os.system("pip install flet")

import flet as ft
import json
import difflib

def main(page: ft.Page):
    # Настройки страницы
    page.title = "Поиск сетов"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20
    page.bgcolor = ft.Colors.GREY_900  # Темный фон

    # Загрузка данных из файла data.json
    with open("data.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    # Функция для копирования текста в буфер обмена
    def copy_to_clipboard(text):
        page.set_clipboard(text)
        page.snack_bar = ft.SnackBar(ft.Text(f"Скопировано: {text}", color=ft.Colors.WHITE))
        page.snack_bar.open = True
        page.update()

    # Функция для поиска и отображения данных
    def search(e):
        search_term = search_field.value.lower()
        results.controls.clear()

        # Поиск точного совпадения
        if search_term in data:
            for item in data[search_term]:
                # Добавляем текст с возможностью копирования через кнопку
                results.controls.append(
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Text(item, selectable=True, color=ft.Colors.WHITE),
                                ft.IconButton(
                                    icon=ft.Icons.COPY,
                                    icon_color=ft.Colors.BLUE_200,
                                    on_click=lambda e, text=item: copy_to_clipboard(text),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        border=ft.border.all(1, ft.Colors.BLUE_200),  # Обводим рамкой
                        padding=10,
                        border_radius=10,
                        margin=5,
                    )
                )
        else:
            # Поиск близких по значению слов
            close_matches = difflib.get_close_matches(search_term, data.keys(), n=3, cutoff=0.6)
            if close_matches:
                results.controls.append(
                    ft.Text("Возможно, вы имели в виду:", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD))
                for match in close_matches:
                    results.controls.append(ft.Text(f"{match}:", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD))
                    for item in data[match]:
                        results.controls.append(
                            ft.Container(
                                content=ft.Row(
                                    [
                                        ft.Text(item, selectable=True, color=ft.Colors.WHITE),
                                        ft.IconButton(
                                            icon=ft.Icons.COPY,
                                            icon_color=ft.Colors.BLUE_200,
                                            on_click=lambda e, text=item: copy_to_clipboard(text),
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                ),
                                border=ft.border.all(1, ft.Colors.BLUE_200),  # Обводим рамкой
                                padding=10,
                                border_radius=10,
                                margin=5,
                            )
                        )
            else:
                results.controls.append(ft.Text("Ничего не найдено", color=ft.Colors.WHITE))
        page.update()

    # Функция для отображения всех блоков
    def show_all_blocks(e):
        results.controls.clear()
        for key, values in data.items():
            results.controls.append(ft.Text(f"{key}:", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD))
            for value in values:
                results.controls.append(
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Text(value, selectable=True, color=ft.Colors.WHITE),
                                ft.IconButton(
                                    icon=ft.Icons.COPY,
                                    icon_color=ft.Colors.BLUE_200,
                                    on_click=lambda e, text=value: copy_to_clipboard(text),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        border=ft.border.all(1, ft.Colors.BLUE_200),  # Обводим рамкой
                        padding=10,
                        border_radius=10,
                        margin=5,
                    )
                )
        page.update()

    # Функция для скрытия списка
    def hide_blocks(e):
        results.controls.clear()
        page.update()

    # Поле для ввода поискового запроса
    search_field = ft.TextField(
        label="Введите запрос",
        label_style=ft.TextStyle(color=ft.Colors.WHITE),
        border_color=ft.Colors.BLUE_200,
        cursor_color=ft.Colors.WHITE,
        text_style=ft.TextStyle(color=ft.Colors.WHITE),
        on_submit=search,
        width=300,
    )

    # Кнопка для поиска
    search_button = ft.ElevatedButton(
        "Поиск",
        on_click=search,
        bgcolor=ft.Colors.BLUE_800,
        color=ft.Colors.WHITE,
        elevation=5,
    )

    # Кнопка для показа всех блоков
    show_all_button = ft.ElevatedButton(
        "Показать все блоки",
        on_click=show_all_blocks,
        bgcolor=ft.Colors.BLUE_800,
        color=ft.Colors.WHITE,
        elevation=5,
    )

    # Кнопка для скрытия списка
    hide_button = ft.ElevatedButton(
        "Скрыть список",
        on_click=hide_blocks,
        bgcolor=ft.Colors.BLUE_800,
        color=ft.Colors.WHITE,
        elevation=5,
    )

    # Контейнер для отображения результатов (с прокруткой)
    results = ft.ListView(expand=True, spacing=10, padding=20)

    # Добавление элементов на страницу
    page.add(
        # Заголовок "Поиск сетов"
        ft.Text("Поиск сетов", size=24, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),

        # Кнопки и поле ввода
        ft.Row(
            [
                # Кнопки слева сверху
                ft.Column(
                    [
                        show_all_button,
                        hide_button,
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
                # Поле ввода и кнопка поиска по центру
                ft.Column(
                    [
                        ft.Row([search_field, search_button], alignment=ft.MainAxisAlignment.CENTER),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    expand=True,
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
        ),
        results,  # Список результатов с прокруткой

        # Ники снизу слева
        ft.Row(
            [
                ft.Text("@azfdagg", color=ft.Colors.WHITE),
                ft.Text("@DeepSeek", color=ft.Colors.WHITE),
            ],
            alignment=ft.MainAxisAlignment.START,
        ),
    )


ft.app(target=main)