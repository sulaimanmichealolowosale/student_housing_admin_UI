from kivymd.uix.boxlayout import MDBoxLayout
from kivy.lang import Builder
from kivy.utils import get_color_from_hex
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty
import requests
import threading
from kivy.clock import Clock
from kivymd.uix.screen import MDScreen
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.app import MDApp


Builder.load_string('''

<Check@MDCheckbox>:
    group: 'group'
    size_hint: None, None
    size: dp(48), dp(48)

<LoginView>:

    MDFloatLayout:
        md_bg_color:1,1,1,1
    

        MDLabel:
            color:rgba(0,0,59, 255)
            text:"W E L C O M E !"
            font_size:"26sp"
            size_hint:1, .1
            pos_hint:{"center_x":.6,"center_y":.85}

        MDLabel:
            color:rgba(135,135,135, 255)
            text:"Sign in to continue!"
            font_size:"18sp"
            size_hint:1, .1
            pos_hint:{"center_x":.6,"center_y":.79}
        
        MDBoxLayout:
            orientation: "vertical"
            size_hint_x: .8
            spacing: "20dp"
            adaptive_height: True
            pos_hint: {"center_x": .5, "center_y": .5}
            # md_bg_color:.4, .5,.2,.4
            MDTextField:
                id:email
                text:"superuser@superuser.com"
                hint_text:"Email"
                helper_text: "someone@something.com"
                helper_text_mode: "persistent"
                validator:"email"
                background_color: app.theme_cls.bg_normal
                pos_hint:{"center_x":.5, "center_y":.5}
                cursor_color:rgba(0,0,59,255)
                font_size:"14sp"
                cursor_width:"2sp"
                multiline:False
            MDTextField:
                id:password
                text:"sulaiman"
                hint_text:"Password"
                pos_hint:{"center_x":.5, "center_y":.5}
                foreground_color:rgba(0,0,59,255)
                cursor_color:rgba(0,0,59,255)
                font_size:"14sp"
                cursor_width:"2sp"
                multiline:False
                password:True
        MDFloatLayout:
            pos_hint:{"left":1, "center_y":.5}
            size_hint:1, .2
            MDIconButton:
                icon: "eye-off"
                theme_text_color: "Hint"
                pos_hint:{"center_x":.8,"center_y":.23}
                on_release:
                    self.icon = "eye" if self.icon == "eye-off" else "eye-off"
                    password.password = False if password.password is True else True

        MDRectangleFlatIconButton:
            id:login_btn
            icon: "login"
            text:"LOGIN"
            pos_hint:{"center_x":.5, "center_y":.34}
            size_hint:.6, None
            background_color:0,0,0,0
            on_press:
                root.login()

        MDLabel:
            text:root.error_text
            color:1,0,0,.7
            pos_hint:{"center_x":.5, "center_y":.2}
            halign:"center"

        MDSpinner:
            active:root.spinner_state
            size_hint:None, None
            height: dp(50)
            width: dp(50)
            pos_hint:{'center_x': .5, 'center_y': .2}

''')

# BASE_URL = "http://192.168.0.101:8000"
# IMAGE_BASE_URL = "http://192.168.0.101:8000"

BASE_URL = "https://student-housing.onrender.com"
IMAGE_BASE_URL = "https://student-housing.onrender.com"


class LoginView(MDScreen, MDBoxLayout):
    spinner_state = BooleanProperty(False)
    error_text = StringProperty()
    name = "login"
    profile_image = StringProperty()

    def login(self):
        t = threading.Thread(target=self._login)
        t.start()

    def send_to_screen(
            self,
            *args,
            access_token,
            first_name,
            last_name,
            nick_name,
            id,
            role,
            email,
            profile_picture,
    ):
        screens = [self.parent.get_screen(f"{key}") for key in args]
        for screen in screens:
            screen.first_name = first_name
            screen.last_name = last_name
            screen.role = role
            screen.email = email
            screen.nick_name = nick_name
            screen.access_token = access_token
            screen.user_id = id
            screen.base_url = BASE_URL
            screen.image_base_url = IMAGE_BASE_URL
            screen.profile_picture = f"{IMAGE_BASE_URL}/{profile_picture}"

    def on_login_complete(self, res):
        self.parent.current = "dashboard"
        app = MDApp.get_running_app()
        picture = app.root.ids.profile_picture
        picture.source = f"{IMAGE_BASE_URL}/{res['image_url']}"

    def _login(self):
        self.spinner_state = True
        try:
            email_field = self.ids.email
            password_field = self.ids.password
            data = {
                "username": email_field.text,
                "password": password_field.text
            }
            response = requests.post(
                url=f"{BASE_URL}/auth/",
                headers={
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                data=data

            )

            res = response.json()
            if response.ok:
                Clock.schedule_once(
                    lambda x: self.show_error(""))
                Clock.schedule_once(
                    lambda x: self.on_login_complete(res))
                Clock.schedule_once(
                    lambda x: self.send_to_screen(
                        "dashboard",
                        "manage_user",
                        "add_user",
                        "user_details",
                        "manage_category",
                        "add_category",
                        "category_details",
                        "update_category",
                        "update_user",
                        "manage_property",
                        "add_property",
                        "property_details",
                        "update_property",
                        "account",
                        first_name=res['first_name'],
                        last_name=res['last_name'],
                        access_token=res['access_token'],
                        nick_name=res['nick_name'],
                        id=res['id'],
                        role=res['role'],
                        email=res['email'],
                        profile_picture=res['image_url'],

                    )
                )

            elif response.status_code == 422:
                Clock.schedule_once(
                    lambda x: self.show_error("Either of the fields is empty"))

            elif response.status_code == 403:
                Clock.schedule_once(
                    lambda x: self.show_error("Invalid credentials"))

        except Exception as e:
            self.spinner_state = False
            Clock.schedule_once(
                lambda x: self.show_error("Internal server error"))

    def show_error(self, message):

        self.spinner_state = False
        self.error_text = message
