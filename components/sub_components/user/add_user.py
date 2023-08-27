from kivymd.uix.boxlayout import MDBoxLayout
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty, ListProperty
from kivy.clock import Clock

import requests
import threading
from kivymd.uix.datatables import MDDataTable
from kivy.uix.anchorlayout import AnchorLayout
from kivy.metrics import dp
from kivymd.uix.button import MDIconButton
from kivymd.toast import toast
from kivymd.app import MDApp
from components.loading_modal import LoadingModal


Builder.load_string('''

<DefaultTextField@MDTextField>:
    helper_text_color_focus:"white"
    helper_text_color_normal:"white"
    text_color_normal:1 , 1 , 1 , 1
    text_color_focus:1 , 1 , 1 , 1


<AddUser>:
    orientation: "vertical"
    MDScrollView:
        id:scroll
        effect_cls: "ScrollEffect"
        size_hint: 1, .9
        MDBoxLayout:
            id:main_box
            orientation: 'vertical'
            size_hint: 1, .9
            pos_hint:{"center_y":.5}
            spacing: '20dp'
            padding: ('10dp', '20dp', '10dp', '10dp')
            size_hint_y:None
            height:self.minimum_height

            DefaultTextField:
                id:first_name
                text:"Sulaiman"
                hint_text:"Firstname"
                hint_text_color_normal:"white"
                helper_text: "John"
                helper_text_mode: "persistent"
                background_color: app.theme_cls.bg_normal
                pos_hint:{"center_x":.5}
                cursor_color:rgba(0,0,59,255)
                font_size:"14sp"
                cursor_width:"2sp"
                multiline:False
            DefaultTextField:
                id:last_name
                text:"Micheal"
                hint_text:"Firstname"
                hint_text_color_normal:"white"
                helper_text: "Doe"
                helper_text_mode: "persistent"
                background_color: app.theme_cls.bg_normal
                pos_hint:{"center_x":.5}
                cursor_color:rgba(0,0,59,255)
                font_size:"14sp"
                cursor_width:"2sp"
                multiline:False
            DefaultTextField:
                id:nick_name
                text:"mickey"
                hint_text:"Nickname"
                hint_text_color_normal:"white"
                helper_text: "jonny"
                helper_text_mode: "persistent"
                background_color: app.theme_cls.bg_normal
                pos_hint:{"center_x":.5}
                cursor_color:rgba(0,0,59,255)
                font_size:"14sp"
                cursor_width:"2sp"
                multiline:False
            DefaultTextField:
                id:email
                text:"admin@admin.com"
                hint_text:"Email"
                hint_text_color_normal:"white"
                helper_text: "someone@something.com"
                helper_text_mode: "persistent"
                validator:"email"
                background_color: app.theme_cls.bg_normal
                pos_hint:{"center_x":.5, "center_y":.5}
                cursor_color:rgba(0,0,59,255)
                font_size:"14sp"
                cursor_width:"2sp"
                multiline:False
            DefaultTextField:
                id:phone
                text:"09056435678"
                hint_text:"Phone Number"
                hint_text_color_normal:"white"
                helper_text: "09056435678"
                helper_text_mode: "persistent"
                background_color: app.theme_cls.bg_normal
                pos_hint:{"center_x":.5, "center_y":.5}
                cursor_color:rgba(0,0,59,255)
                font_size:"14sp"
                cursor_width:"2sp"
                multiline:False
            Spinner:
                id: role
                text: "agent"
                values: root.values
                size_hint_y:None
                background_color: rgba(0, 128, 128, 255)
                color:1,1,1,1
                height:50
            DefaultTextField:
                id:password
                text:"sulaiman"
                hint_text:"Password"
                hint_text_color_normal:"white"
                hint_text:"Password"
                background_color: app.theme_cls.bg_normal
                pos_hint:{"center_x":.5}
                cursor_color:rgba(0,0,59,255)
                font_size:"14sp"
                cursor_width:"2sp"
                password:True
                multiline:False
            DefaultTextField:
                id:password_conf
                hint_text:"Confirm password"
                hint_text_color_normal:"white" if password.text == self.text else "red"
                background_color: app.theme_cls.bg_normal
                pos_hint:{"center_x":.5}
                cursor_color:rgba(0,0,59,255)
                font_size:"14sp"
                cursor_width:"2sp"
                password:True
                multiline:False
            MDRectangleFlatIconButton:
                text:"ADD NEW USER"
                icon:"database-plus-outline"
                size_hint_x:1
                text_color: 1 , 1 , 1 , 1
                line_color: 1 , 1 , 1 , 1
                icon_color: 1 , 1 , 1 , 1
                on_release: 
                    root.register()
        

''')


class AddUser(MDScreen, MDBoxLayout):
    name = "add_user"
    first_name = StringProperty()
    last_name = StringProperty()
    nick_name = StringProperty()
    access_token = StringProperty()
    base_url = StringProperty()
    role = StringProperty()
    image_base_url = StringProperty()
    user_count = StringProperty()
    category_count = StringProperty()
    property_count = StringProperty()
    data_tables = ObjectProperty()
    data = ObjectProperty()
    key = StringProperty()
    row_id_mapping = ObjectProperty()
    values = ListProperty()
    user_id: int
    id = StringProperty()
    message = StringProperty()
    message_color = (1, 1, 0, .7)

    def disable_role(self):
        if self.role == "admin":
            self.values = ["agent", "admin"]
        else:
            self.values = ["agent", "admin", "superadmin"]

    def register(self):
        t = threading.Thread(target=self._register)
        t.start()

    def on_register(self):
        Clock.schedule_once(lambda x: LoadingModal().close_modal())
        self.ids.first_name.text = ""
        self.ids.last_name.text = ""
        self.ids.nick_name.text = ""
        self.ids.email.text = ""
        self.ids.phone.text = ""
        self.ids.role.text = ""
        self.ids.password.text = ""
        self.parent.current = "manage_user"

    def on_register_message(self, message, background_color):
        Clock.schedule_once(lambda x: LoadingModal().close_modal())
        toast(message, duration=5, background=background_color)

    def _register(self):
        try:
            Clock.schedule_once(lambda x: LoadingModal().open_modal())
            data = {
                "first_name": self.ids.first_name.text,
                "last_name": self.ids.last_name.text,
                "nick_name": self.ids.nick_name.text,
                "email": self.ids.email.text,
                "phone": self.ids.phone.text,
                "role": self.ids.role.text,
                "password": self.ids.password.text,
            }

            if data['email'] == "" or data['first_name'] == "" or data["last_name"] == "" or data["nick_name"] == "" or data['password'] == "" or data['phone'] == "":
                Clock.schedule_once(lambda x: self.on_register_message(
                    message="Make sure no field is empty",
                    background_color=(1, 0, 0, .7)
                ))
                return

            elif data['password'] != self.ids.password_conf.text:
                Clock.schedule_once(lambda x: self.on_register_message(
                    message="Password Mismatch",
                    background_color=(1, 0, 0, .7)
                ))
                return
            else:
                response = requests.post(
                    url=f"{self.base_url}/user",
                    headers={
                        'Content-Type': 'application/json',
                        'Authorization': f'Bearer {self.access_token}'
                    },
                    json=data
                )

                if response.ok:
                    self.message = "User added successfully"
                    self.message_color = (0, 1, 0, .7)
                    Clock.schedule_once(lambda x: self.on_register())

                elif response.status_code == 409:
                    Clock.schedule_once(lambda x: self.on_register_message(
                        message="User already exist",
                        background_color=(1, 0, 0, .7)
                    ))

                elif response.status_code == 422:
                    self.message = "Make sure no field is empty"
                    self.message_color = (1, 0, 0, .7)

        except Exception as e:
            print(e)

    def on_enter(self):
        app = MDApp.get_running_app()
        app_bar = app.root.ids.app_bar
        app_bar.title = "Add User"
        self.disable_role()
