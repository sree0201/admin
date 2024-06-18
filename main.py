from kivy.lang import Builder
from kivymd.uix.fitimage import FitImage
from pymongo import MongoClient
from urllib.parse import quote_plus
from kivy.core.window import Window
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp
from kivymd.theming import ThemeManager
from kivymd.uix.button import MDFlatButton
from kivymd.uix.card import MDCard, MDCardSwipe
from kivymd.uix.list import ThreeLineIconListItem, MDList, IconLeftWidget, TwoLineIconListItem
from kivymd.uix.navigationdrawer import MDNavigationDrawer, MDNavigationDrawerHeader
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.floatlayout import MDFloatLayout
from pymongo.server_api import ServerApi
from bson import ObjectId
KV = '''
screenman:
    Landing:
    Login:
    Home:
    Feedbacks:
    Manuser:
    Mandriver:
    Notification:
    Profile:

<DrawerClickableItem@MDNavigationDrawerItem>
    text_color: "#4a4939"
    icon_color: "#4a4939"
    ripple_color: "#43454a"
    selected_color: "#fffff"

<Landing>
    name:"landing"

    FitImage:
        source: app.get_image('car')
        pos_hint: {"y": .5,'x':.05}
        size_hint_y: .2
        size_hint_x: .9
    MDIconButton:
        size_hint:{.20, .1}
        icon:"login"
        pos_hint:{'center_x':.4, 'center_y':.1}
        on_release:
            app.root.current='login'
            app.root.transition.direction = 'up'
    MDLabel:
        text: "RidePool"
        font_style:'H4'
        color:(1,1,1,1)
        size_hint:{.5,.3}
        pos_hint:{'x':.3,'center_y':.9}
    MDLabel:
        text: "Continue"
        font_style:'H5'
        color:(1,1,1,1)
        pos_hint:{'x':.3,'center_y':.1}
<Login>:
    name:"login"

    FitImage:
        source: app.get_image('car')
        pos_hint:{'x':.0, 'y':.5}
        size_hint_y: .2
        size_hint_x: .9
    Label:
        text:"Login"
        font_size:50
        pos_hint:{'x':.0, 'y':.45}

    MDFloatLayout:
        radius: [25, 0, 0, 0]
        md_bg_color:(1,1,1,0.8)
        size_hint:(.8,.5)
        pos_hint: {"x": .1, "center_y": .56}
        radius: [25, 25, 25, 25]

        MDTextField:
            mode: "rectangle"
            hint_text:'Enter User ID'
            multiline: False
            id:userid
            required: True
            size_hint:{.65, .2}
            pos_hint:{'center_x':.4, 'center_y':.76}
            icon_left: "account"
            #on_text_validate:root.userid(self)

        MDTextField:
            mode: "rectangle"
            hint_text:'Enter Password'
            id:password
            required: True
            password: True
            multiline:False
            size_hint:{.65, .2}
            pos_hint:{'center_x':.4, 'center_y':.56}
            icon_left: "key-variant"
            #on_text_validate:root.password(self)
        MDIconButton:
            icon: "eye-off"
            pos_hint: {'center_x':.85, 'center_y': .56}
            on_release:
                self.icon = "eye" if self.icon == "eye-off" else "eye-off"
                password.password = False if password.password is True else True

        MDRaisedButton:
            text:"Login"
            size_hint:{.35, .05}
            pos_hint:{'center_x':.5, 'center_y':.3}
            on_press: root.logon(userid.text, password.text)
<Home>:
    name:'home'
    FitImage:
        source: app.get_image('admin_backg')
        allow_stretch: True
        keep_ratio: False
    MDFloatLayout:
        md_bg_color:(1,1,1,0.4)
        MDRelativeLayout:
            md_bg_color:(1,0,0,0.6)
            size_hint:(.4,.1)
            pos_hint:{"center_x":.25,"center_y":.7}
            radius: (26, 26, 26, 26)
            MDTextButton:
                text:"Manage User"
                pos_hint:{"x":.1,"y":.4}
                on_release:
                    app.root.current='manuser'
                    app.root.transition.direction = 'left'

        MDRelativeLayout:
            md_bg_color:(1,0,0,0.6)
            size_hint:(.4,.1)
            pos_hint:{"center_x":.7,"center_y":.7}
            radius: (26, 26, 26, 26)
            MDTextButton:
                text:"Manage Driver"
                pos_hint:{"x":.1,"y":.4}
                on_release:
                    app.root.current='mandriver'
                    app.root.transition.direction = 'right'
    MDTopAppBar:
        id: toolbar
        title: "Admin Home"
        left_action_items:[["menu", lambda x: nav_drawer.set_state("open")]]
        elevation: 4
        pos_hint: {'top': 1}

    MDNavigationDrawer:
        id:nav_drawer
        size_hint_x: .7
        md_bg_color: 1, 1, 1, 1
        radius: (0, 26, 26, 0)
        MDNavigationDrawerMenu:
            FitImage:
                source: app.get_image('login')
                size_hint_y: None
                height: dp(120)
            DrawerClickableItem:
                icon: "home"
                text: "Home"
                on_release:
                    app.root.current='home'
                    app.root.transition.direction = 'right'
                    nav_drawer.set_state("close")
            DrawerClickableItem:
                icon: "bell"
                text: 'Feedback'
                on_release:
                    app.root.current='feedback'
                    app.root.transition.direction = 'right'
                    nav_drawer.set_state("close")
            DrawerClickableItem:
                icon: "bell"
                text: 'Notification'
                on_release:
                    app.root.current='notification'
                    app.root.transition.direction = 'right'
                    nav_drawer.set_state("close")
            DrawerClickableItem:
                icon: "account"
                text: "Profile"
                on_release:
                    app.root.current='profile'
                    app.root.transition.direction = 'right'
                    nav_drawer.set_state("close")
            DrawerClickableItem:
                icon: "logout"
                text: "Logout"
                on_release:
                    app.root.current='login'
                    app.root.transition.direction = 'right'
                    nav_drawer.set_state("close")

<Feedbacks>:
    name:"feedback"
    FitImage:
        allow_stretch: True
        keep_ratio: False
        source: app.get_image('admin_backg')
    MDFloatLayout:
        md_bg_color:(1,1,1,0.8)
        size_hint:(1,.9)
        MDScrollView:
            MDList:
                id: container
                md_bg_color:(0,0,0,0.5)
    MDTopAppBar:
        id: toolbar
        left_action_items:[["menu", lambda x: nav_drawer.set_state("open")]]
        title: "Feedbacks"
        elevation: 4
        pos_hint: {'top': 1}
    MDNavigationDrawer:
        id:nav_drawer
        size_hint_x: .7
        md_bg_color: 1, 1, 1, .9
        radius: (0, 26, 26, 0)
        MDNavigationDrawerMenu:
            FitImage:
                size_hint_y: None
                height: dp(120)
                source: app.get_image('login')
            DrawerClickableItem:
                icon: "home"
                text: "Home"
                on_release:
                    app.root.current='home'
                    app.root.transition.direction = 'right'
                    nav_drawer.set_state("close")
            DrawerClickableItem:
                icon: "bell"
                text: 'Feedback'
                on_release:
                    app.root.current='feedback'
                    app.root.transition.direction = 'right'
                    nav_drawer.set_state("close")
            DrawerClickableItem:
                icon: "bell"
                text: 'Notification'
                on_release:
                    app.root.current='notification'
                    app.root.transition.direction = 'right'
                    nav_drawer.set_state("close")
            DrawerClickableItem:
                icon: "account"
                text: "Profile"
                on_release:
                    app.root.current='profile'
                    app.root.transition.direction = 'right'
                    nav_drawer.set_state("close")
            DrawerClickableItem:
                icon: "logout"
                text: "Logout"
                on_release:
                    app.root.current='login'
                    app.root.transition.direction = 'right'
                    nav_drawer.set_state("close")
<Manuser>:
    name:"manuser"
    FitImage:
        allow_stretch: True
        keep_ratio: False
        source: app.get_image('admin_backg')
    MDFloatLayout:
        md_bg_color:(1,1,1,0.8)
        size_hint:(1,.9)
        MDScrollView:
            MDList:
                id: mdlist
                md_bg_color:(0,0,0,0.5)
    MDTopAppBar:
        id: toolbar
        left_action_items:[["menu", lambda x: nav_drawer.set_state("open")]]
        title: "Manage User"
        elevation: 4
        pos_hint: {'top': 1}
    MDNavigationDrawer:
        id:nav_drawer
        size_hint_x: .7
        md_bg_color: 1, 1, 1, .9
        radius: (0, 26, 26, 0)
        MDNavigationDrawerMenu:
            FitImage:
                source: app.get_image('login')
                size_hint_y: None
                height: dp(120)
            DrawerClickableItem:
                icon: "home"
                text: "Home"
                on_release:
                    app.root.current='home'
                    app.root.transition.direction = 'right'
                    nav_drawer.set_state("close")
            DrawerClickableItem:
                icon: "bell"
                text: 'Feedback'
                on_release:
                    app.root.current='feedback'
                    app.root.transition.direction = 'right'
                    nav_drawer.set_state("close")
            DrawerClickableItem:
                icon: "bell"
                text: 'Notification'
                on_release:
                    app.root.current='notification'
                    app.root.transition.direction = 'right'
                    nav_drawer.set_state("close")
            DrawerClickableItem:
                icon: "account"
                text: "Profile"
                on_release:
                    app.root.current='profile'
                    app.root.transition.direction = 'right'
                    nav_drawer.set_state("close")
            DrawerClickableItem:
                icon: "logout"
                text: "Logout"
                on_release:
                    app.root.current='login'
                    app.root.transition.direction = 'right'
                    nav_drawer.set_state("close")
<Mandriver>:
    name:"mandriver"
    FitImage:
        allow_stretch: True
        keep_ratio: False
        source: app.get_image('admin_backg')
    MDFloatLayout:
        md_bg_color:(1,1,1,0.8)
        size_hint:(1,.9)
        MDScrollView:
            MDList:
                id: mdlistdriver
                md_bg_color:(0,0,0,0.5)
    MDTopAppBar:
        id: toolbar
        left_action_items:[["menu", lambda x: nav_drawer.set_state("open")]]
        title: "Manage Driver"
        elevation: 4
        pos_hint: {'top': 1}
    MDNavigationDrawer:
        id:nav_drawer
        size_hint_x: .7
        md_bg_color: 1, 1, 1, 1
        radius: (0, 26, 26, 0)
        MDNavigationDrawerMenu:
            FitImage:
                source: app.get_image('login')
                size_hint_y: None
                height: dp(120)
            DrawerClickableItem:
                icon: "home"
                text: "Home"
                on_release:
                    app.root.current='home'
                    app.root.transition.direction = 'right'
                    nav_drawer.set_state("close")
            DrawerClickableItem:
                icon: "bell"
                text: 'Feedback'
                on_release:
                    app.root.current='feedback'
                    app.root.transition.direction = 'right'
                    nav_drawer.set_state("close")
            DrawerClickableItem:
                icon: "bell"
                text: 'Notification'
                on_release:
                    app.root.current='notification'
                    app.root.transition.direction = 'right'
                    nav_drawer.set_state("close")
            DrawerClickableItem:
                icon: "account"
                text: "Profile"
                on_release:
                    app.root.current='profile'
                    app.root.transition.direction = 'right'
                    nav_drawer.set_state("close")
            DrawerClickableItem:
                icon: "logout"
                text: "Logout"
                on_release:
                    app.root.current='login'
                    app.root.transition.direction = 'right'
                    nav_drawer.set_state("close")

<Notification>:
    name:"notification"
    FitImage:
        source: app.get_image('admin_backg')
        allow_stretch: True
        keep_ratio: False
    MDFloatLayout:
        md_bg_color:(1,1,1,0.8)
        size_hint:(1,.9)
        MDScrollView:
            MDList:
                id: notify
                md_bg_color:(0,0,0,0.5)
    MDTopAppBar:
        id: toolbar
        left_action_items:[["menu", lambda x: nav_drawer.set_state("open")]]
        title: "Notifications"
        elevation: 4
        pos_hint: {'top': 1}
    MDNavigationDrawer:
        id:nav_drawer
        size_hint_x: .7
        md_bg_color: 1, 1, 1, .9
        radius: (0, 26, 26, 0)
        MDNavigationDrawerMenu:
            FitImage:
                source: app.get_image('login')
                size_hint_y: None
                height: dp(120)
            DrawerClickableItem:
                icon: "home"
                text: "Home"
                on_release:
                    app.root.current='home'
                    app.root.transition.direction = 'right'
                    nav_drawer.set_state("close")
            DrawerClickableItem:
                icon: "bell"
                text: 'Feedback'
                on_release:
                    app.root.current='feedback'
                    app.root.transition.direction = 'right'
                    nav_drawer.set_state("close")
            DrawerClickableItem:
                icon: "bell"
                text: 'Notification'
                on_release:
                    app.root.current='notification'
                    app.root.transition.direction = 'right'
                    nav_drawer.set_state("close")
            DrawerClickableItem:
                icon: "account"
                text: "Profile"
                on_release:
                    app.root.current='profile'
                    app.root.transition.direction = 'right'
                    nav_drawer.set_state("close")
            DrawerClickableItem:
                icon: "logout"
                text: "Logout"
                on_release:
                    app.root.current='login'
                    app.root.transition.direction = 'right'
                    nav_drawer.set_state("close")

<Profile>:
    name:"profile"
    FitImage:
        source: app.get_image('admin_backg')
        allow_stretch: True
        keep_ratio: False
    MDFloatLayout:
        md_bg_color:(1,1,1,0.8)
        size_hint:(1,.9)

    MDTopAppBar:
        id: toolbar
        left_action_items:[["menu", lambda x: nav_drawer.set_state("open")]]
        title: "Profile"
        elevation: 4
        pos_hint: {'top': 1}

    FitImage:
        size_hint:{.25, .1}
        pos_hint:{'x':.4,'y':.65}
        source: app.get_image('account')
    MDRelativeLayout:
        id: my_layout
        MDLabel:
            text: "Name: "
            font_style:'H6'
            size_hint:{.5,.3}
            pos_hint:{'x':.3,'center_y':.45}
        MDLabel:
            text: root.my_name
            size_hint:{.5,.3}
            font_style:'H6'
            pos_hint:{'x':.5,'center_y':.45}
        MDLabel:
            text: "Role: "
            font_style:'H6'
            size_hint:{.5,.3}
            pos_hint:{'x':.3,'center_y':.35}
        MDLabel:
            id:"mob"
            text:root.my_role
            size_hint:{.5,.3}
            font_style:'H6'
            pos_hint:{'x':.45,'center_y':.35}
        MDLabel:
            id:"name"
            text: "Mob: "
            font_style:'H6'
            size_hint:{.5,.3}
            pos_hint:{'x':.3,'center_y':.25}
        MDLabel:
            text:root.my_mob
            size_hint:{.5,.3}
            font_style:'H6'
            pos_hint:{'x':.45,'center_y':.25}
    MDNavigationDrawer:
        id:nav_drawer
        size_hint_x: .7
        md_bg_color: 1, 1, 1, .9
        radius: (0, 26, 26, 0)
        MDNavigationDrawerMenu:
            FitImage:
                source: app.get_image('login')
                size_hint_y: None
                height: dp(120)
            DrawerClickableItem:
                icon: "home"
                text: "Home"
                on_release:
                    app.root.current='home'
                    app.root.transition.direction = 'right'
                    nav_drawer.set_state("close")
            DrawerClickableItem:
                icon: "bell"
                text: 'Feedback'
                on_release:
                    app.root.current='feedback'
                    app.root.transition.direction = 'right'
                    nav_drawer.set_state("close")
            DrawerClickableItem:
                icon: "bell"
                text: 'Notification'
                on_release:
                    app.root.current='notification'
                    app.root.transition.direction = 'right'
                    nav_drawer.set_state("close")
            DrawerClickableItem:
                icon: "account"
                text: "Profile"
                on_release:
                    app.root.current='Profile'
                    app.root.transition.direction = 'right'
                    nav_drawer.set_state("close")
            DrawerClickableItem:
                icon: "logout"
                text: "Logout"
                on_release:
                    app.root.current='login'
                    app.root.transition.direction = 'right'
                    nav_drawer.set_state("close")
'''
username = 'Sree'
password = 'Sree@123'
hostname = 'ridepool.iyf4x9n.mongodb.net'
database = 'RidePool'

escaped_username = quote_plus(username)
escaped_password = quote_plus(password)

uri = (f"mongodb+srv://{escaped_username}:{escaped_password}@{hostname}/{database}?retryWrites=true&w=majority&appName"
       f"=RidePool")

my_client = MongoClient(uri, server_api=ServerApi('1'))
mydb = my_client["RidePool"]
auth = mydb["Admin_auth"]
feed = mydb["feedback"]
user = mydb["Auth"]
images = mydb["images"]
Window.size = (300, 600)


# auth.insert_one({'user': 'sree'})


def show_message(message):
    Snackbar(text=message).open()


class Landing(Screen):
    pass


class Login(Screen):
    def logon(self, username, password):
        if auth.find_one({'username': username, 'password': password}):
            show_message('Successfull')
            app = MDApp.get_running_app()
            app.root.current = 'home'
        else:
            show_message('Invalid username or password')


class Home(Screen):
    pass


class Manuser(Screen):

    def on_pre_enter(self, *args):
        # self.listd1 = MDList()
        # user1 = {"role": 'User'}
        # for i in user.find(user1):
        #     id1 = str(i.get('_id', ''))
        #     self.listd1.add_widget(TwoLineIconListItem(
        #         IconLeftWidget(
        #             icon="delete"
        #         ),
        #         text="User: " + i.get('username', ''),
        #         secondary_text="User_id: " + str(i.get('_id', ''))
        #     ))
        #
        # self.ids.mdlist.add_widget(self.listd1)
        self.listd1 = MDList()
        user1 = {"role": 'User'}
        for i in user.find(user1):
            id1 = str(i.get('_id', ''))
            icon = IconLeftWidget(icon="delete")
            icon.bind(on_release=lambda widget, user_id=id1: self.delete_user(user_id))
            self.listd1.add_widget(TwoLineIconListItem(
                text="User: " + i.get('username', ''),
                secondary_text="User_id: " + id1,
                _no_ripple_effect=True  # Optional: Disable ripple effect on the list item
            ))
            self.listd1.children[0].add_widget(icon)  # Adding the IconLeftWidget to the TwoLineIconListItem

        self.ids.mdlist.add_widget(self.listd1)

    def delete_user(self, user_id):
        user.delete_one({'_id': ObjectId(user_id)})

    def on_leave(self, *args):
        self.ids.mdlist.remove_widget(self.listd1)


class Mandriver(Screen):

    def on_pre_enter(self, *args):
        self.listd2 = MDList()
        user1 = {"role": 'Driver'}
        for i in user.find(user1):
            id2 = str(i.get('_id', ''))
            icon = IconLeftWidget(icon="delete")
            icon.bind(on_release=lambda widget, driver_id=id2: self.delete_Driver(driver_id))
            self.listd2.add_widget(TwoLineIconListItem(
                text="Driver: " + i.get('username', ''),
                secondary_text="Driver_id: " + id2,
                _no_ripple_effect=True  # Optional: Disable ripple effect on the list item
            ))
            self.listd2.children[0].add_widget(icon)  # Adding the IconLeftWidget to the TwoLineIconListItem

        self.ids.mdlistdriver.add_widget(self.listd2)

    def delete_Driver(self, driver_id):
        print(driver_id)
        user.delete_one({'_id': ObjectId(driver_id)})

    def on_leave(self, *args):
        self.ids.mdlistdriver.remove_widget(self.listd2)


class Feedbacks(Screen):
    def on_pre_enter(self, *args):
        self.listd = MDList()
        for i in feed.find():
            self.listd.add_widget(ThreeLineIconListItem(
                text="Subject: " + i.get('heading', ''),
                secondary_text="Body: " + i.get('body', ''),
                tertiary_text="Ride_id: " + i.get('ride_id', ''),
            ))
        self.ids.container.add_widget(self.listd)

    def on_leave(self, *args):
        self.ids.container.remove_widget(self.listd)


class Notification(Screen):
    def on_pre_enter(self, *args):
        self.listd2 = MDList()
        for i in feed.find():
            self.listd2.add_widget(ThreeLineIconListItem(

                text="Subject: " + i.get('heading', ''),
                secondary_text="Body: " + i.get('body', ''),
                tertiary_text="Ride_id: " + i.get('ride_id', ''),
            ))
        self.ids.notify.add_widget(self.listd2)

    def on_leave(self, *args):
        self.ids.notify.remove_widget(self.listd2)


class Profile(Screen):
    my_name = StringProperty("")
    my_role = StringProperty("")
    my_mob = StringProperty("")

    def on_pre_enter(self):
        dis_data = auth.find_one()
        if dis_data:
            uname = dis_data.get('name', '')
            role = dis_data.get('Role', '')
            mob = dis_data.get('mob', '')
            self.my_name = uname
            self.my_role = role
            self.my_mob = mob


class screenman(ScreenManager):
    pass


class Admin(MDApp):
    def build(self):
        self.theme_cls = ThemeManager()
        self.theme_cls.theme_style = "Dark"
        return Builder.load_string(KV)

    def get_image(self, name):
        image_data = images.find_one({'filename': name})
        if image_data:
            with open(str(image_data['filename']) + '.jpg', 'wb') as file:
                file.write(image_data['data'])
            return str(image_data['filename']) + '.jpg'


if __name__ == "__main__":
    Admin().run()
