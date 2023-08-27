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
from components.loading_modal import LoadingModal


Builder.load_string('''

<DefaultTextField@MDTextField>:
    helper_text_color_focus:"white"
    helper_text_color_normal:"white"
    text_color_normal:1 , 1 , 1 , 1
    text_color_focus:1 , 1 , 1 , 1

<UpdateCategory>:
    orientation: "vertical"

    MDTopAppBar:
        pos_hint: {'top':1 }
        left_action_items: [["arrow-left", lambda x: root.back()]]
        title: "Update Category"

    MDBoxLayout:
        id:main_box
        orientation: 'vertical'
        size_hint: 1, None
        height:self.minimum_height
        pos_hint:{"center_y":.6}
        spacing: '30dp'
        padding: ('10dp', '20dp', '10dp', '10dp')

        DefaultTextField:
            id:title
            text:root.title
            hint_text:"Category title"
            helper_text: "Single room"
            hint_text_color_normal:"white"
            helper_text_mode: "persistent"
            background_color: app.theme_cls.bg_normal
            pos_hint:{"center_x":.5}
            cursor_color:rgba(0,0,59,255)
            font_size:"14sp"
            cursor_width:"2sp"
            multiline:False
        DefaultTextField:
            id:description
            text:root.description
            hint_text:"Category description"
            hint_text_color_normal:"white"
            helper_text: "This category consists of single rooms only"
            helper_text_mode: "persistent"
            background_color: app.theme_cls.bg_normal
            pos_hint:{"center_x":.5}
            cursor_color:rgba(0,0,59,255)
            font_size:"14sp"
            cursor_width:"2sp"
            multiline:True
        
        MDRectangleFlatIconButton:
            text:"UPDATE CATEGORY"
            icon:"database-plus-outline"
            size_hint_x:1
            text_color: 1 , 1 , 1 , 1
            line_color: 1 , 1 , 1 , 1
            icon_color: 1 , 1 , 1 , 1
            on_release: 
                root.update()
        

''')


class UpdateCategory(MDScreen, MDBoxLayout):
    name = "update_category"
    first_name = StringProperty()
    last_name = StringProperty()
    nick_name = StringProperty()
    access_token = StringProperty()
    base_url = StringProperty()
    role = StringProperty()
    image_base_url = StringProperty()
    user_count = StringProperty()
    user_id: int
    id = StringProperty()
    title = StringProperty()
    description = StringProperty()

    def back(self):
        self.parent.current = "category_details"

    def get_details(self):
        t = threading.Thread(target=self._get_details)
        t.start()

    def on_get_details(self, res):
        self.title = res['title']
        self.description = res['description']

    def _get_details(self):
        try:
            response = requests.get(
                url=f"{self.base_url}/category/{self.id}",
                headers={
                    'Authorization': f'Bearer {self.access_token}'
                },
            )

            res = response.json()
            Clock.schedule_once(lambda x: self.on_get_details(res))
        except Exception as e:
            print(e)

    def on_enter(self):
        self.get_details()

    def update(self):
        t = threading.Thread(target=self._update)
        t.start()

    def on_update(self):
        Clock.schedule_once(lambda x: LoadingModal().close_modal())

        self.ids.title.text = ""
        self.ids.description.text = ""
        self.parent.current = "manage_category"

    def on_update_message(self, message, background_color):
        Clock.schedule_once(lambda x: LoadingModal().close_modal())
        toast(message, duration=5, background=background_color)

    def _update(self):
        try:
            Clock.schedule_once(lambda x: LoadingModal().open_modal())
            data = {
                "title": self.ids.title.text,
                "description": self.ids.description.text,
            }

            if data['title'] == "" or data['description'] == "":
                Clock.schedule_once(lambda x: self.on_update_message(
                    message="Make sure no field is empty",
                    background_color=(1, 0, 0, .7)
                ))
                return
            else:
                response = requests.put(
                    url=f"{self.base_url}/category/{self.id}",
                    headers={
                        'Content-Type': 'application/json',
                        'Authorization': f'Bearer {self.access_token}'
                    },
                    json=data
                )

                if response.ok:
                    Clock.schedule_once(lambda x: self.on_update())

                elif response.status_code == 409:
                    Clock.schedule_once(lambda x: self.on_update_message(
                        message="Category already exist",
                        background_color=(1, 0, 0, .7)
                    ))

        except Exception as e:
            print(e)
