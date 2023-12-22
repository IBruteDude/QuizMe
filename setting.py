from flet import *
from get_quotes import *

color_purple = colors.SHADOW
color_white = colors.WHITE

text_style = {
  'font_family': 'font',
  'size': 10,
  'text_align': TextAlign.CENTER,
  'weight': FontWeight.NORMAL,
  'color': colors.GREY_700,
}

score_style = {
  'font_family': 'font',
  'size': 20,
  'text_align': TextAlign.CENTER,
  'weight': FontWeight.NORMAL,
  'color': colors.WHITE,
}

container_style = {
  "width": 150,
  "height": 50,
  "bgcolor": color_purple,
  "border_radius": 10,
  "padding": padding.all(10),
  "shadow": BoxShadow(
    spread_radius=1,
    blur_radius=15,
    color=colors.BLACK,
    offset=Offset(0, 0),
    blur_style=ShadowBlurStyle.INNER,
  ),
}

page_style = {
  'padding': 20,
  'title': "Typeer",
  'window_width': 1280,
  'window_height': 800,
  'scroll': 'always',
  'fonts': { "font": "/font/Inconsolata.ttf" },
  'theme_mode': 'dark',
  'theme': Theme(font_family="font", ),
}

char_style = lambda c: {
  'border_radius': 5,
  'padding': padding.only(left=5, right=5),
  'margin': margin.only(left=-4, right=-4),
  'bgcolor': colors.TRANSPARENT,
  'content': Text(
    value=c,
    size=30,
    weight=FontWeight.BOLD,
    color=colors.GREY_700,
    no_wrap=True,
  )
  # 'bgcolor': colors.with_opacity(0.1, colors.GREY_100),
}

user_buttons = {
  'start': {
    'text': "Start",
    'icon': icons.PLAY_ARROW,
    'icon_color': colors.WHITE,
  },
  'reset': {
    'text': "Reset",
    'icon': icons.RESTART_ALT,
    'icon_color': colors.WHITE,
    'tooltip': "Restart Test",
  },
}

user_inputs = {
    'prefix_icon': icons.ABC,
    'text_size': 20,
    'cursor_color': colors.GREEN,
    'width': 500,
    'content_padding': 5,
    'border_radius': 10,
    'border_color': colors.WHITE,
    'selection_color': colors.GREEN,
    'disabled': True
}

# Sample words for typing practice
words_to_type = generated_quote[0].lower()
