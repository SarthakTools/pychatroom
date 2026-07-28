from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp, sp
import threading, requests, socket

KV="""
#:kivy 2.2.1
#:import dp kivy.metrics.dp
#:import sp kivy.metrics.sp

<Root>:

    orientation: "vertical"
    padding: dp(12)
    spacing: dp(10)

    canvas.before:
        Color:
            rgba: .10,.10,.12,1
        Rectangle:
            pos: self.pos
            size: self.size

    Label:
        text: "PyChat"
        font_size: sp(28)
        bold: True
        size_hint_y: None
        height: dp(40)
        color: 0.2,0.7,1,1

    Label:
        id: status
        text: "🔴 Offline"
        font_size: sp(16)
        size_hint_y: None
        height: dp(30)
        color: .8,.8,.8,1

    TextInput:
        id: username
        hint_text: "Username"
        multiline: False
        font_size: sp(16)
        size_hint_y: None
        height: dp(48)
        background_color: .16,.16,.18,1
        foreground_color: 1,1,1,1
        cursor_color: 1,1,1,1
        padding: dp(10)

    Button:
        id: connect
        text: "Connect"
        font_size: sp(16)
        size_hint_y: None
        height: dp(48)
        background_normal: ""
        background_color: .15,.55,.95,1
        color: 1,1,1,1
        on_release: root.connect()

    TextInput:
        id: chat
        readonly: True
        multiline: True
        background_color: .13,.13,.15,1
        foreground_color: 1,1,1,1
        cursor_color: 1,1,1,1
        font_size: sp(16)
        padding: dp(10)

    BoxLayout:
        size_hint_y: None
        height: dp(52)
        spacing: dp(8)

        TextInput:
            id: message
            hint_text: "Type a message..."
            multiline: False
            font_size: sp(16)
            background_color: .16,.16,.18,1
            foreground_color: 1,1,1,1
            cursor_color: 1,1,1,1
            padding: dp(10)
            on_text_validate: root.send()

        Button:
            text: "Send"
            font_size: sp(16)
            size_hint_x: None
            width: dp(90)
            background_normal: ""
            background_color: .15,.55,.95,1
            color: 1,1,1,1
            on_release: root.send()

"""

Builder.load_string(KV)

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
            except:
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
        except:
            pass

class Root(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client = ChatClient()

    def connect(self):

        username = self.ids.username.text.strip()

        if username == "":
            self.add_message("Enter username.")
            return

        self.ids.connect.disabled = True
        self.add_message("Connecting...")

        threading.Thread(
            target=self.connect_thread,
            args=(username,),
            daemon=True
        ).start()

    def connect_thread(self, username):

        try:

            self.client.connect(
                username,
                self.receive_message
            )

            Clock.schedule_once(
                lambda dt: self.connected()
            )

        except Exception as e:
            error = str(e)

            Clock.schedule_once(
                lambda dt, error=error: self.failed(error)
            )

    def connected(self):

        self.ids.status.text = "🟢 Online"

        self.add_message("Connected Successfully!")

    def failed(self, error):

        self.ids.connect.disabled = False

        self.ids.status.text = "🔴 Offline"

        self.add_message(error)

    def receive_message(self, message):

        Clock.schedule_once(
            lambda dt: self.add_message(message)
        )

    def add_message(self, message):

        self.ids.chat.text += message + "\n"

        self.ids.chat.cursor = (0, len(self.ids.chat.text))

    def send(self):

        message = self.ids.message.text.strip()

        if message == "":
            return

        self.client.send(message)

        self.ids.message.text = ""

    def enter_send(self):

        self.send()

class PyChat(App):

    def build(self):
        self.title = "PyChat"
        return Root()

PyChat().run()
