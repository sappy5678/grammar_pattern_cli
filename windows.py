# 暫時沒有用到
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit import Application
from prompt_toolkit.document import Document
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.layout.containers import VSplit, Window, HSplit
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.application import get_app

kb = KeyBindings()

@kb.add('c-q')
def exit_(event):
    """
    Pressing Ctrl-Q will exit the user interface.

    Setting a return value means: quit the event loop that drives the user
    interface and return this value from the `Application.run()` call.
    """
    event.app.exit()

@kb.add('s-down')
def exit_(event):
    """
    Pressing Ctrl-Q will exit the user interface.

    Setting a return value means: quit the event loop that drives the user
    interface and return this value from the `Application.run()` call.
    """
    get_app().layout.focus(control_window)

@kb.add('s-up')
def exit_(event):
    """
    Pressing Ctrl-Q will exit the user interface.

    Setting a return value means: quit the event loop that drives the user
    interface and return this value from the `Application.run()` call.
    """
    get_app().layout.focus(show_window)

control_buffer = Buffer()  # Editable buffer.

show_buffer = Buffer(read_only=True)

show_window = Window(content=BufferControl(buffer=show_buffer, focus_on_click=True),)
control_window = Window(content=BufferControl(buffer=control_buffer, focus_on_click=True), height=5)

root_container = HSplit([
    
    # Display the text 'Hello world' on the right.
    show_window,

    # A vertical line in the middle. We explicitly specify the width, to
    # make sure that the layout engine will not try to divide the whole
    # width by three for all these windows. The window will simply fill its
    # content by repeating this character.
    Window(char='─',height=1),


    # One window that holds the BufferControl with the default buffer on
    # the left.
    control_window,
])


t = ''
for i in range(99):
    t += '<style bg="blue" fg="white">' + str(i) + '</style>' + '\n'

show_buffer.reset(Document(HTML(t, )))
layout = Layout(root_container)
app = Application(layout=layout, full_screen=True, key_bindings=kb)
app.run()

