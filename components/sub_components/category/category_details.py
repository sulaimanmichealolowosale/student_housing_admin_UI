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

<CategoryDetails>:
    orientation: "vertical"

    MDBoxLayout:
        id:main_box
        orientation: 'vertical'
        size_hint: 1, .9
        spacing: '20dp'
        padding: ('10dp', '20dp', '10dp', '10dp')
            
        MDBoxLayout:
            size_hint_y:1
            spacing: '10dp'
            orientation: 'vertical'
            md_bg_color:rgba(255, 255, 255, 255)
            radius: [20]
            padding: ('10dp')
            height:self.minimum_height
            MDLabel:
                text:root.title
                halign:"center"
                font_style:"H6"
            MDLabel:
                id:description
                text:root.description
                halign:"center"
                font_style:"Subtitle1"
                size_hint_y: None
                height: self.texture_size[1]
            MDLabel:
                font_style:"H5"
                text: 'Properties count: ' + root.property_count
            MDLabel:
                font_style:"H5"
                text: 'Added By: ' + root.nick_name
            

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
                text: 'Delete category'
                size_hint_x: .5
                icon_color: 1 , 0 , 0 , 1
                text_color:1 , 0 , 0 , 1
                line_color:1 , 0 , 0 , 1
                on_release: root.delete_user()
    
    ''')


class CategoryDetails(MDScreen, MDBoxLayout):
    name = "category_details"
    access_token = StringProperty()
    role = StringProperty()
    user_id: int
    base_url = StringProperty()
    image_base_url = StringProperty()
    property_count = StringProperty()
    image_url = StringProperty()
    id = StringProperty()
    title = StringProperty()
    description = StringProperty()
    agent = StringProperty()
    nick_name = StringProperty()

    def to_update(self):
        if self.role == "agent":
            self.on_message(
                "You are not allowed to do that",
                background_color=(1, 0, 0, .7)
            )
            return
        else:
            self.parent.get_screen("update_category").id = self.id
            self.parent.current = "update_category"

    def on_message(self, message, background_color):
        toast(message, duration=5, background=background_color)

    def on_get_user(self, res):
        self.title = res['title']
        self.property_count = str(len(res['properties']))
        self.description = res['description']
        self.agent = str(res['agent_id'])
        self.nick_name = str(res['agent_nickname'])

        app = MDApp.get_running_app()
        app_bar = app.root.ids.app_bar
        app_bar.title = "Category Details"

    def _get_user(self):
        try:
            response = requests.get(
                url=f"{self.base_url}/category/{self.id}",
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
                url=f"{self.base_url}/category/{self.id}",
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
        self.parent.current = "manage_category"

    def on_enter(self):
        self.get_user()
