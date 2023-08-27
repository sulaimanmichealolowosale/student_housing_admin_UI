from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivymd.app import MDApp
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from components.login import LoginView
from components.dashboard import DashboardView


################## USER IMPORTS#########################

from components.sub_components.user.add_user import AddUser
from components.sub_components.user.user_details import UserDetails
from components.manage_user import ManageUser
from components.sub_components.user.update_user import UpdateUser

################## CATEGORY IMPORTS#########################

from components.manage_category import ManageCategory
from components.sub_components.category.category_details import CategoryDetails
from components.sub_components.category.add_category import AddCategory
from components.sub_components.category.update_category import UpdateCategory

################## PROPERTY IMPORTS#########################
from components.manage_property import ManageProperty
from components.sub_components.properties.add_property import AddProperty
from components.sub_components.properties.property_details import PropertyDetails
from components.sub_components.properties.update_property import UpdateProperty


from components.account import Account
from kivy.clock import Clock

from kivy.core.window import Window

Window.size = (400, 650)

BASE_URL = "http://192.168.0.100:8000/"
IMAGE_BASE_URL = "http://192.168.0.100:8000/"


KV = '''

<DrawerClickableItem@MDNavigationDrawerItem>
    focus_color: "#e7e4c0"
    text_color: "#4a4939"
    icon_color: "#4a4939"
    ripple_color: "#c5bdd2"
    selected_color: "#0c6c4d"
    

<Main>

    MDNavigationDrawerMenu:
        effect_cls: "ScrollEffect"

        # MDNavigationDrawerHeader:
        #     title: "ADMIN"
        #     title_color: "#4a4939"
        #     # text: "Main"
        #     spacing: "4dp"
        #     source: root.nav_image
        #     padding: "12dp", 0, 0, "56dp"
        
        DrawerClickableItem:
            icon: "view-dashboard"
            text: "Dashboard"
            on_press:
                root.nav_drawer.set_state("close")
                root.screen_manager.current = "dashboard"

        DrawerClickableItem:
            icon: "account-supervisor"
            text: "Manage Users"
            on_press:
                root.nav_drawer.set_state("close")
                root.screen_manager.current = "manage_user"

        DrawerClickableItem:
            icon: "playlist-check"
            text: "Manage Categories"
            on_press:
                root.nav_drawer.set_state("close")
                root.screen_manager.current = "manage_category"
        DrawerClickableItem:

            icon: "home-city"
            text: "Manage Properties"
            on_press:
                root.nav_drawer.set_state("close")
                root.screen_manager.current = "manage_property"
                
        MDNavigationDrawerDivider:

        DrawerClickableItem:
            icon: "account"
            text: "Account"
            on_press:
                root.nav_drawer.set_state("close")
                root.screen_manager.current = "account"

        DrawerClickableItem:
            icon: "logout"
            text: "Logout"
            on_press:
                root.nav_drawer.set_state("close")
                root.screen_manager.current = "login"

MDScreen:

    FitImage:
        id:profile_picture
        height: root.height
        allow_stretch:False  

        canvas.after:
            Color:
                rgba: 0, 0, 0, .5  
            Rectangle:
                pos: self.pos
                size: self.size

    MDTopAppBar:
        id:app_bar
        pos_hint: {"top": 1}
        elevation: 4
        left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]
       

    MDNavigationLayout:

        MDScreenManager:
            id: screen_manager

            LoginView:
                on_enter:nav_drawer.disabled = True
                on_pre_leave:nav_drawer.disabled = False

            DashboardView:

            ManageUser:

            Account:

            AddUser:

            UserDetails:

            UpdateUser:

            ManageCategory:

            AddCategory:

            CategoryDetails:

            UpdateCategory:

            ManageProperty:

            AddProperty:
            
            PropertyDetails:

            UpdateProperty:



        MDNavigationDrawer:
            id: nav_drawer
            radius: (0, 16, 16, 0)
            enable_swiping:True

            Main:
                id:main
                screen_manager: screen_manager
                nav_drawer: nav_drawer
               
'''


class Main(MDScrollView):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()
    nav_image = StringProperty("kivy.png")


class StudentHousing(MDApp):

    def build(self):
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.accent_palette = "Red"
        # self.theme_cls.theme_style = "Dark"
        return Builder.load_string(KV)


if __name__ == "__main__":
    try:
        StudentHousing().run()
    except Exception as e:
        print(e)
