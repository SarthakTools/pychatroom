from kivy.config import Config
# 1. This shrinks your PC window to look like a phone screen
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '600')

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.metrics import dp, sp
from kivy.properties import StringProperty, BooleanProperty, ListProperty, NumericProperty
from datetime import datetime
import threading, requests, socket
import re
from kivy.core.window import Window
Window.softinput_mode = 'below_target'

KV = """
#:kivy 2.2.1
#:import dp kivy.metrics.dp
#:import sp kivy.metrics.sp

<RoundedButton@Button>:
    accent_color: 0.20, 0.58, 0.98, 1
    background_normal: ""
    background_down: ""
    background_color: 0, 0, 0, 0
    color: 1, 1, 1, 1
    font_size: sp(15)
    bold: True

    canvas.before:
        Color:
            rgba: self.accent_color if self.state == "normal" else [c * 0.8 for c in self.accent_color[:3]] + [1]
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(16)]

<Root>:
    screen_manager: screen_manager

    ScreenManager:
        id: screen_manager

        Screen:
            name: "login"
            BoxLayout:
                orientation: "vertical"
                padding: dp(24)
                spacing: dp(18)

                canvas.before:
                    Color:
                        rgba: 0.067, 0.075, 0.098, 1
                    Rectangle:
                        pos: self.pos
                        size: self.size

                Widget:

                Label:
                    text: "MayBee"
                    font_size: sp(36)
                    bold: True
                    color: 0.35, 0.75, 1, 1
                    size_hint_y: None
                    height: dp(52)
                    halign: "center"
                    valign: "middle"
                    text_size: self.size

                Label:
                    text: "Connect with BEE-Server to Buzz !!!"
                    font_size: sp(16)
                    color: 0.75, 0.78, 0.86, 1
                    halign: "center"
                    valign: "middle"
                    text_size: self.width, None
                    size_hint_y: None
                    height: self.texture_size[1] + dp(24)

                MDTextField:
                    id: username
                    hint_text: "Username"
                    mode: "rectangle"
                    fill_color_normal: "#333333"
                    text_color_normal: 1, 1, 1, 1
                    hint_text_color_normal: 0.6, 0.6, 0.6, 1
                    line_color_normal: 0.35, 0.35, 0.35, 1
                    font_size: "15sp"
                    size_hint_y: None
                    height: dp(50)

                RoundedButton:
                    id: connect
                    text: "Connect to Hive"
                    accent_color: 0.20, 0.58, 0.98, 1
                    size_hint_y: None
                    height: dp(48)
                    on_release: root.connect()

                Label:
                    id: login_message
                    text: ""
                    font_size: sp(14)
                    color: 0.95, 0.45, 0.45, 1
                    halign: "center"
                    valign: "middle"
                    text_size: self.width, None
                    size_hint_y: None
                    height: self.texture_size[1] + dp(12)

                Widget:

        Screen:
            name: "chat"
            BoxLayout:
                orientation: "vertical"
                padding: dp(12), dp(10), dp(12), dp(10)
                spacing: dp(10)

                canvas.before:
                    Color:
                        rgba: 0.047, 0.055, 0.078, 1
                    Rectangle:
                        pos: self.pos
                        size: self.size

                Widget:
                    size_hint_y: None
                    height: dp(8)

                BoxLayout:
                    orientation: "vertical"
                    size_hint_y: None
                    height: dp(60)
                    padding: dp(5), dp(10), dp(10), dp(8)
                    spacing: dp(0)
                    canvas.before:
                        Color:
                            rgba: 0.11, 0.14, 0.22, 1
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                            radius: [dp(22), dp(22), dp(22), dp(22)]

                    BoxLayout:
                        size_hint_y: None
                        height: dp(42)

                        Label:
                            id: title
                            text: "MayBee"
                            font_size: sp(19)
                            bold: True
                            color: 0.35, 0.75, 1, 1
                            halign: "left"
                            valign: "middle"
                            text_size: self.size
                            padding:[dp(10), dp(0), dp(0), dp(0)]

                        Label:
                            id: status
                            text: "Offline"
                            font_size: sp(18)
                            padding:[dp(0), dp(0), dp(10), dp(0)]
                            bold: True
                            color: 0.9, 0.3, 0.3, 1
                            halign: "right"
                            valign: "middle"
                            text_size: self.size
                            size_hint_x: 0.3

                ScrollView:
                    id: scroll
                    do_scroll_x: False
                    bar_width: dp(3)
                    bar_color: 0.35, 0.4, 0.5, 0.6

                    BoxLayout:
                        id: chat_box
                        orientation: "vertical"
                        size_hint_y: None
                        height: self.minimum_height
                        padding: [dp(4), dp(12)]
                        spacing: dp(14)

                BoxLayout:
                    size_hint_y: None
                    height: dp(48)
                    spacing: dp(10)

                    # RoundedButton:
                    #     text: "+"
                    #     accent_color: 0.42, 0.34, 0.78, 1
                    #     size_hint_x: None
                    #     width: dp(46)
                    #     height: dp(16)
                    #     font_size: sp(15)
                    #     on_release: root.add_system_message("Attachments coming soon")

                # typing status label (appears above the input box)
                Label:
                    id: typing_status
                    text: ""
                    size_hint_y: None
                    height: dp(20)
                    font_size: sp(13)
                    color: 0.75, 0.78, 0.86, 1
                    halign: "left"
                    valign: "middle"
                    text_size: self.width, None
                    padding: [dp(6), dp(0)]

                BoxLayout:
                    size_hint_y: None
                    height: dp(48)
                    spacing: dp(10)

                    # RoundedButton:
                    #     text: "+"
                    #     accent_color: 0.42, 0.34, 0.78, 1
                    #     size_hint_x: None
                    #     width: dp(46)
                    #     height: dp(16)
                    #     font_size: sp(15)
                    #     on_release: root.add_system_message("Attachments coming soon")

                    MDTextField:
                        id: message
                        hint_text: "Message"
                        mode: "rectangle"
                        multiline: False
                        fill_color_normal: "#1a1f2c"
                        text_color_normal: 1, 1, 1, 1
                        hint_text_color_normal: 0.65, 0.65, 0.7, 1
                        line_color_normal: 0.35, 0.35, 0.35, 1
                        font_size: "15sp"
                        size_hint_y: None
                        height: dp(48)
                        on_text_validate: root.send()
                        on_text: root.on_typing()

                    RoundedButton:
                        text: "Buzz"
                        accent_color: 0.20, 0.58, 0.98, 1
                        size_hint_x: None
                        width: dp(64)
                        on_release: root.send()

# ---------- Message Bubble ----------
<MessageBubble>:
    size_hint_y: None
    height: self.minimum_height
    size_hint_x: None
    width: root.bubble_width
    orientation: "vertical"
    padding: [dp(14), dp(9), dp(14), dp(7)]
    spacing: dp(3)

    canvas.before:
        Color:
            rgba: root.bubble_color
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: root.corner_radius

    Label:
        text: root.username
        font_size: sp(12)
        bold: True
        color: root.name_color
        size_hint_y: None
        height: dp(16)
        text_size: self.width, None
        halign: "left" if not root.is_self else "right"
        valign: "middle"

    Label:
        text: root.message
        font_size: sp(15)
        color: 1, 1, 1, 1
        size_hint_y: None
        height: self.texture_size[1]
        text_size: root.bubble_width - dp(28), None
        halign: "left"
        valign: "top"

    Label:
        text: root.timestamp
        font_size: sp(11)
        color: 0.78, 0.78, 0.85, 1
        size_hint_y: None
        height: dp(14)
        text_size: self.width, None
        halign: "right"
        valign: "middle"

# ---------- System message ----------
<SystemMessage>:
    size_hint_y: None
    height: dp(26)
    text: root.message
    font_size: sp(13)
    color: 0.58, 0.58, 0.65, 1
    halign: "center"
    valign: "middle"
    text_size: self.size

# ---------- Typing indicator ----------
<TypingIndicator>:
    size_hint_y: None
    size_hint_x: None
    height: dp(34)
    width: dp(62)
    orientation: "horizontal"
    padding: [dp(14), dp(9), dp(14), dp(9)]
    spacing: dp(4)

    canvas.before:
        Color:
            rgba: 0.22, 0.22, 0.26, 1
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(14), dp(14), dp(14), dp(4)]

    Label:
        text: "•"
        font_size: sp(22)
        color: 0.78, 0.78, 0.85, root.alpha1
        size_hint_x: None
        width: dp(8)

    Label:
        text: "•"
        font_size: sp(22)
        color: 0.78, 0.78, 0.85, root.alpha2
        size_hint_x: None
        width: dp(8)

    Label:
        text: "•"
        font_size: sp(22)
        color: 0.78, 0.78, 0.85, root.alpha3
        size_hint_x: None
        width: dp(8)

# ---------- Date separator ----------
<DateSeparator>:
    size_hint_y: None
    height: dp(30)
    orientation: "horizontal"
    padding: [dp(30), 0]
    spacing: dp(10)

    Widget:
        canvas:
            Color:
                rgba: 0.24, 0.24, 0.29, 1
            Rectangle:
                pos: self.x, self.center_y
                size: self.width, dp(1)

    Label:
        text: "Today"
        font_size: sp(12)
        color: 0.68, 0.68, 0.75, 1
        size_hint_x: None
        width: self.texture_size[0] + dp(18)
        canvas.before:
            Color:
                rgba: 0.17, 0.18, 0.22, 1
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [dp(12)]

    Widget:
        canvas:
            Color:
                rgba: 0.24, 0.24, 0.29, 1
            Rectangle:
                pos: self.x, self.center_y
                size: self.width, dp(1)
"""

Builder.load_string(KV)

NAME_COLORS = [
    (0.55, 0.45, 0.95, 1),
    (0.30, 0.70, 0.95, 1),
    (0.30, 0.85, 0.55, 1),
    (0.95, 0.55, 0.30, 1),
    (0.95, 0.40, 0.60, 1),
    (0.90, 0.80, 0.30, 1),
]


class MessageBubble(BoxLayout):
    username = StringProperty("")
    message = StringProperty("")
    timestamp = StringProperty("")
    is_self = BooleanProperty(False)
    bubble_color = ListProperty([0.22, 0.22, 0.26, 1])
    name_color = ListProperty([0.7, 0.7, 0.75, 1])
    bubble_width = NumericProperty(dp(220))
    corner_radius = ListProperty([dp(14), dp(14), dp(14), dp(4)])


class SystemMessage(Label):
    message = StringProperty("")


class DateSeparator(BoxLayout):
    pass


class TypingIndicator(BoxLayout):
    alpha1 = NumericProperty(0.3)
    alpha2 = NumericProperty(0.3)
    alpha3 = NumericProperty(0.3)

    def start(self):
        # Stagger three identical bounce loops so the dots pulse left-to-right
        self._anims = []
        for prop, delay in (("alpha1", 0), ("alpha2", 0.15), ("alpha3", 0.3)):
            Clock.schedule_once(lambda dt, p=prop: self._loop(p), delay)

    def _loop(self, prop):
        anim = Animation(**{prop: 1}, duration=0.3) + Animation(**{prop: 0.3}, duration=0.3)
        anim.repeat = True
        anim.start(self)
        self._anims.append(anim)

    def stop(self):
        for anim in getattr(self, "_anims", []):
            anim.cancel(self)
        self._anims = []


class ChatClient:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        self.username = ""
        self.callback = None
        self._recv_buffer = ""

    def load_server(self):
        # url = "https://raw.githubusercontent.com/SarthakTools/pychat/main/config.json"
        # config = requests.get(url, timeout=5).json()
        # return config["host"], int(config["port"])
        return "127.0.0.1",8080

    def connect(self, username, callback):
        self.username = username
        self.callback = callback
        host, port = self.load_server()
        self.client.connect((host, port))
        if self.client.recv(1024).decode() == "USERNAME":
            self.client.send(username.encode())
        self.connected = True
        threading.Thread(target=self.receive_loop, daemon=True).start()

    def receive_loop(self):
        while self.connected:
            try:
                chunk = self.client.recv(1024).decode()
                if not chunk:
                    raise ConnectionError("Server closed the connection.")

                # TCP has no message boundaries: a single recv() can contain
                # zero, one, or several messages, and a message can be split
                # across multiple recv() calls. Buffer everything and only
                # emit complete newline-delimited messages.
                self._recv_buffer += chunk

                # Defensive fix: the server doesn't reliably terminate every
                # message with "\n" (the "X joined/left the chat." notice is
                # the known offender). When a message is missing its
                # trailing "\n", whatever arrives next gets glued onto the
                # end of it and both sit stuck in the buffer together until
                # something else finally supplies a "\n" -- which is why the
                # join notice doesn't appear until you start typing (the
                # typing marker is the first thing to arrive with a
                # newline), and why a chat message glued onto a stale notice
                # can fail the "is this my own echo" check and show up as a
                # duplicate bubble with the username visible.
                #
                # Insert virtual boundaries both BEFORE and AFTER every known
                # message signature, so each one is always isolated and
                # flushed on its own regardless of what the server did or
                # didn't append.
                self._recv_buffer = re.sub(
                    r"(?<!\n)(__CTRL__\|)", r"\n\1", self._recv_buffer
                )
                self._recv_buffer = re.sub(
                    r"(TYPING_ON|TYPING_OFF)(?!\n)", r"\1\n", self._recv_buffer
                )
                self._recv_buffer = re.sub(
                    r"((?:joined|left) the chat\.)(?!\n)", r"\1\n", self._recv_buffer
                )

                while "\n" in self._recv_buffer:
                    line, self._recv_buffer = self._recv_buffer.split("\n", 1)
                    if line:
                        self.callback(line)
            except Exception:
                self.connected = False
                self.callback("Disconnected from server.")
                break

    def send(self, message):
        if self.connected:
            self.client.send(f"{self.username}: {message}\n".encode())

    def send_typing(self, is_typing):
        # Uses a "__CTRL__|" prefix so it never matches the "user: text" chat
        # pattern. Every message ends with "\n" so the receiver can split the
        # raw TCP byte stream back into individual messages reliably.
        if self.connected:
            marker = "TYPING_ON" if is_typing else "TYPING_OFF"
            try:
                self.client.send(f"__CTRL__|{self.username}|{marker}\n".encode())
            except Exception:
                pass

    def disconnect(self):
        self.connected = False
        try:
            self.client.close()
        except Exception:
            pass


class Root(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client = ChatClient()
        self.name_color_map = {}
        self.color_index = 0
        self._date_added = False

        # System typing animation widget + anim handle
        self._typing_sys_widget = None
        self._typing_sys_anim = None

        # Typing indicator state
        self._is_typing = False           # am I currently signalling "typing"?
        self._typing_stop_event = None    # debounce timer for my own typing
        self._typing_hide_event = None    # safety auto-hide for the incoming indicator
        self._typing_last_activity = 0.0  # time of last TYPING_ON (monotonic)
        self._typing_user = None
        self._typing_row = None
        self._typing_indicator = None

    def get_name_color(self, username):
        if username not in self.name_color_map:
            self.name_color_map[username] = NAME_COLORS[self.color_index % len(NAME_COLORS)]
            self.color_index += 1
        return self.name_color_map[username]

    def connect(self):
        username = self.ids.username.text.strip()
        if not username:
            self.ids.login_message.text = "Enter your name first."
            return
        self.ids.connect.disabled = True
        self.ids.login_message.text = "Connecting..."
        threading.Thread(target=self.connect_thread, args=(username,), daemon=True).start()

    def connect_thread(self, username):
        try:
            self.client.connect(username, self.receive_message)
            Clock.schedule_once(lambda dt: self.on_connected())
        except Exception as e:
            error = str(e)
            Clock.schedule_once(lambda dt, err=error: self.on_failed(err))

    def on_connected(self):
        self.ids.status.text = "Online"
        self.ids.status.color = (0.2, 0.85, 0.4, 1)
        self.ids.login_message.text = ""
        self.ids.screen_manager.current = "chat"
        self.add_system_message("Connected successfully!")

        if not self._date_added:
            self.add_date_separator()
            self._date_added = True

    def on_failed(self, error):
        self.ids.connect.disabled = False
        self.ids.login_message.text = f"Failed: {error}"

    def receive_message(self, message):
        Clock.schedule_once(lambda dt: self.handle_incoming(message))

    def handle_incoming(self, raw):
        raw = raw.strip()
        if not raw:
            return

        # Typing control messages: "__CTRL__|username|TYPING_ON/OFF"
        if raw.startswith("__CTRL__|"):
            parts = raw.split("|", 2)
            if len(parts) == 3:
                _, user, marker = parts
                if user != self.client.username:
                    if marker == "TYPING_ON":
                        self._typing_user = user
                        self._typing_last_activity = Clock.get_time()
                        self.show_typing(user)
                        # Safety: only hide if no fresh TYPING_ON for a while.
                        # Continuous keystrokes keep resetting _typing_last_activity,
                        # so the indicator stays up while the other person is typing.
                        if self._typing_hide_event:
                            self._typing_hide_event.cancel()
                        self._typing_hide_event = Clock.schedule_once(
                            self._check_typing_timeout, 5.5
                        )
                    elif marker == "TYPING_OFF":
                        self.hide_typing()
            return

        # System messages
        if any(x in raw for x in ("Disconnected", "joined the chat", "left the chat")):
            self.add_system_message(raw)
            if "Disconnected" in raw:
                self.ids.title.text = "MayBee — Offline"
                self.ids.connect.disabled = False
            return

        # Normal chat message: "username: text"
        match = re.match(r"^([^:]+):\s*(.*)$", raw, re.DOTALL)
        if match:
            user = match.group(1).strip()
            msg = match.group(2).strip()
            is_self = (user == self.client.username)
            # Skip server echo of our own messages (we already showed them)
            if is_self:
                return
            # Real message arrived → typing indicator is immediately stale.
            # Always clear it (and cancel any pending safety timer).
            if self._typing_hide_event:
                self._typing_hide_event.cancel()
                self._typing_hide_event = None
            self.hide_typing()
            self.add_bubble(user, msg, is_self=False)
        else:
            self.add_system_message(raw)

    def add_bubble(self, username, message, is_self=False):
        if not self._date_added:
            self.add_date_separator()
            self._date_added = True

        dt_now = datetime.now()
        hour_12 = dt_now.hour % 12
        hour_12 = 12 if hour_12 == 0 else hour_12
        now = dt_now.strftime(f"{hour_12}:%M %p").lower()

        # Create the bubble
        bubble = MessageBubble()
        bubble.username = username
        bubble.message = message
        bubble.timestamp = now + ("" if is_self else "")
        bubble.is_self = is_self

        # Calculate a reasonable width based on text length
        approx_width = min(dp(280), max(dp(120), len(message) * dp(8) + dp(40)))
        bubble.bubble_width = approx_width

        if is_self:
            bubble.bubble_color = [0.298, 0.239, 0.694, 1]
            bubble.name_color = [1.000, 0.820, 0.400, 1]
            bubble.corner_radius = [dp(14), dp(14), dp(4), dp(14)]
        else:
            bubble.bubble_color = [0.22, 0.22, 0.26, 1]
            bubble.name_color = self.get_name_color(username)
            bubble.corner_radius = [dp(14), dp(14), dp(14), dp(4)]

        # Row that pushes the bubble left or right
        row = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=bubble.height,   # will be updated after
            spacing=dp(0)
        )

        if is_self:
            row.add_widget(Widget())          # left spacer
            row.add_widget(bubble)
        else:
            row.add_widget(bubble)
            row.add_widget(Widget())          # right spacer

        self.ids.chat_box.add_widget(row)

        # Force height update after labels measure
        def update_height(dt):
            row.height = bubble.minimum_height
            bubble.height = bubble.minimum_height
            self._scroll_to_bottom()
        Clock.schedule_once(update_height, 0.02)

    def show_typing(self, username):
        if self._typing_sys_widget is not None:
            try:
                pass
            except Exception:
                pass
            return

        if not self._date_added:
            self.add_date_separator()
            self._date_added = True

        self._typing_user = username
        sys = SystemMessage()
        self.ids.chat_box.add_widget(sys)
        self._typing_sys_widget = sys
        self._typing_sys_anim = None
        try:
            self.ids.typing_status.text = f"{username} is typing..."
        except Exception:
            pass

        self._scroll_to_bottom()

    def hide_typing(self):
        if self._typing_hide_event:
            self._typing_hide_event.cancel()
            self._typing_hide_event = None

        if self._typing_sys_widget is not None:
            try:
                self.ids.chat_box.remove_widget(self._typing_sys_widget)
            except Exception:
                pass
            self._typing_sys_widget = None

        try:
            self.ids.typing_status.text = ""
        except Exception:
            pass

        self._typing_user = None
        self._typing_last_activity = 0.0

    def _check_typing_timeout(self, dt):
        """Only hide if no TYPING_ON arrived recently (safety net)."""
        self._typing_hide_event = None
        # 5s of silence after the last activity → consider them stopped
        if Clock.get_time() - self._typing_last_activity >= 5.0:
            self.hide_typing()
        else:
            # Still fresh activity — reschedule another check
            remaining = 5.5 - (Clock.get_time() - self._typing_last_activity)
            if remaining < 0.5:
                remaining = 0.5
            self._typing_hide_event = Clock.schedule_once(
                self._check_typing_timeout, remaining
            )

    def on_typing(self):
        # Fired on every keystroke in the message field.
        if not self.client.connected:
            return

        # Resend TYPING_ON on every keystroke, not just when starting typing.
        # The receiver keeps the indicator alive via last-activity timestamp.
        self._is_typing = True
        self.client.send_typing(True)

        # Reset the "stopped typing" debounce timer on every keystroke.
        if self._typing_stop_event:
            self._typing_stop_event.cancel()
        self._typing_stop_event = Clock.schedule_once(self._stop_typing, 0.6)

    def _stop_typing(self, dt):
        self._is_typing = False
        self.client.send_typing(False)

    def add_system_message(self, text):
        if self.ids.screen_manager.current == "login":
            self.ids.login_message.text = text
            return
        sys = SystemMessage()
        sys.message = text
        self.ids.chat_box.add_widget(sys)
        self._scroll_to_bottom()

    def add_date_separator(self):
        self.ids.chat_box.add_widget(DateSeparator())

    def _scroll_to_bottom(self):
        Clock.schedule_once(lambda dt: setattr(self.ids.scroll, "scroll_y", 0), 0.05)

    def send(self):
        message = self.ids.message.text.strip()
        if not message:
            self.ids.message.focus = True
            return
        if not self.client.connected:
            self.add_system_message("Not connected. Connect first.")
            self.ids.message.focus = True
            return

        # Stop signalling "typing" immediately since the message is sent
        if self._typing_stop_event:
            self._typing_stop_event.cancel()
            self._typing_stop_event = None
        if self._is_typing:
            self._is_typing = False
            self.client.send_typing(False)

        # Show own message immediately
        self.add_bubble(self.client.username, message, is_self=True)
        self.client.send(message)
        self.ids.message.text = ""
        self.ids.message.focus = True


class MayBee(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        self.title = "MayBee"
        return Root()


if __name__ == "__main__":
    MayBee().run()
