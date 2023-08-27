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
<ManageCategory>:
    orientation: "vertical"
    MDBoxLayout:
        id:main_box
        orientation: 'vertical'
        size_hint: 1, .9
        spacing: '15dp'
        padding: ('10dp', '20dp', '10dp', '10dp')

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
                text:"ADD NEW CATEGORY"
                pos_hint: {'center_y': .5}
                text_color: 1 , 1 , 1 , 1
                line_color: 1 , 1 , 1 , 1
                icon_color: 1 , 1 , 1 , 1
                on_release: root.to_add_user()
            MDTextField:
                id:search_field
                hint_text:"Search"
                helper_text: "search by: title, agent"
                helper_text_mode: "persistent"
                hint_text_color_normal:"white"
                hint_text_color_focus:"white"
                helper_text_color_focus:"white"
                helper_text_color_normal:"white"
                text_color_normal:1 , 1 , 1 , 1
                text_color_focus:1 , 1 , 1 , 1
                background_color: app.theme_cls.bg_normal
                pos_hint:{"center_y":.5}
                cursor_color:rgba(0,0,59,255)
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


class ManageCategory(MDScreen, MDBoxLayout):
    name = "manage_category"
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
        self._get_category()

    def _on_search(self):
        Clock.schedule_once(lambda x: self.on_search_success())

    def to_add_user(self):
        if self.role == "admin":
            toast("You are not allow to do that", background=(1, 0, 0, .7))
            return
        else:
            self.parent.current = "add_category"

    def get_table(self):
        try:

            layout = AnchorLayout()
            self.data_tables = MDDataTable(
                size_hint=(1, 1),
                use_pagination=True,
                column_data=[
                    ("ID", dp(15)),
                    ("Title", dp(50)),
                    ("Agent", dp(30)),
                    ("Description", dp(70)),
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
                self.parent.current = "category_details"
                self.parent.get_screen(
                    "category_details").id = str(selected_id)

        except Exception as e:
            toast("Please select from the ID field")

    def get_category(self):
        t = threading.Thread(target=self._get_category)
        t.start()

    def on_get_category(self):
        try:
            app = MDApp.get_running_app()
            app_bar = app.root.ids.app_bar
            app_bar.title = "Categories"
            self.spinner_state = False
            self.row_id_mapping = {}
            row_data = []
            for key, item in enumerate(self.data):
                self.row_id_mapping[key+1] = item['id']
                row = (
                    f"{key+1}",
                    f"{item['title']}",
                    f"{item['agent_nickname']}",
                    f"{item['description']}",
                )
                row_data.append(row)
            self.data_tables.row_data = row_data
            toast(f"Total categories: {len(self.data)}")
        except Exception as e:
            print(e)

    def _get_category(self):
        self.spinner_state = True

        try:
            response = requests.get(
                url=f"{self.base_url}/category/?search={self.search_text}",
                headers={
                    'Authorization': f'Bearer {self.access_token}'
                }
            )
            if response.ok:
                self.spinner_state = False
                res = response.json()
                self.data = res
                Clock.schedule_once(lambda x: self.on_get_category())
            return res

        except Exception as e:
            print(e)

    def on_enter(self):
        self.get_table()
        self.get_category()

    def on_leave(self):
        table_box = self.ids.table_box
        table_box.clear_widgets()
