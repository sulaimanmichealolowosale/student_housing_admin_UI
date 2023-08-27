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
from components.image_modal import ImageModal
from kivymd.app import MDApp

Builder.load_string('''
<DefaultLabel@MDLabel>:
    font_style:"H6"

<PropertyDetails>:
    orientation: "vertical"
    MDScrollView:
        id:scroll
        effect_cls: "ScrollEffect"
        size_hint: 1, .9

        MDBoxLayout:
            id:main_box
            orientation: 'vertical'
            spacing: '20dp'
            padding: ('10dp', '20dp', '10dp', '10dp')
            pos_hint:{"center_y":.5}
            size_hint_x:None
            size_hint_y:None
            size:(root.width, root.height)
            height:self.minimum_height

            MDBoxLayout:
                # md_bg_color:rgba(26, 62, 255, 255)
                id:image_box
                size_hint:1, None
                height: dp(200)
                pos_hint: {'center_x': .5 }
                MDSmartTile:
                    source:root.image_url
                    pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                    size_hint: 1, 1
                    mipmap:True
                    box_color:[0,0,0,0]
                    allow_stretch: False
                    on_release: root.open_modal(self)
                    # radius: [100]

            MDBoxLayout:
                orientation: 'vertical'
                spacing: '40dp'
                size_hint:1, None
                height:self.minimum_height
                md_bg_color:rgba(255, 255, 255, 255)
                radius: [20]
                padding: ('10dp', '10dp', '10dp', '10dp')
                
                # height: dp(70)
                MDLabel:
                    text:root.title
                    halign:"center"
                    font_style:"H5"
                    size_hint_y: None
                    height: self.texture_size[1]

                MDLabel:
                    font_style:"H5"
                    text: 'Description: '

                MDLabel:
                    text:root.description
                    halign:"left"
                    font_style:"Subtitle1"
                    size_hint_y: None
                    height: self.texture_size[1]
                MDLabel:
                    font_style:"H5"
                    text: 'Price: '

                MDLabel:
                    text:root.price
                    halign:"left"
                    font_style:"Subtitle1"
                    size_hint_y: None
                    height: self.texture_size[1]

                MDLabel:
                    font_style:"H5"
                    text: 'Payment duration: '

                MDLabel:
                    text:root.payment_duration
                    halign:"left"
                    font_style:"Subtitle1"
                    size_hint_y: None
                    height: self.texture_size[1]

            MDBoxLayout:
                spacing: '40dp'
                orientation: 'vertical'
                md_bg_color:rgba(255, 255, 255, 255)
                radius: [20]
                padding: ('20dp')
                size_hint_y:None
                height:self.minimum_height

                MDLabel:
                    font_style:"H5"
                    text: 'Category:'
                MDLabel:
                    text:root.category_title
                    font_style:"Subtitle1"
                    height: self.texture_size[1]
                    halign:"left"

                MDLabel:
                    font_style:"H5"
                    text: 'Agent: '

                MDBoxLayout:
                    size_hint: 1, None
                    height:self.minimum_height
                    spacing: '40dp'
                    orientation: 'vertical'

                    MDLabel:
                        text: "Email: " + root.agent_email
                        font_style:"Body1"
                    MDLabel:
                        text: "Fullname: " + root.agent_fullname
                        font_style:"Body1"
                    MDLabel:
                        text: "Nickname: " + root.agent_nickname
                        font_style:"Body1"
                    # MDLabel:
                    #     text: "Rating: " + root.agent_rating
                    #     font_style:"Body1"

            MDBoxLayout:
                size_hint:1, None
                height:self.minimum_height
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
                    text: 'Delete property'
                    size_hint_x: .5
                    icon_color: 1 , 0 , 0 , 1
                    text_color:1 , 0 , 0 , 1
                    line_color:1 , 0 , 0 , 1
                    on_release: root.delete_property()

    
    ''')


class PropertyDetails(MDScreen, MDBoxLayout):
    name = "property_details"
    title = StringProperty()
    description = StringProperty()
    agent_nickname = StringProperty()
    agent_fullname = StringProperty()
    agent_email = StringProperty()
    price = StringProperty()
    payment_duration = StringProperty()
    access_token = StringProperty()
    role = StringProperty()
    selectet_user_role = StringProperty()
    user_id: int
    base_url = StringProperty()
    image_base_url = StringProperty()
    image_url = StringProperty()
    category_title = StringProperty()
    agent_rating = StringProperty()
    id = StringProperty()
    agent_id = StringProperty()

    def open_modal(self, instance):
        modal = ImageModal()
        modal.open_modal(instance=instance)


    def to_update(self):

        if str(self.user_id) == self.agent_id:
            self.parent.get_screen("update_property").id = self.id
            self.parent.current = "update_property"

        elif self.role == "superuser":
            self.parent.get_screen("update_property").id = self.id
            self.parent.current = "update_property"

        else:
            self.on_message(
                "You are not allowed to do that",
                background_color=(1, 0, 0, .7)
            )
            return

    def on_message(self, message, background_color):
        toast(message, duration=5, background=background_color)

    def on_get_property(self, res):
        self.image_url = f"{self.image_base_url}/{res['primary_image_path']}"
        self.title = res['title']
        self.price = res['price']
        self.payment_duration = res['payment_duration']
        self.description = res['description']
        self.category_title = res['category']['title']
        self.agent_fullname = f"{res['agent']['first_name']} {res['agent']['last_name']}"
        self.agent_email = res['agent']['email']
        self.agent_nickname = res['agent']['nick_name']
        self.agent_rating = str(res['agent']['rating'])
        self.agent_id = str(res['agent_id'])
        app = MDApp.get_running_app()
        app_bar = app.root.ids.app_bar
        app_bar.title = "Property Details"
        # self.selectet_user_role = res['role']
        # self.email = res['email']

    def _get_property(self):
        try:
            response = requests.get(
                url=f"{self.base_url}/property/{self.id}",
                headers={
                    'Authorization': f'Bearer {self.access_token}'
                },
            )

            res = response.json()
            Clock.schedule_once(lambda x: self.on_get_property(res))
        except Exception as e:
            print(e)

    def get_property(self):
        t = threading.Thread(target=self._get_property)
        t.start()

    def _delete_property(self):
        try:
            response = requests.delete(
                url=f"{self.base_url}/property/{self.id}",
                headers={
                    'Authorization': f'Bearer {self.access_token}'
                },
            )

            Clock.schedule_once(lambda x: self.on_delete())
        except Exception as e:
            return

    def delete_property(self):
        if str(self.user_id) == self.agent_id:
            t = threading.Thread(target=self._delete_property)
            t.start()

        elif self.role == "admin" or self.role == "superuser":
            t = threading.Thread(target=self._delete_property)
            t.start()
        else:
            self.on_message(
                "You are not allowed to do that",
                background_color=(1, 0, 0, .7)
            )
            return

    def on_delete(self):
        self.parent.current = "manage_property"

    def on_enter(self):
        self.get_property()
