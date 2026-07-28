from kivy.config import Config
# 1. This shrinks your PC window to look like a phone screen
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '600')

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.metrics import dp, sp
from kivy.properties import StringProperty, BooleanProperty, ListProperty, NumericProperty
from datetime import datetime
import threading, requests, socket
import re
from kivy.core.window import Window
Window.softinput_mode = 'resize' 

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
    orientation: "vertical"
    padding: dp(14)
    spacing: dp(10)

    canvas.before:
        Color:
            rgba: 0.067, 0.075, 0.098, 1
        Rectangle:
            pos: self.pos
            size: self.size

    # Title with Online/Offline status
    BoxLayout:
        size_hint_y: None
        height: dp(42)

        Label:
            id: title
            text: "PyChat"
            font_size: sp(23)
            bold: True
            color: 0.35, 0.75, 1, 1
            halign: "left"
            valign: "middle"
            text_size: self.size

        Label:
            id: status
            text: "Offline"
            font_size: sp(18)
            bold: True
            color: 0.9, 0.3, 0.3, 1
            halign: "right"
            valign: "middle"
            text_size: self.size
            size_hint_x: 0.3

    # Username + Connect
    BoxLayout:
        size_hint_y: None
        height: dp(54)
        spacing: dp(10)

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
            height: dp(48)

        RoundedButton:
            id: connect
            text: "Connect"
            accent_color: 0.20, 0.58, 0.98, 1
            size_hint_x: None
            width: dp(108)
            on_release: root.connect()

    # Chat area
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

    # Bottom bar
    BoxLayout:
        size_hint_y: None
        height: dp(48)
        spacing: dp(10)

        RoundedButton:
            text: "+"
            accent_color: 0.42, 0.34, 0.78, 1
            size_hint_x: None
            width: dp(46)
            height: dp(16)
            font_size: sp(15)
            on_release: root.add_system_message("Attachments coming soon")

        MDTextField:
            id: message
            hint_text: "Message"
            mode: "rectangle"
            multiline: False
            fill_color_normal: "#333333"
            text_color_normal: 1, 1, 1, 1
            hint_text_color_normal: 0.6, 0.6, 0.6, 1
            line_color_normal: 0.35, 0.35, 0.35, 1
            font_size: "15sp"
            size_hint_y: None
            height: dp(48)
            on_text_validate: root.send()

        RoundedButton:
            text: "Send"
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


class ChatClient:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        self.username = ""
        self.callback = None

    def load_server(self):
        url = "https://raw.githubusercontent.com/SarthakTools/pychat/main/config.json"
        config = requests.get(url, timeout=5).json()
        return config["host"], int(config["port"])
        # return "127.0.0.1", 8080

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
                message = self.client.recv(1024).decode()
                if message:
                    self.callback(message)
            except Exception:
                self.connected = False
                self.callback("Disconnected from server.")
                break

    def send(self, message):
        if self.connected:
            self.client.send(f"{self.username}: {message}".encode())

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

    def get_name_color(self, username):
        if username not in self.name_color_map:
            self.name_color_map[username] = NAME_COLORS[self.color_index % len(NAME_COLORS)]
            self.color_index += 1
        return self.name_color_map[username]

    def connect(self):
        username = self.ids.username.text.strip()
        if not username:
            self.add_system_message("Enter a username first.")
            return
        self.ids.connect.disabled = True
        self.add_system_message("Connecting...")
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
        self.add_system_message("Connected successfully!")

                
        if not self._date_added:
            self.add_date_separator()
            self._date_added = True

    def on_failed(self, error):
        self.ids.connect.disabled = False
        self.ids.title.text = "PyChat — Offline"
        self.add_system_message(f"Failed: {error}")

    def receive_message(self, message):
        Clock.schedule_once(lambda dt: self.handle_incoming(message))

    def handle_incoming(self, raw):
        raw = raw.strip()
        if not raw:
            return

        # System messages
        if any(x in raw for x in ("Disconnected", "joined the chat", "left the chat")):
            self.add_system_message(raw)
            if "Disconnected" in raw:
                self.ids.title.text = "PyChat — Offline"
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
            self.add_bubble(user, msg, is_self=False)
        else:
            self.add_system_message(raw)

    def add_bubble(self, username, message, is_self=False):
        if not self._date_added:
            self.add_date_separator()
            self._date_added = True

        try:
            now = datetime.now().strftime("%-I:%M %p").lower()
        except ValueError:
            now = datetime.now().strftime("%I:%M %p").lstrip("0").lower()

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

    def add_system_message(self, text):
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
            return
        if not self.client.connected:
            self.add_system_message("Not connected. Connect first.")
            return

        # Show own message immediately
        self.add_bubble(self.client.username, message, is_self=True)
        self.client.send(message)
        self.ids.message.text = ""


class PyChat(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        self.title = "PyChat"
        return Root()


if __name__ == "__main__":
    PyChat().run()
