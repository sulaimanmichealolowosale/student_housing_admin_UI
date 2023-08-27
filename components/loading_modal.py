from kivy.uix.modalview import ModalView
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.widget import Widget
from kivymd.uix.spinner import MDSpinner
from kivy.properties import ObjectProperty
from kivy.metrics import dp


class LoadingModal(Widget):
    image_modal = ModalView(auto_dismiss=True)

    def open_modal(self):
        # self.image_modal = ModalView(auto_dismiss=True)
        self.image_modal.background_color = (0, 0, 1, .3)
        # parent_box = MDBoxLayout(
        #     orientation="vertical",
        #     size_hint=(1, 1),
        #     spacing=20,
        #     padding=10,
        # )

        spinner = MDSpinner(
            active=True,
            size_hint=(None, None),
            height=dp(100),
            width=dp(100),
            pos_hint={'center_x': .5, 'senter_y': .5},
            # determinate= True
        )

        self.image_modal.add_widget(spinner)
        self.image_modal.open()

    def close_modal(self):
        self.image_modal.clear_widgets()
        self.image_modal.dismiss()
