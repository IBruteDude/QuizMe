import threading
from time import sleep

from flet import (
  Container, Row, Column, TextField, Text,
  Control, UserControl, ElevatedButton, TextButton, KeyboardEvent,
  icons, colors, margin, padding, border, alignment,
  BoxShadow, MainAxisAlignment, CrossAxisAlignment, Offset, ShadowBlurStyle, FontWeight
)

from setting import (
  score_style, container_style, text_style, char_style, user_buttons,
  user_inputs, words_to_type, quote_generator, generated_quote
)


class StatPanel:
  def __init__(self, label_text: str, stat_format: str, var_ref):
    self.func = var_ref
    self.format = stat_format
    self.label = Text(label_text, **score_style)
    self.stat_text = Text(stat_format.format(self.func()), **score_style)
    self.controls = [
      Container(
        content=self.label,
        **container_style,
      ),
      Container(
        content=self.stat_text,
        **container_style,
      ),
    ]


  def update(self, val=None):
    if val:
      self.stat_text.value = self.format.format(val)
    else:
      self.stat_text.value = self.format.format(self.func())


class Cursor:
  def __init__(self, char_slots: list[Control], displayed_text: str):
    self.text = displayed_text.strip()
    self.chars = char_slots
    for char in self.text:
      self.chars.append(Container(**char_style(char)))
    self.curr = 0


  def refresh(self):
    for char in self.chars:
      char.bgcolor = colors.TRANSPARENT
      char.content.color = colors.GREY_700
    self.curr = 0
    self.chars[0].border = border.only(bottom=border.BorderSide(1))


  def clear(self, new_text: str):
    self.text = new_text.strip()
    self.chars.clear()
    for char in self.text:
      self.chars.append(Container(**char_style(char)))
    self.curr = 0


  def trigger(self, key: str):
    if self.curr == len(self.text) - 1:
      self.chars[self.curr].__dict__.update({
        'bgcolor': colors.GREEN_700,
        'border': border.only(bottom=border.BorderSide(1)),
        'color': colors.GREY_700,
        'content.color': colors.WHITE,
      })
      return

    if "Backspace" == key:
      self.chars[self.curr].border = border.only(bottom=border.BorderSide(1))
      self.chars[self.curr - 1].border = border.only(bottom=border.BorderSide(5, "white"))
      self.chars[self.curr - 1].bgcolor = colors.TRANSPARENT
      self.chars[self.curr - 1].content.color = colors.GREY_700
      if self.curr > 0:
        self.curr -= 1
    elif key.lower() == self.text[self.curr]:
      self.chars[self.curr].bgcolor = colors.GREEN_700

      self.chars[self.curr + 1].border = border.only(bottom=border.BorderSide(5, "white"))
      self.chars[self.curr].border = border.only(bottom=border.BorderSide(1))
      self.chars[self.curr].color = colors.GREY_700
      self.chars[self.curr].content.color = colors.WHITE
      self.curr += 1
    elif key.lower() != self.text[self.curr]:
      self.chars[self.curr].bgcolor = colors.RED_700

      self.chars[self.curr + 1].border = border.only(bottom=border.BorderSide(5, "white"))
      self.chars[self.curr].border = border.only(bottom=border.BorderSide(1))
      self.chars[self.curr].content.color = colors.WHITE
      self.curr += 1
    else:
      self.chars[self.curr].bgcolor = colors.GREY_700
      self.chars[self.curr].content.color = colors.WHITE


class TypingApp(UserControl):
  def __init__(self):
    super().__init__()
    self.StartRound = True
    self.quote_text = words_to_type

    # UI controls
    self.text_displayed = Row(wrap=True)
    self.start_button = ElevatedButton(**user_buttons['start'])
    self.start_button.on_click = self.start
    self.reset_button = ElevatedButton(**user_buttons['reset'])
    self.reset_button.on_click = self.reset
    self.input = TextField(**user_inputs)

    # Labels for displaying scores
    self.total_time = 60
    self.wrong_words = 0
    self.total_words = 0
    self.time = 0
    self.wpm = 0

    self.elapsed_time_stat = StatPanel("Elapsed Time", "{}", lambda: self.time)
    self.remaining_time_stat = StatPanel("Remaining Time", "{}", lambda: self.total_time - self.time)
    self.total_words_stat = StatPanel("Total Words", "{}", lambda: self.total_words)
    self.wpm_stat = StatPanel("WPM", "{:.2f}", lambda: self.wpm)
    self.wrong_words_stat = StatPanel("Wrong Words", "{}", lambda: self.wrong_words)
    self.accuracy_stat = StatPanel("Accuracy", "{:.2f}%", lambda: self.__calculate_accuracy(len(self.quote_text), self.wrong_words))

    # Game variables
    self.stats = [
      self.elapsed_time_stat,
      self.remaining_time_stat,
      self.wpm_stat,
      self.total_words_stat,
      self.wrong_words_stat,
      self.accuracy_stat,
    ]

    # Threading setup
    self.back_button = TextButton(icon=icons.ARROW_BACK, icon_color=colors.WHITE)
    self.stop_flag_timer = threading.Event()
    self.stop_flag_count = threading.Event()
    self.layout = Column(
      alignment="center",
      horizontal_alignment="center",
      controls=[
        Container(
          margin=margin.only(top=10, bottom=10),
          border_radius=10,
          bgcolor=colors.SHADOW,
          content=Row(
            controls=[
              Row(
                controls=[
                  self.back_button,
                  TextButton(
                    text="TIME",
                    icon=icons.TIMER,
                    icon_color=colors.YELLOW_700,
                    disabled=True,
                  ),
                  TextButton(
                    text="15",
                    on_click=lambda x: (self.refresh(), self.change_game_time(15))[1],
                  ),
                  TextButton(
                    text="30",
                    on_click=lambda x: (self.refresh(), self.change_game_time(30))[1],
                  ),
                  TextButton(
                    text="60",
                    on_click=lambda x: (self.refresh(), self.change_game_time(60))[1],
                  ),
                ]
              )
            ]
          ),
        ),
        Container(
          margin=margin.only(top=10, bottom=10),
          border_radius=10,
          padding=padding.all(10),
          shadow=BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=colors.BLACK,
            offset=Offset(0, 0),
            blur_style=ShadowBlurStyle.OUTER,
          ),
          content=self.text_displayed,
        ),
        Row(
          alignment=MainAxisAlignment.END,
          controls=[
            Container(
              margin=margin.only(bottom=10),
              border_radius=10,
              padding=padding.all(10),
              shadow=BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=colors.BLACK,
                offset=Offset(0, 0),
                blur_style=ShadowBlurStyle.OUTER,
              ),
              content=Text(value=f"author: {generated_quote[1]}"),
            ),
          ],
        ),
        Row(
          wrap=True,
          controls=[
            Column(controls=self.stats[0].controls, horizontal_alignment="center"),
            Column(controls=self.stats[1].controls),
            Column(controls=self.stats[2].controls),
            Column(controls=self.stats[3].controls),
            Column(controls=self.stats[4].controls),
            Column(controls=self.stats[5].controls),
          ],
        ),
        Row(
          alignment=MainAxisAlignment.CENTER,
          controls=[
            self.input,
            self.start_button,
            self.reset_button,
          ]
        ),
      ],
    )
    self.cursor = Cursor(self.text_displayed.controls, self.quote_text)

  # Build the UI layout
  def build(self):
    # Display words for typing in the UI
    self.refresh()
    return self.layout

  def refresh(self):
    for stat in self.stats:
      stat.update(0)
    self.remaining_time_stat.update()
    self.cursor.refresh()

  def change_game_time(self, time):
    # change the time of the game if user click button
    self.total_time = time
    self.remaining_time_stat.update(time)
    self.update()

  def on_keyboard(self, e: KeyboardEvent):
    # Handling keyboard input during typing
    self.cursor.trigger(e.key)
    for control in self.stats:
      control.update()
    self.update()

  def start(self, e):
    """Start both threads"""
    self.stop_flag_timer = threading.Thread(target=self.__start_timer, args=(e,))
    self.stop_flag_timer.start()

  def __start_timer(self, e):
    # Timer thread function
    self.start_button.disabled = True
    self.input.disabled = False
    self.input.focus()
    self.refresh()
    for self.time in range(1, self.total_time + 1):
      self.elapsed_time_stat.update()
      self.remaining_time_stat.update()
      sleep(1)
      self.update()
      if (
        self.time == self.total_time
        or len(self.cursor.text) == self.cursor.curr
      ):
        self.StartRound = False
        self.calculateScores(self.StartRound)
        self.input.disabled = True
        return
    self.reset_button.disabled = False
    self.update()

  def calculateScores(self, StartRound):
    user_entered_paragraph = []
    self.total_words = 0
    if not StartRound:
      user_entered_paragraph = self.input.value.split()
      self.total_words = len(user_entered_paragraph)

    self.total_words_stat.update()
    self.update()

    words_to_type_array = self.quote_text.split()

    for pair in list(zip(words_to_type_array, user_entered_paragraph)):
      if pair[0] != pair[1]:
        self.wrong_words += 1
        self.wrong_words_stat.update()

    self.wpm = ((self.total_words - self.wrong_words) / self.time) * 60
    self.wpm_stat.update()
    self.update()

  def reset(self, e):
    # Reset all values and controls
    self.elapsed_time_stat.update(0)
    self.remaining_time_stat.update()
    self.total_time = 60
    self.total_words = 0
    self.wrong_words = 0
    self.time = 0
    self.start_button.disabled = False
    self.reset_button.disabled = False
    self.input.value = ""
    self.input.disabled = True

    # self.cursor.refresh()
    self.cursor.clear(quote_generator.get_quote()[0])

    self.wpm_stat.update(0)
    self.accuracy_stat.update()
    self.total_words_stat.update()
    self.wrong_words_stat.update()
    self.update()

  # def update(self):
  #   for stat in self.stats:
  #     stat.update()
  #   super().update()

  def __calculate_gross_wpm(self, word_length=5):
    total_characters, total_time_seconds = len(self.quote_text), int((self.time / 60) * 60)

    if total_time_seconds == 0:
      total_time_seconds = 0

    total_words = total_characters / word_length
    gross_wpm = (
      total_words / total_time_seconds
    ) * 60  # Convert total time to minutes
    return gross_wpm

  def __calculate_accuracy(self, total_characters, total_errors):
    accuracy_percentage = (
      (total_characters - total_errors) / total_characters
    ) * 100
    return accuracy_percentage

  def __calculate_net_wpm(self, gross_wpm, error_rate):
    net_wpm = max(0, gross_wpm - error_rate)
    return net_wpm
