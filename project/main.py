from kivy.lang import Builder
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.storage.jsonstore import JsonStore

store = JsonStore('user_data.json')

class LoginScreen(Screen):
    def login(self):
        username = self.ids.username_input.text.strip()
        if username:
            store.put('user', name=username)
            self.manager.current = 'homepage'

class HomePage(Screen):
    def on_pre_enter(self):
        user_data = store.get('user')
        username = user_data.get('name', 'User')
        self.ids.name_label.text = f"{username}"


class MyApp(App):
    def build(self):
        try:
            Builder.load_file('main.kv')
        except Exception as e:
            print(f"Error loading main.kv: {e}")
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(HomePage(name='homepage'))
        return sm

if __name__ == '__main__':
    MyApp().run()
