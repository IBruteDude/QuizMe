from flet import *
import flet as ft




def main(page: Page):
    page.window_width = 700
    page.window_height = 500
    page.title = "Quiz Me"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    textInputLogin = TextField(value='name',width=400)
    textInputPassword = TextField(value='password',width=400)
    btnSubmit = ElevatedButton(text="submit")
    column =Container(content= Column(
            horizontal_alignment=CrossAxisAlignment.CENTER,
            controls=[textInputLogin, textInputPassword,btnSubmit])
    )
    page.add(column)

if __name__ == "__main__":
    app(target=main)



# import flet as ft
# from flet import *
#
#
# t = Text(
#     'hello',size=30,color=ft.colors.BLUE
# )
#
# def main(page: Page):
#     page.window_width = 500
#     page.window_height = 500
#     page.add(t)
#
#
# app(target=main)
