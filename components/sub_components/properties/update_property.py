from kivymd.uix.boxlayout import MDBoxLayout
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty, ListProperty, DictProperty
from kivy.clock import Clock

import requests
import threading
from kivymd.uix.datatables import MDDataTable
from kivy.uix.anchorlayout import AnchorLayout
from kivy.metrics import dp
from kivymd.uix.button import MDIconButton
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.list import ImageLeftWidget
from kivymd.toast import toast
import os
from kivy.utils import platform
from kivy.utils import get_color_from_hex
from components.loading_modal import LoadingModal


Builder.load_string('''

<DefaultTextField@MDTextField>:
    helper_text_color_focus:"white"
    helper_text_color_normal:"white"
    text_color_normal:1 , 1 , 1 , 1
    text_color_focus:1 , 1 , 1 , 1

<UpdateProperty>:
    orientation: "vertical"

    MDTopAppBar:
        pos_hint: {'top':1 }
        left_action_items: [["arrow-left", lambda x: root.back()]]
        title: "Update Property"

    MDScrollView:
        id:scroll
        effect_cls: "ScrollEffect"
        size_hint: 1, .9
        MDBoxLayout:
            id:main_box
            orientation: 'vertical'
            pos_hint:{"center_y":.5}
            spacing: '30dp'
            padding: ('10dp', '20dp', '10dp', '10dp')
            size_hint_y:None
            height:self.minimum_height
            

            MDLabel:
                text: 'All fields with red hint text are required'
                size_hint: 1, None
                height: dp(10)
                halign:"center"
                color: rgba(255, 0, 0, 200)
                font_style:"Caption"
                color: 1 , 1 , 1 , 1

            DefaultTextField:
                id:title
                text:root.title
                hint_text:"Title"
                hint_text_color_normal:"red"
                helper_text: "eg: single single room, room self-contained"
                helper_text_mode: "on_focus"
                background_color: app.theme_cls.bg_normal
                pos_hint:{"center_x":.5}
                cursor_color:rgba(0,0,59,255)
                font_size:"14sp"
                cursor_width:"2sp"
                multiline:True
            
            DefaultTextField:
                id:description
                text:root.description
                hint_text:"Description"
                hint_text_color_normal:"red"
                helper_text: "Including size, features, distance from school etc."
                helper_text_mode: "on_focus"
                background_color: app.theme_cls.bg_normal
                pos_hint:{"center_x":.5}
                cursor_color:rgba(0,0,59,255)
                font_size:"14sp"
                cursor_width:"2sp"
                multiline:True

            DefaultTextField:
                id:address
                text:root.address
                hint_text:"Address"
                helper_text: "eg: school two, deuteronomy etc."
                hint_text_color_normal:"red"
                # hint_text_color_focus:"red"
                helper_text_mode: "on_focus"
                background_color: app.theme_cls.bg_normal
                pos_hint:{"center_x":.5}
                cursor_color:rgba(0,0,59,255)
                font_size:"14sp"
                cursor_width:"2sp"
                multiline:True
            DefaultTextField:
                id:security_type
                text:root.security_type
                hint_text:"Security Type"
                hint_text_color_normal:"red"
                helper_text: "Fenced with security personnel"
                helper_text_mode: "on_focus"
                background_color: app.theme_cls.bg_normal
                pos_hint:{"center_x":.5, "center_y":.5}
                cursor_color:rgba(0,0,59,255)
                font_size:"14sp"
                cursor_width:"2sp"
                multiline:True
            DefaultTextField:
                id:water_system
                text:root.water_system
                hint_text:"Water System"
                hint_text_color_normal:"red"
                helper_text: "eg: tap water, well water"
                helper_text_mode: "on_focus"
                background_color: app.theme_cls.bg_normal
                pos_hint:{"center_x":.5, "center_y":.5}
                cursor_color:rgba(0,0,59,255)
                font_size:"14sp"
                cursor_width:"2sp"
                multiline:True
            DefaultTextField:
                id:toilet_bathroom_description
                text:root.toilet_bathroom_description
                hint_text:"Toilet and Bathroom Description"
                hint_text_color_normal:"red"
                helper_text: "eg: One bathroom and one toilet"
                helper_text_mode: "on_focus"
                background_color: app.theme_cls.bg_normal
                pos_hint:{"center_x":.5, "center_y":.5}
                cursor_color:rgba(0,0,59,255)
                font_size:"14sp"
                cursor_width:"2sp"
                multiline:True
            DefaultTextField:
                id:kitchen_description
                text:root.kitchen_description
                hint_text:"Kitchen Description"
                helper_text: "eg: One kitchen"
                helper_text_mode: "on_focus"
                background_color: app.theme_cls.bg_normal
                pos_hint:{"center_x":.5, "center_y":.5}
                cursor_color:rgba(0,0,59,255)
                font_size:"14sp"
                cursor_width:"2sp"
                multiline:True
            Spinner:
                id: property_status
                text: root.property_status
                values: ["available", "unavailable"]
                size_hint_y:None
                background_color: rgba(0, 128, 128, 255)
                color:1,1,1,1
                height:50
            Spinner:
                id: property_type
                text: root.property_type
                values: ["Rent", "Sale", "Lease"]
                size_hint_y:None
                background_color: rgba(0, 128, 128, 255)
                color:1,1,1,1
                height:50
            DefaultTextField:
                id:price
                text:root.price
                hint_text:"Price"
                hint_text_color_normal:"red"
                helper_text:"eg: 76,000 (without the currency sign)"
                helper_text_mode: "on_focus"
                background_color: app.theme_cls.bg_normal
                pos_hint:{"center_x":.5}
                cursor_color:rgba(0,0,59,255)
                font_size:"14sp"
                cursor_width:"2sp"
                multiline:True
            DefaultTextField:
                id:phone
                hint_text:"Phone Number"
                helper_text: "09056435678"
                hint_text_color_normal:"red"
                helper_text_mode: "on_focus"
                background_color: app.theme_cls.bg_normal
                pos_hint:{"center_x":.5}
                cursor_color:rgba(0,0,59,255)
                font_size:"14sp"
                cursor_width:"2sp"
                multiline:False
                on_text: root.on_phone()
            DefaultTextField:
                id:payment_duration
                text:root.payment_duration
                hint_text:"Payment Duration"
                hint_text_color_normal:"red"
                helper_text:"eg: per session, per year"
                helper_text_mode: "on_focus"
                background_color: app.theme_cls.bg_normal
                pos_hint:{"center_x":.5}
                cursor_color:rgba(0,0,59,255)
                font_size:"14sp"
                cursor_width:"2sp"
                multiline:True
            DefaultTextField:
                id:additional_fee
                text:root.additional_fee
                hint_text:"Addition Fee"
                helper_text:"eg: 1,000(without the currency sign)"
                helper_text_mode: "on_focus"
                background_color: app.theme_cls.bg_normal
                pos_hint:{"center_x":.5}
                cursor_color:rgba(0,0,59,255)
                font_size:"14sp"
                cursor_width:"2sp"
                multiline:True
            DefaultTextField:
                id:reason_for_fee
                text:root.reason_for_fee
                hint_text:"Reason for additional fee"
                helper_text:"Maintanance fee"
                helper_text_mode: "on_focus"
                background_color: app.theme_cls.bg_normal
                pos_hint:{"center_x":.5}
                cursor_color:rgba(0,0,59,255)
                font_size:"14sp"
                cursor_width:"2sp"
                multiline:True

            Spinner:
                id: category
                text: root.category
                values: root.categories
                size_hint_y:None
                background_color: rgba(0, 128, 128, 255)
                color:1,1,1,1
                height:50

            MDRectangleFlatIconButton:
                text:"ADD IMAGES"
                size_hint_x:1
                text_color: 1 , 1 , 1 , 1
                line_color: 1 , 1 , 1 , 1
                icon_color: 1 , 1 , 1 , 1
                on_release:
                    root.add_primary_image()
            MDLabel:
                text: 'Previous images will be deleted'
                size_hint: 1, None
                height: dp(10)
                halign:"center"
                color: rgba(0, 128, 128, 255)
                font_style:"Caption"
                color: 1 , 1 , 1 , 1

            MDBoxLayout:
                id:primary_image_box
                id:image_box
                size_hint:1, None
                height:'170dp'
                pos_hint: {'center_x': .5 }
                MDSmartTile:
                    id:primary_image
                    source:root.primary_image_path
                    mipmap:True
                    box_color: [0, 0, 0, 0] if self.source == "" else [0,0,0,.5] 
                    MDLabel:
                        text: "Primary image"
                        bold: True
                        color: [1, 1, 1, 1] if primary_image.source != "" else [0,0,0,0]
                        halign:"center"
               
            MDGridLayout:
                id:images_grid
                cols:2
                spacing: '30dp'
                size_hint: 1, None
                height:"350dp"
                pos_hint: {'center_x': .5 }
                padding: ('25dp', '10dp', '10dp', '10dp')
                MDBoxLayout:
                    size_hint: None, None
                    size:"150dp", "150dp"
                    id:image_1_box
                    MDSmartTile:
                        id:image_1
                        source:root.image_1
                        mipmap:True
                        box_color: [0, 0, 0, 0] if self.source == "" else [0,0,0,.5]
                        spacing: '10dp'
                        MDIconButton:
                            icon:"check"
                            theme_icon_color: "Custom"
                            icon_color: 0, 1, 0, 1
                            pos_hint: {"center_y": .5}
                            opacity: 1 if image_1.source != "" else 0
                            on_release: 
                                root.primary_image_path = image_1.source
                                
                        MDIconButton:
                            icon:"close"
                            theme_icon_color: "Custom"
                            icon_color: 1, 0, 0, 1
                            pos_hint: {"center_y": .5}
                            opacity: 1 if image_1.source != "" else 0
                            on_release: 
                                root.images_path.remove(root.image_1)
                                root.image_1 = ""
          

                MDBoxLayout:
                    size_hint: None, None
                    size:"150dp", "150dp"
                    MDSmartTile:
                        id:image_2
                        source:root.image_2
                        mipmap:True
                        box_color: [0, 0, 0, 0] if self.source == "" else [0,0,0,.5]

                        MDIconButton:
                            icon:"check"
                            theme_icon_color: "Custom"
                            icon_color: 0, 1, 0, 1
                            pos_hint: {"center_y": .5}
                            opacity: 1 if image_2.source != "" else 0
                            on_release: 
                                root.primary_image_path = image_2.source
                                
                        MDIconButton:
                            icon:"close"
                            theme_icon_color: "Custom"
                            icon_color: 1, 0, 0, 1
                            pos_hint: {"center_y": .5}
                            opacity: 1 if image_2.source != "" else 0
                            on_release: 
                                root.images_path.remove(root.image_2)
                                root.image_2 = ""

                    
                MDBoxLayout:
                    size_hint: None, None
                    size:"150dp", "150dp"
                    MDSmartTile:
                        id:image_3
                        source:root.image_3
                        mipmap:True
                        box_color: [0, 0, 0, 0] if self.source == "" else [0,0,0,.5]
                        MDIconButton:
                            icon:"check"
                            theme_icon_color: "Custom"
                            icon_color: 0, 1, 0, 1
                            pos_hint: {"center_y": .5}
                            opacity: 1 if image_3.source != "" else 0
                            on_release: 
                                root.primary_image_path = image_3.source
                                
                        MDIconButton:
                            icon:"close"
                            theme_icon_color: "Custom"
                            icon_color: 1, 0, 0, 1
                            pos_hint: {"center_y": .5}
                            opacity: 1 if image_3.source != "" else 0
                            on_release: 
                                root.images_path.remove(root.image_3)
                                root.image_3 = ""
                                

                MDBoxLayout:
                    size_hint: None, None
                    size:"150dp", "150dp"
                    MDSmartTile:
                        id:image_4
                        source:root.image_4
                        mipmap:True
                        box_color: [0, 0, 0, 0] if self.source == "" else [0,0,0,.5]
                        MDIconButton:
                            icon:"check"
                            theme_icon_color: "Custom"
                            icon_color: 0, 1, 0, 1
                            pos_hint: {"center_y": .5}
                            opacity: 1 if image_4.source != "" else 0
                            on_release: 
                                root.primary_image_path = image_4.source
                                
                        MDIconButton:
                            icon:"close"
                            theme_icon_color: "Custom"
                            icon_color: 1, 0, 0, 1
                            pos_hint: {"center_y": .5}
                            opacity: 1 if image_4.source != "" else 0
                            on_release: 
                                root.images_path.remove(root.image_4)
                                root.image_4 = ""
                    

            MDRectangleFlatIconButton:
                text:"ADD PROPERTY"
                icon:"database-plus-outline"
                size_hint_x:1
                text_color: 1 , 1 , 1 , 1
                line_color: 1 , 1 , 1 , 1
                icon_color: 1 , 1 , 1 , 1
                on_release: 
                    root.update()
            MDLabel:
                text:root.error_text
                color: 1 , 0 , 0 , .7
                size_hint:1, None
                height:dp(0) if self.text == "" else dp(60)
                halign:"center"
                padding: ('10dp', '10dp', '10dp', '10dp')
        

''')


class UpdateProperty(MDScreen, MDBoxLayout):
    name = "update_property"
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
    file_manager = ObjectProperty()
    primary_image_path = StringProperty()
    title = StringProperty()
    description = StringProperty()
    address = StringProperty()
    security_type = StringProperty()
    water_system = StringProperty()
    toilet_bathroom_description = StringProperty()
    kitchen_description = StringProperty()
    property_status = StringProperty()
    property_type = StringProperty()
    price = StringProperty()
    phone = StringProperty()

    payment_duration = StringProperty()
    additional_fee = StringProperty()
    reason_for_fee = StringProperty()
    images_path = []
    image_1 = StringProperty()
    image_2 = StringProperty()
    image_3 = StringProperty()
    image_4 = StringProperty()
    categories = ListProperty()
    categories_dict = DictProperty()
    error_text = StringProperty()
    category = StringProperty()

    def back(self):
        self.parent.current = "property_details"

    def on_phone(self):
        phone = self.ids.phone

        if len(phone.text) == 1:
            self.on_update_message(
                message="Phone number field will be disabled once it gets to exceeds the maximum. Plesae verify",
                background_color=(1, 0, 0, .7)
            )
        elif len(phone.text) > 10:
            phone.disabled = True

    def get_details(self):
        t = threading.Thread(target=self._get_details)
        t.start()

    def on_get_details(self, res):
        self.ids.title.text = res['title']
        self.ids.description.text = res['description']
        self.ids.address.text = res['address']
        self.ids.security_type.text = res['security_type']
        self.ids.water_system.text = res['water_system']
        self.ids.toilet_bathroom_description.text = res['toilet_bathroom_desc']
        self.ids.kitchen_description.text = res['kitchen_desc']
        self.ids.property_status.text = res['property_status']
        self.ids.property_type.text = res['property_type']
        self.ids.price.text = res['price']
        # self.ids.phone.text = res['agent_phone']
        self.ids.payment_duration.text = res['payment_duration']
        self.ids.additional_fee.text = res['additional_fee']
        self.ids.reason_for_fee.text = res['reason_for_fee']
        self.category = res['category']['title']
        # self.images_path.append(
        #     f"{self.image_base_url}/{res['primary_image_path']}")
        # self.primary_image_path = self.images_path[0]
        # self.image_1 = ""
        # self.image_2 = ""
        # self.image_3 = ""
        # self.image_4 = ""

        # print(self.images_path)

    def _get_details(self):
        try:
            response = requests.get(
                url=f"{self.base_url}/property/{self.id}",
                headers={
                    'Authorization': f'Bearer {self.access_token}'
                },
            )

            res = response.json()
            Clock.schedule_once(lambda x: self.on_get_details(res))
        except Exception as e:
            print(e)

    def exit_manager(self, *args):
        self.file_manager.close()

    def _on_select(self):
        self.primary_image_path = self.images_path[0]
        self.image_1 = self.images_path[1]
        self.image_2 = self.images_path[2]
        self.image_3 = self.images_path[3]
        self.image_4 = self.images_path[4]

    def select_path(self, path: str):
        try:
            self.images_path.append(path)
            self.exit_manager()
            self._on_select()
        except Exception as e:
            pass

    def add_primary_image(self):
        try:
            self.file_manager = MDFileManager(
                exit_manager=self.exit_manager,
                select_path=self.select_path,
                icon_selection_button="",
                background_color_selection_button=(0, 0, 0, 0),
                preview=True,
                ext=['.png', '.jpg', '.jpeg', '.gif'],
            )
            file_manager_path = ""
            if platform == 'android':
                from android.permissions import request_permissions, Permission
                from android.storage import primary_external_storage_path
                request_permissions(
                    [
                        Permission.READ_EXTERNAL_STORAGE,
                        Permission.WRITE_EXTERNAL_STORAGE
                    ]

                )

                file_manager_path = primary_external_storage_path()
            else:
                file_manager_path = os.path.expanduser("~")
            if len(self.images_path) >= 5:
                self.on_update_message(
                    message="Maximum images selected", background_color=(1, 0, 0, .7))
                return
            else:
                self.file_manager.show(file_manager_path)
        except:
            pass

    def update(self):
        t = threading.Thread(target=self._update)
        t.start()

    def on_update(self):
        Clock.schedule_once(lambda x: LoadingModal().close_modal())
        self.ids.title.text = ""
        self.ids.description.text = ""
        self.ids.address.text = ""
        self.ids.security_type.text = ""
        self.ids.water_system.text = ""
        self.ids.toilet_bathroom_description.text = ""
        self.ids.kitchen_description.text = ""
        self.ids.property_status.text = ""
        self.ids.price.text = ""
        self.ids.phone.text = ""
        self.ids.payment_duration.text = ""
        self.ids.additional_fee.text = ""
        self.ids.reason_for_fee.text = ""
        self.images_path.clear()
        self.primary_image_path = ""
        self.image_1 = ""
        self.image_2 = ""
        self.image_3 = ""
        self.image_4 = ""
        self.error_text = ""
        self.parent.current = "manage_property"

    def on_update_message(self, message, background_color):
        Clock.schedule_once(lambda x: LoadingModal().close_modal())
        toast(message, duration=5, background=background_color)

    def _update(self):
        try:
            Clock.schedule_once(lambda x: LoadingModal().open_modal())
            selected_category = self.categories_dict[self.ids.category.text]
            file = open(self.primary_image_path, "rb")

            images = []
            for item in self.images_path[1:]:
                new_item = open(item, "rb")
                images.append(new_item)

            data = {
                "title": self.ids.title.text,
                "description": self.ids.description.text,
                "address": self.ids.address.text,
                "security_type": self.ids.security_type.text,
                "water_system": self.ids.water_system.text,
                "toilet_bathroom_desc": self.ids.toilet_bathroom_description.text,
                "kitchen_desc": self.ids.kitchen_description.text,
                "property_status": self.ids.property_status.text,
                "property_type": self.ids.property_type.text,
                "price": self.ids.price.text,
                "agent_phone": self.ids.phone.text,
                "payment_duration": self.ids.payment_duration.text,
                "additional_fee": self.ids.additional_fee.text,
                "reason_for_fee": self.ids.reason_for_fee.text,
            }

            if data['title'] == "" or data['description'] == "" or data["address"] == "" or data["security_type"] == "" or data['water_system'] == "" or data['toilet_bathroom_desc'] == "" or data['price'] == "" or data['agent_phone'] == "" or data['payment_duration'] == "":

                Clock.schedule_once(lambda x: self.on_update_message(
                    message="Please check the required fields",
                    background_color=(1, 0, 0, .7)
                ))
                return

            else:
                response = requests.put(
                    url=f"{self.base_url}/property/{self.id}?category_id={selected_category}",

                    headers={
                        'Authorization': f'Bearer {self.access_token}',
                        'Content-Type': 'application/json',
                    },

                    json=data
                )

                res = response.json()

                if response.ok:

                    add_image = requests.put(
                        url=f"{self.base_url}/property/add-primary-image/{res['id']}",

                        headers={
                            'Authorization': f'Bearer {self.access_token}'
                        },
                        files={"file": file}
                    )

                    delete_images = requests.delete(
                        url=f"{self.base_url}/property/delete-images/all/{res['id']}",
                        headers={
                            'Authorization': f'Bearer {self.access_token}',
                        },
                    )

                    if add_image.ok:
                        Clock.schedule_once(lambda x: self.on_update())
                    for item in images:
                        add_images = requests.post(
                            url=f"{self.base_url}/property/add-images/{res['id']}",
                            headers={
                                'Authorization': f'Bearer {self.access_token}',
                            },
                            files={"file": item}
                        )

        except Exception as e:
            Clock.schedule_once(lambda x: LoadingModal().close_modal())
            self.error_text = "Ensure that a category is selected and at least one image is selected"

    def get_categories(self):
        try:
            response = requests.get(
                url=f"{self.base_url}/category",
                headers={
                    'Authorization': f'Bearer {self.access_token}'
                }
            )
            res = response.json()
            for item in res:
                self.categories.append(item['title'])
                self.categories_dict[item['title']] = item['id']

        except Exception as e:
            print(e)

    def on_enter(self):

        self.get_details()
        self.get_categories()

    def on_leave(self):
        phone = self.ids.phone
        phone.disabled = False
        self.error_text = ""
        self.categories.clear()
        self.images_path.clear()
