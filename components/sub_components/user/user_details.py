from kivymd.uix.boxlayout import MDBoxLayout
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty
from kivy.clock import Clock

import requests
import threading
from kivymd.uix.datatables import MDDataTable
from kivy.uix.anchorlayout import AnchorLayout
from kivy.metrics import dp
from kivymd.uix.button import MDIconButton
from kivymd.toast import toast
from kivymd.app import MDApp

Builder.load_string('''
<DefaultLabel@MDLabel>:
    font_style:"H6"

<UserDetails>:
    orientation: "vertical"

    MDBoxLayout:
        id:main_box
        orientation: 'vertical'
        size_hint: 1, .9
        spacing: '20dp'
        padding: ('10dp', '20dp', '10dp', '10dp')

        MDBoxLayout:
            # md_bg_color:rgba(26, 62, 255, 255)
            id:image_box
            size_hint:None, None
            size: '170dp','170dp'
            pos_hint: {'center_x': .5 }
            FitImage:
                source:root.image_url
                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                size_hint: 1, 1
                mipmap:True
                allow_stretch: False
                radius: [100]

        MDBoxLayout:
            orientation: 'vertical'
            spacing: '25dp'
            size_hint:1, None
            height: dp(70)
            MDLabel:
                text:root.full_name
                halign:"center"
                font_style:"H6"
                color: 1 , 1 , 1 , 1
            MDLabel:
                text:root.email
                halign:"center"
                font_style:"Subtitle1"
                color: 1 , 1 , 1 , 1
            MDLabel:
                text:root.nick_name
                halign:"center"
                font_style:"Subtitle2"
                color: 1 , 1 , 1 , 1
            MDLabel:
                text:root.selectet_user_role
                halign:"center"
                font_style:"Caption"
                color: 1 , 1 , 1 , 1
        MDBoxLayout:
            size_hint_y:1
            spacing: '10dp'
            orientation: 'vertical'
            md_bg_color:rgba(255, 255, 255, 255)
            radius: [20]
            padding: ('10dp')
            MDLabel:
                font_style:"H5"
                text: 'Categories added: ' + root.category_count
            MDLabel:
                font_style:"H5"
                text: 'Properties added: ' + root.property_count
            # MDLabel:
            #     font_style:"H5"
            #     text: 'Rating: ' + root.rating

        MDBoxLayout:
            size_hint:1, .2
            spacing: '20dp'
            orientation: 'horizontal'

            MDRectangleFlatIconButton:
                icon: "update"
                text: 'Update details'
                size_hint_x:.5
                icon_color: 1 , 1 , 0 , 1
                text_color:1 , 1 , 0 , 1
                line_color:1 , 1 , 0 , 1
                on_release: root.to_update()

            MDRectangleFlatIconButton:
                icon:"delete-outline"
                text: 'Delete user'
                size_hint_x: .5
                icon_color: 1 , 0 , 0 , 1
                text_color:1 , 0 , 0 , 1
                line_color:1 , 0 , 0 , 1
                on_release: root.delete_user()

            

    
    ''')


class UserDetails(MDScreen, MDBoxLayout):
    name = "user_details"
    first_name = StringProperty()
    last_name = StringProperty()
    nick_name = StringProperty()
    access_token = StringProperty()
    role = StringProperty()
    selectet_user_role = StringProperty()
    email = StringProperty()
    user_id: int
    base_url = StringProperty()
    image_base_url = StringProperty()
    image_url = StringProperty()
    category_count = StringProperty()
    property_count = StringProperty()
    rating = StringProperty()
    id = StringProperty()
    message = StringProperty()
    message_color = (1, 1, 0, .7)
    full_name = StringProperty()

    def to_update(self):
        if self.role == "agent":
            self.on_message(
                "You are not allowed to do that",
                background_color=(1, 0, 0, .7)
            )
            return
        else:
            self.parent.get_screen("update_user").id = self.id
            self.parent.current = "update_user"

    def on_message(self, message, background_color):
        toast(message, duration=5, background=background_color)

    def on_get_user(self, res):
        self.image_url = f"{self.image_base_url}/{res['image_url']}"
        self.full_name = f"{res['first_name']} {res['last_name']}"
        self.nick_name = res['nick_name']
        self.category_count = str(len(res['categories']))
        self.property_count = str(len(res['properties']))
        self.rating = str(res['rating'])
        self.selectet_user_role = res['role']
        self.email = res['email']
        app = MDApp.get_running_app()
        app_bar = app.root.ids.app_bar
        app_bar.title = "User Details"

    def _get_user(self):
        try:
            response = requests.get(
                url=f"{self.base_url}/user/{self.id}",
                headers={
                    'Authorization': f'Bearer {self.access_token}'
                },
            )

            res = response.json()
            Clock.schedule_once(lambda x: self.on_get_user(res))
        except Exception as e:
            print(e)

    def get_user(self):
        t = threading.Thread(target=self._get_user)
        t.start()

    def _delete_user(self):
        try:
            response = requests.delete(
                url=f"{self.base_url}/user/{self.id}",
                headers={
                    'Authorization': f'Bearer {self.access_token}'
                },
            )

            Clock.schedule_once(lambda x: self.on_delete())
        except Exception as e:
            return

    def delete_user(self):
        if self.role == "agent":
            self.on_message(
                "You are not allowed to do that",
                background_color=(1, 0, 0, .7)
            )
            return
        else:
            t = threading.Thread(target=self._delete_user)
            t.start()

    def on_delete(self):
        self.parent.current = "manage_user"

    def on_enter(self):
        self.get_user()
