from random import choice

from flet import *
from typing_app import TypingApp
from setting import page_style


def main(page: Page):
  # set all the page attributes
  for key, value in page_style.items():
    setattr(page, key, value)
  page.window_center()
  # initialise an instance of the app and register it's keyboard control
  typing_app = TypingApp()
  page.on_keyboard_event = typing_app.on_keyboard

  def route_change(e: RouteChangeEvent):
    # handle the routeing in the application
    page.views.clear()
    page.views.append(
      View(
        # "/" is the root of the app first page appear
        route='/',
        controls=[
          Text(value="Welcome to Typeer!", size=60),
          Row(controls=[
            ElevatedButton(text="Test your typing skills ", on_click=lambda _: page.go('/typing_test')),
          ], alignment=MainAxisAlignment.CENTER)
        ],
        vertical_alignment=MainAxisAlignment.CENTER,
        horizontal_alignment=CrossAxisAlignment.CENTER
      )
    )
    if page.route == '/typing_test':
        page.views.append(
          View(
            route='/typing_test',
            controls=[typing_app]
          )
        )
    page.update()

  def view_pop(e: ViewPopEvent):
    # a function for going back one page
    page.views.pop()
    page.go(page.views[-1].route)
  typing_app.back_button.on_click = lambda _: page.go('/')
  page.on_route_change = route_change
  page.on_view_pop = view_pop
  page.go(page.route)


if __name__ == '__main__':
    app(target=main, assets_dir="font")
