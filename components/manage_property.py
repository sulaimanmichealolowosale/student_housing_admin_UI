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
from kivy.uix.image import AsyncImage
from kivymd.toast import toast
from kivymd.app import MDApp


Builder.load_string('''
<ManageProperty>:
    orientation: "vertical"
    MDBoxLayout:
        id:main_box
        orientation: 'vertical'
        size_hint: 1, .9
        spacing: '15dp'
        padding: ('10dp', '20dp', '10dp', '10dp')
        color: 1 , 1 , 1 , 1

        MDBoxLayout:
            id:box
            orientation: 'horizontal'
            pos_hint: {'center_x': .5}
            size_hint: 1, .1
            spacing: '10dp'
            padding: ('10dp')
            MDRectangleFlatIconButton:
                id:add_new_btn
                icon:"database-plus-outline"
                text:"ADD NEW PROPERTY"
                pos_hint: {'center_y': .5}
                text_color: 1 , 1 , 1 , 1
                line_color: 1 , 1 , 1 , 1
                icon_color: 1 , 1 , 1 , 1
                on_release: root.to_add_property()
            MDTextField:
                id:search_field
                hint_text:"Search"
                hint_text_color_normal:"white"
                hint_text_color_focus:"white"
                helper_text_color_focus:"white"
                helper_text_color_normal:"white"
                text_color_normal:1 , 1 , 1 , 1
                text_color_focus:1 , 1 , 1 , 1
                helper_text: "search by: all fields..."
                helper_text_mode: "persistent"
                background_color: app.theme_cls.bg_normal
                pos_hint:{"center_y":.5}
                cursor_color:1 , 1 , 1 , 1
                font_size:"14sp"
                cursor_width:"2sp"
                multiline:False
                on_text: root.on_search()
        MDBoxLayout:
            id:table_box 

    MDSpinner:
        active:root.spinner_state
        size_hint:None, None
        height: dp(50)
        width: dp(50)
        pos_hint:{'center_x': .5, 'center_y': .5}
''')


class ManageProperty(MDScreen, MDBoxLayout):
    name = "manage_property"
    first_name = StringProperty()
    last_name = StringProperty()
    nick_name = StringProperty()
    access_token = StringProperty()
    role = StringProperty()
    base_url = StringProperty()
    image_base_url = StringProperty()
    user_count = StringProperty()
    category_count = StringProperty()
    property_count = StringProperty()
    data_tables = ObjectProperty()
    data = ObjectProperty()
    key = StringProperty()
    row_id_mapping = ObjectProperty()
    user_id: int
    search_text = StringProperty()
    spinner_state = BooleanProperty(True)

    def on_search(self):
        t = threading.Thread(target=self._on_search)
        t.start()

    def on_search_success(self):
        self.search_text = self.ids.search_field.text
        self._get_property()

    def _on_search(self):
        Clock.schedule_once(lambda x: self.on_search_success())

    def to_add_property(self):
        if self.role == "admin":
            toast("You are not allow to do that", background=(1, 0, 0, .7))
            return
        else:
            self.parent.current = "add_property"

    def get_table(self):
        try:
            layout = AnchorLayout()
            self.data_tables = MDDataTable(
                size_hint=(1, 1),
                use_pagination=True,
                column_data=[
                    ("ID", dp(15)),
                    ("Title", dp(40)),
                    ("Description", dp(80)),
                    ("Agent", dp(30)),
                    ("Status", dp(15)),
                    ("Type", dp(20)),
                    ("Price", dp(20)),
                    ("Duration", dp(25)),
                ],
            )

            self.data_tables.bind(on_row_press=self.on_row_press)

            layout.add_widget(self.data_tables)
            table_box = self.ids.table_box
            table_box.add_widget(layout)

        except Exception as e:
            print(e)

    def on_row_press(self, instance_table, instance_row):
        try:
            num = ''
            data = ''
            for index, row_data in enumerate(instance_table.row_data):
                num = int(instance_row.text)
                if instance_row.text in row_data:
                    data = row_data
            if instance_row.text in data:
                selected_id = self.row_id_mapping[num]
                self.parent.current = "property_details"
                self.parent.get_screen(
                    "property_details").id = str(selected_id)

        except Exception as e:
            toast("Please select from the ID field")

    def get_property(self):
        t = threading.Thread(target=self._get_property)
        t.start()

    def on_get_property(self):
        try:

            app = MDApp.get_running_app()
            app_bar = app.root.ids.app_bar
            app_bar.title = "Properties"
            
            self.spinner_state = False
            self.row_id_mapping = {}
            row_data = []
            for key, item in enumerate(self.data):
                self.row_id_mapping[key+1] = item['id']
                row = (
                    f"{key+1}",
                    f"{item['title']}",
                    f"{item['description']}"[:100] + "...",
                    f"{item['agent_nickname']}",
                    ('close', [1, 0, 0, 1], "")
                    if item['property_status'] == "unavailable" else (
                        'check', [0, 1, 0, 1], ""),
                    f"{item['property_type']}",
                    f"\u20a6{item['price']}",
                    f"{item['payment_duration']}",
                )
                row_data.append(row)
            self.data_tables.row_data = row_data
            toast(f"Total properties: {len(self.data)}")
        except Exception as e:
            print(e)

    def _get_property(self):
        self.spinner_state = True

        try:
            response = requests.get(
                url=f"{self.base_url}/property/?search={self.search_text}",
                headers={
                    'Authorization': f'Bearer {self.access_token}'
                }
            )
            if response.ok:
                self.spinner_state = False
                res = response.json()
                self.data = res
                Clock.schedule_once(lambda x: self.on_get_property())

        except Exception as e:
            print(e)

    def on_enter(self):
        self.get_table()
        self.get_property()

    def on_leave(self):
        table_box = self.ids.table_box
        table_box.clear_widgets()
