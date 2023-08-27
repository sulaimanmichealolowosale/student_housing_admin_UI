from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty
from kivy.clock import Clock
from kivymd.app import MDApp
from components.loading_modal import LoadingModal


import requests
import threading


Builder.load_string('''

<DefaultLabel@MDLabel>:
    font_style:"Subtitle1"
    color: 1 , 1 , 1 , 1

<DefaultMDLabel@MDLabel>:
    theme_text_color:"Custom"
    color: 1 , 0 , 0 , 1
    halign:"center"
    font_style:"H5"


<Card@MDCard>:
    orientation:"vertical"
    md_bg_color:rgba(0, 128, 128, 255)
    size_hint_y: None
    height:"160dp"
    ripple_behavior: True
    radius:[10, ]

<DashboardView>:
    orientation: "vertical"
    MDBoxLayout:
        orientation: 'vertical'
        size_hint: 1, .9
        spacing: '10dp'
        padding: ('10dp', '20dp', '10dp', '10dp')
        MDBoxLayout:
            orientation: 'horizontal'
            size_hint: 1, .03
            padding:10
            # md_bg_color:rgba(54, 65, 100, 255)
            DefaultLabel:
                text: root.first_name +" "+ root.last_name
                halign:"left"
            DefaultLabel:
                text: root.nick_name
                halign:"right"

        MDGridLayout:
            cols:2
            spacing: '10dp'
            Card:
                MDIcon:
                    icon: "account"
                    pos_hint: {"center_x": .5, "center_y": .5}
                    theme_text_color:"Custom"
                    color: 1 , 1 , 1 , 1
                    font_size:"100dp"
                    badge_font_size:"45dp"
                DefaultLabel:
                    text:"USERS"
                    theme_text_color:"Custom"
                    color: 1 , 1 , 1 , 1
                    halign:"center"
                DefaultMDLabel:
                    text:root.user_count
                    
            Card:
                MDIcon:
                    icon: "playlist-check"
                    pos_hint: {"center_x": .5, "center_y": .5}
                    theme_text_color:"Custom"
                    color: 1 , 1 , 1 , 1
                    font_size:"100dp"
                    badge_font_size:"45dp"
                DefaultLabel:
                    text:"CATEGORIES"
                    theme_text_color:"Custom"
                    color: 1 , 1 , 1 , 1
                    halign:"center"
                DefaultMDLabel:
                    text:root.category_count
            Card:
                MDIcon:
                    icon: "home-city"
                    pos_hint: {"center_x": .5, "center_y": .5}
                    theme_text_color:"Custom"
                    color: 1 , 1 , 1 , 1
                    font_size:"100dp"
                    badge_font_size:"45dp"
                DefaultLabel:
                    text:"PROPERTIES"
                    theme_text_color:"Custom"
                    color: 1 , 1 , 1 , 1
                    halign:"center"
                DefaultMDLabel:
                    text:root.property_count
 
    
''')


class DashboardView(MDScreen, BoxLayout):
    name = "dashboard"
    first_name = StringProperty()
    last_name = StringProperty()
    nick_name = StringProperty()
    access_token = StringProperty()
    base_url = StringProperty()
    profile_picture = StringProperty()
    image_base_url = StringProperty()
    user_count = StringProperty()
    category_count = StringProperty()
    property_count = StringProperty()
    user_id: int

    def make_requests(self):
        t = threading.Thread(target=self._make_requests)
        t.start()

    def _make_requests(self):
        try:
            Clock.schedule_once(lambda x: LoadingModal().open_modal())
            headers = {
                'Authorization': f'Bearer {self.access_token}'
            }
            user_response = requests.get(
                url=f"{self.base_url}/user/get-users/all",
                headers=headers
            )
            if self.role == "agent":
                property_response = requests.get(
                    url=f"{self.base_url}/property/get-properties/mine/all",
                    headers=headers
                )
                category_response = requests.get(
                    url=f"{self.base_url}/category//get-categories/mine/all",
                    headers=headers
                )
            else:
                property_response = requests.get(
                    url=f"{self.base_url}/property/get-properties/all",
                    headers=headers
                )
                category_response = requests.get(
                    url=f"{self.base_url}/category/get-categories/all",
                    headers=headers
                )
            property_res = property_response.json()
            category_res = category_response.json()
            user_res = user_response.json()

            if user_response.ok:
                Clock.schedule_once(lambda x: LoadingModal().close_modal())

            self.property_count = str(len(property_res))
            self.category_count = str(len(category_res))
            self.user_count = str(len(user_res))

        except Exception as e:
            print(e)

    def on_enter(self):
        app = MDApp.get_running_app()
        app_bar = app.root.ids.app_bar
        app_bar.title = "Dashboard"
        self.make_requests()
