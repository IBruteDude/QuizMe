from random import choice

from flet import (
  View, Page, ViewPopEvent, RouteChangeEvent, AppBar,
  Container, Row, Column, TextField, Text,
  UserControl, ElevatedButton, TextButton, KeyboardEvent,
  icons, colors, margin, padding, border, alignment,
  BoxShadow, MainAxisAlignment, CrossAxisAlignment, Offset, ShadowBlurStyle, FontWeight
)
from typing_app import TypingApp
from setting import page_style
from ui import QuizInterface
from Quiz import QuizRegister

from flet import app, Page, Theme


def main(page: Page):
  for key, value in page_style.items():
    setattr(page, key, value)

  page.window_center()
  typing_app = TypingApp()
  # quiz_app = QuizInterface(choice(quizs))
  page.on_keyboard_event = typing_app.on_keyboard

  def route_change(e: RouteChangeEvent):
    page.views.clear()
    page.views.append(
      View(
        route='/',
        controls=[
          Text(value="Welcome to QuizMe!", size=60),
          Row(controls=[
            ElevatedButton(text="Test your typing skills", on_click=lambda _: page.go('/typing_test')),
            ElevatedButton(text="Test your trivia skills", on_click=lambda _: page.go('/quizs'))
          ], alignment=MainAxisAlignment.CENTER)
        ],
        spacing=30,
        vertical_alignment=MainAxisAlignment.CENTER,
        horizontal_alignment=CrossAxisAlignment.CENTER
      )
    )
    match(page.route):
      case '/typing_test':
        page.views.append(
          View(
            route='/typing_test',
            controls=[typing_app]
          )
        )
    #   case '/quizs':
    #     page.views.append(
    #       View(
    #         route='/quizs',
    #         controls=[quiz_app]
    #       )
    #     )
    page.update()
    
  def view_pop(e: ViewPopEvent):
    page.views.pop()
    page.go(page.views[-1].route)

  typing_app.back_button.on_click = lambda _: page.go('/')
  page.on_route_change = route_change
  page.on_view_pop = view_pop
  page.go(page.route)


if __name__ == '__main__':
    app(target=main, assets_dir="font")
