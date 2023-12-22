import threading
from time import sleep

from flet import *
from setting import *

class StatPanel:
  def __init__(self, label_text: str, stat_format: str, var_ref):
    # the function to get the value of the variable
    self.func = var_ref
    # the format for displaying the variable
    self.format = stat_format
    # the label and display of the counter
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
    """ Update the displayed value """
    if val:
      self.stat_text.value = self.format.format(val)
    else:
      self.stat_text.value = self.format.format(self.func())


class Cursor:
  def __init__(self, char_slots: list[Control], displayed_text: str):
    """ Add the text content and add the displays of each character """
    self.text = displayed_text.strip()
    self.chars = char_slots
    for char in self.text:
      self.chars.append(Container(**char_style(char)))
    self.current_position = 0


  def refresh(self):
    """ Reset all the characters in the text and the cursor position """
    # reset character looks
    for char in self.chars:
      char.bgcolor = colors.TRANSPARENT
      char.content.color = colors.GREY_700
      char.border = border.only()
    # show cursor at the first char
    self.current_position = 0
    self.chars[0].border = border.only(bottom=border.BorderSide(1))


  def clear(self, new_text: str):
    """ Change the text and reset the cursor """
    self.text = new_text.strip()
    # clear the displayed characters add the new ones
    self.chars.clear()
    for char in self.text:
      self.chars.append(Container(**char_style(char)))
    self.current_position = 0


  def trigger(self, key: str):
    """ Process the triggered key press """
    if self.current_position == len(self.chars):
      return False

    if "Backspace" == key:
      # go back one character and change the cursor position and looks
      self.chars[self.current_position].border = border.only(bottom=border.BorderSide(1))
      self.chars[self.current_position - 1].border = border.only(bottom=border.BorderSide(5, "white"))
      self.chars[self.current_position - 1].bgcolor = colors.TRANSPARENT
      self.chars[self.current_position - 1].content.color = colors.GREY_700
      if self.current_position > 0:
        self.current_position -= 1
    elif key.lower() == self.text[self.current_position]:
      # change the color of the right character to green
      self.chars[self.current_position].bgcolor = colors.GREEN_700

      self.chars[self.current_position].border = border.only(bottom=border.BorderSide(1))
      self.chars[self.current_position].color = colors.GREY_700
      self.chars[self.current_position].content.color = colors.WHITE
      # bounds check
      if self.current_position < len(self.chars) - 1:
        self.chars[self.current_position + 1].border = border.only(bottom=border.BorderSide(5, "white"))
      self.current_position += 1
    elif key.lower() != self.text[self.current_position]:
      # change the color of the right character to green
      self.chars[self.current_position].bgcolor = colors.RED_700

      self.chars[self.current_position].border = border.only(bottom=border.BorderSide(1))
      self.chars[self.current_position].content.color = colors.WHITE
      if self.current_position < len(self.chars) - 1:
        self.chars[self.current_position + 1].border = border.only(bottom=border.BorderSide(5, "white"))
      self.current_position += 1
    else:
      # handle any exceptional input
      self.chars[self.current_position].bgcolor = colors.GREY_700
      self.chars[self.current_position].content.color = colors.WHITE
    return True


class TypingApp(UserControl):
  def __init__(self):
    super().__init__()
    self.StartRound = True
    self.quote_text = words_to_type
    self.text_displayed = Row(wrap=True)

    self.cursor = Cursor(self.text_displayed.controls, self.quote_text)

    # UI controls
    self.input = TextField(**user_inputs)
    self.start_button = ElevatedButton(**user_buttons['start'])
    self.start_button.on_click = self.start
    self.reset_button = ElevatedButton(**user_buttons['reset'])
    self.reset_button.on_click = self.reset
    self.clear_button = ElevatedButton(**user_buttons['clear'])
    self.clear_button.on_click = self.clear

    self.total_time = 60
    self.reset_counters()

    # The stat counters display setup
    self.elapsed_time_stat = StatPanel("Elapsed Time", "{}", lambda: self.time)
    self.remaining_time_stat = StatPanel("Remaining Time", "{}", lambda: self.total_time - self.time)
    self.total_words_stat = StatPanel("Total Words", "{}", lambda: self.total_words)
    self.wrong_words_stat = StatPanel("Wrong Words", "{}", lambda: self.wrong_words)
    self.wpm_stat = StatPanel("WPM", "{:.2f}", lambda: self.__calculate_wpm())
    self.accuracy_stat = StatPanel("Accuracy", "{:.2f}%", lambda: self.__calculate_accuracy())

    self.author_name = Text(value=f"author: {generated_quote[1]}")

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
    # the column of the whole test layout
    self.layout = Column(
      alignment="center",
      horizontal_alignment="center",
      controls=[
        # container for the back and time selection buttons
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
                    on_click=lambda _: (self.refresh(), self.elapsed_time_stat.update(0), self.change_game_time(15))[2],
                  ),
                  TextButton(
                    text="30",
                    on_click=lambda _: (self.refresh(), self.elapsed_time_stat.update(0), self.change_game_time(30))[2],
                  ),
                  TextButton(
                    text="60",
                    on_click=lambda _: (self.refresh(), self.elapsed_time_stat.update(0), self.change_game_time(60))[2],
                  ),
                ]
              )
            ]
          ),
        ),
        # the container of the test characters and displayed text
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
        # a place to position the quote auther name
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
              content=self.author_name),
          ],
        ),
        # all the counters for the different statistics
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
        # inputs and user controls
        Row(
          alignment=MainAxisAlignment.CENTER,
          controls=[
            self.input,
            self.start_button,
            self.clear_button,
            self.reset_button,
          ]
        ),
      ],
    )

  # Build the UI layout
  def build(self):
    # Display words for typing in the UI
    self.refresh()
    return self.layout

  def refresh(self):
    # reset all the counters to a starting state
    self.reset_counters()
    self.remaining_time_stat.update()
    self.cursor.refresh()

  def change_game_time(self, time):
    # change the time of the game if user click button
    self.total_time = time
    self.remaining_time_stat.update(time)
    self.update()

  def on_keyboard(self, e: KeyboardEvent):
    # Handling keyboard input during typing
    if self.start_button.disabled and not self.input.focus():
      self.cursor.trigger(e.key)
      for control in self.stats:
        control.update()
      self.update()

  def start(self, e):
    """Start both threads"""
    self.StartRound = True
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
      if (not self.StartRound or
          self.time == self.total_time or
          self.cursor.current_position == len(self.cursor.text)):
        self.__calculateScores()
        self.input.disabled = True
        return
    self.reset_button.disabled = False
    self.update()

  def reset_counters(self):
    self.wrong_words = 0
    self.total_words = 0
    self.time = 0
    self.wpm = 0

  def clear(self, e):
    self.reset_counters()
    for stat in self.stats:
      stat.update()
    self.input.value = ""
    self.start_button.disabled = False
    self.cursor.refresh()
    self.StartRound = False
    self.update()

  def reset(self, e):
    # Reset all values and controls
    self.reset_counters()
    self.elapsed_time_stat.update(0)
    self.remaining_time_stat.update()
    self.start_button.disabled = False
    self.reset_button.disabled = False
    self.input.value = ""
    self.input.disabled = True

    self.cursor.refresh()
    new_quote = quote_generator.get_quote()
    self.quote_text = new_quote[0]
    self.cursor.clear(new_quote[0])
    self.author_name.value = f"author: {new_quote[1]}"
    self.reset_counters()
    self.accuracy_stat.update()
    self.update()

  def __calculateScores(self):
    user_entered_paragraph = []
    self.total_words = 0
    self.wrong_words = 0
    user_entered_paragraph = self.input.value.split()
    self.total_words = len(user_entered_paragraph)
    # print(f"User input: {user_entered_paragraph}")

    self.total_words_stat.update()
    self.update()

    words_to_type_array = self.quote_text.split()
    print(f"Actual text: {user_entered_paragraph}")

    for pair in list(zip(words_to_type_array, user_entered_paragraph)):
      if pair[0].lower() != pair[1].lower():
        self.wrong_words += 1

    self.wrong_words_stat.update()

    for stat in self.stats:
      stat.update()
    self.update()

  def __calculate_wpm(self):
    if self.time == 0:
      self.wpm = 0
    else:
      self.wpm = (self.total_words - self.wrong_words) / self.time * 60
    return self.wpm

  def __calculate_accuracy(self):
    no_chars, no_errors = self.cursor.current_position, 0
    for i in range(no_chars - 1):
      if self.quote_text[i] == self.input.value[i]:
        no_errors += 1
    # print(f'errors: {no_errors}, chars: {no_chars}')
    accuracy_percentage = no_errors / (no_chars - 1) * 100 if no_chars > 1 else 0
    return accuracy_percentage
