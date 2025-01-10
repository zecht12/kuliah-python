from kivy.lang import Builder
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.storage.jsonstore import JsonStore
from datetime import datetime
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp, sp
from kivy.core.window import Window
import random
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior

store = JsonStore('user_data.json')

class RegisterScreen(Screen):
    def register(self):
        username = self.ids.username_input.text.strip()
        password = self.ids.password_input.text.strip()

        if username and password:
            created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            store.put('user', 
                        name=username, 
                        password=password, 
                        created_at=created_at, 
                        total_score=0, 
                        score_level1=0, 
                        score_level2=0, 
                        score_level3=0, 
                        status_level1="Belum Diselesaikan", 
                        status_level2="Belum Diselesaikan", 
                        status_level3="Belum Diselesaikan", 
                        logged_in=True)
            print("Registration successful!")
            self.manager.current = 'homepage'
        else:
            print("Username and password cannot be empty.")

class LoginScreen(Screen):
    def login(self):
        username = self.ids.username_input.text.strip()
        password = self.ids.password_input.text.strip()

        if store.exists('user'):
            user_data = store.get('user')
            stored_username = user_data.get('name')
            stored_password = user_data.get('password')

            if username == stored_username and password == stored_password:
                user_data['logged_in'] = True
                store.put('user', **user_data)
                print("Login successful!")
                self.manager.current = 'homepage'
            else:
                print("Login failed: Invalid username or password.")
        else:
            print("No user registered. Please register first.")

class HomePage(Screen):
    def on_touch_down(self, touch):
        target_box = self.ids.user_info_box
        level_1_box = self.ids.level_1_box
        level_2_box = self.ids.level_2_box
        level_3_box = self.ids.level_3_box
        if level_1_box.collide_point(*touch.pos):
            self.show_level_popup()
        elif level_2_box.collide_point(*touch.pos):
            self.show_quiz_pengurangan_popup()
        elif level_3_box.collide_point(*touch.pos):
            self.show_quiz_perkalian_popup()
        elif target_box.collide_point(*touch.pos):
            self.toggle_logout()
        return super().on_touch_down(touch)

    def show_level_popup(self):
        """Display popup for Level 1 Penjumlahan."""
        content = BoxLayout(orientation="vertical", spacing=dp(10), padding=dp(20))

        label = Label(
            text="Apakah Anda ingin memulai\nLevel 1 Penjumlahan?",
            font_size=sp(18),
            halign="center",
            valign="middle",
            size_hint=(1, None),
            height=dp(50),
            color=(0, 0, 0, 1),
        )
        content.add_widget(label)

        button_layout = BoxLayout(orientation="horizontal", spacing=dp(10))

        popup = Popup(
            title="Memulai Quiz",
            content=content,
            size_hint=(0.8, 0.4),
            auto_dismiss=False,
            background="",
            background_color=(1, 1, 1, 1),
            separator_color=(0.9, 0.9, 0.9, 1),
            title_color=(0, 0, 0, 1),
            title_size=sp(24),
            title_align="center",
        )

        mulai_button = Button(
            text="MULAI",
            size_hint=(1, None),
            height=dp(50),
            background_color=(0.09, 0.76, 0.57, 1),
            color=(1, 1, 1, 1),
            on_release=lambda *args: (self.start_level_1(popup), popup.dismiss()),
        )

        batal_button = Button(
            text="BATAL",
            size_hint=(1, None),
            height=dp(50),
            background_color=(1, 0.4, 0.4, 1),
            color=(1, 1, 1, 1),
            on_release=popup.dismiss,
        )

        button_layout.add_widget(mulai_button)
        button_layout.add_widget(batal_button)

        content.add_widget(button_layout)
        popup.open()

    def start_level_1(self, popup):
        """Start Level 1 quiz."""
        popup.dismiss()
        self.manager.current = "quiz_penjumlahan"

    def on_pre_enter(self):
        if store.exists('user'):
            user_data = store.get('user')
            username = user_data.get('name', 'User')
            total_score = user_data.get('total_score', 0)
            score_level1 = user_data.get('score_level1', 0)
            score_level2 = user_data.get('score_level2', 0)
            score_level3 = user_data.get('score_level3', 0)

            self.ids.name_label.text = f"{username}"
            self.ids.score_label.text = f"{total_score}"

            level_1_best_score_label = self.ids.level_1_box.children[0].children[0]
            level_2_best_score_label = self.ids.level_2_box.children[0].children[0]
            level_3_best_score_label = self.ids.level_3_box.children[0].children[0]

            level_1_best_score_label.text = f"My Bestscore : {score_level1}"
            level_2_best_score_label.text = f"My Bestscore : {score_level2}"
            level_3_best_score_label.text = f"My Bestscore : {score_level3}"


    def show_quiz_pengurangan_popup(self):
        """Display popup for Level 2 Pengurangan."""
        content = BoxLayout(orientation="vertical", spacing=dp(10), padding=dp(20))

        label = Label(
            text="Apakah Anda ingin memulai\nLevel 2 Pengurangan?",
            font_size=sp(18),
            halign="center",
            valign="middle",
            size_hint=(1, None),
            height=dp(50),
            color=(0, 0, 0, 1),
        )
        content.add_widget(label)

        button_layout = BoxLayout(orientation="horizontal", spacing=dp(10))

        popup = Popup(
            title="Memulai Quiz",
            content=content,
            size_hint=(0.8, 0.4),
            auto_dismiss=False,
            background="",
            background_color=(1, 1, 1, 1),
            separator_color=(0.9, 0.9, 0.9, 1),
            title_color=(0, 0, 0, 1),
            title_size=sp(24),
            title_align="center",
        )

        mulai_button = Button(
            text="MULAI",
            size_hint=(1, None),
            height=dp(50),
            background_color=(0.09, 0.76, 0.57, 1),
            color=(1, 1, 1, 1),
            on_release=lambda *args: (self.start_quiz_pengurangan(popup), popup.dismiss()),
        )

        batal_button = Button(
            text="BATAL",
            size_hint=(1, None),
            height=dp(50),
            background_color=(1, 0.4, 0.4, 1),
            color=(1, 1, 1, 1),
            on_release=popup.dismiss,
        )

        button_layout.add_widget(mulai_button)
        button_layout.add_widget(batal_button)

        content.add_widget(button_layout)
        popup.open()

    def start_quiz_pengurangan(self, popup):
        """Start Level 2 Pengurangan quiz."""
        popup.dismiss()
        self.manager.current = "quiz_pengurangan"

    def show_quiz_perkalian_popup(self):
        """Display popup for Quiz Perkalian."""
        content = BoxLayout(orientation="vertical", spacing=dp(10), padding=dp(20))

        label = Label(
            text="Apakah Anda ingin memulai\nQuiz Perkalian?",
            font_size=sp(18),
            halign="center",
            valign="middle",
            size_hint=(1, None),
            height=dp(50),
            color=(0, 0, 0, 1),
        )
        content.add_widget(label)

        button_layout = BoxLayout(orientation="horizontal", spacing=dp(10))

        popup = Popup(
            title="Memulai Quiz",
            content=content,
            size_hint=(0.8, 0.4),
            auto_dismiss=False,
            background="",
            background_color=(1, 1, 1, 1),
            separator_color=(0.9, 0.9, 0.9, 1),
            title_color=(0, 0, 0, 1),
            title_size=sp(24),
            title_align="center",
        )

        mulai_button = Button(
            text="MULAI",
            size_hint=(1, None),
            height=dp(50),
            background_color=(0.09, 0.76, 0.57, 1),
            color=(1, 1, 1, 1),
            on_release=lambda *args: (self.start_quiz_perkalian(popup), popup.dismiss()),
        )

        batal_button = Button(
            text="BATAL",
            size_hint=(1, None),
            height=dp(50),
            background_color=(1, 0.4, 0.4, 1),
            color=(1, 1, 1, 1),
            on_release=popup.dismiss,
        )

        button_layout.add_widget(mulai_button)
        button_layout.add_widget(batal_button)

        content.add_widget(button_layout)
        popup.open()

    def start_quiz_perkalian(self, popup):
        """Start Quiz Perkalian."""
        popup.dismiss()
        self.manager.current = "quiz_perkalian"

    def toggle_logout(self):
        """Show logout popup."""
        self.show_logout_popup()

    def show_logout_popup(self):
        """Display a popup dialog for logging out."""
        layout = BoxLayout(orientation="vertical", spacing=dp(10), padding=dp(20))
        layout.canvas.before.clear()
        label = Label(
            text="Anda yakin ingin keluar?",
            font_size=sp(18),
            halign="center",
            valign="middle",
            size_hint=(1, None),
            height=dp(50),
            color=(0, 0, 0, 1)
        )
        layout.add_widget(label)

        button_layout = BoxLayout(orientation="horizontal", spacing=dp(10))

        popup = Popup(
            title="Keluar Dari Game",
            content=layout,
            size_hint=(0.8, 0.4),
            auto_dismiss=False,
            background="",
            background_color=(1, 1, 1, 1),
            separator_color=(0.9, 0.9, 0.9, 1),
            title_color=(0, 0, 0, 1),
            title_size=sp(24),
            title_align="center",
        )

        keluar_button = Button(
            text="KELUAR",
            size_hint=(1, None),
            height=dp(50),
            background_color=(1, 0.4, 0.4, 1),
            color=(1, 1, 1, 1),
            on_release=lambda *args: (self.logout(), popup.dismiss()),
        )

        lanjutkan_button = Button(
            text="LANJUTKAN",
            size_hint=(1, None),
            height=dp(50),
            background_color=(0.09, 0.76, 0.57, 1),
            color=(1, 1, 1, 1),
            on_release=popup.dismiss,
        )

        button_layout.add_widget(lanjutkan_button)
        button_layout.add_widget(keluar_button)

        layout.add_widget(button_layout)
        popup.open()

    def logout(self, *args):
        """Handle user logout."""
        if store.exists('user'):
            user_data = store.get('user')
            user_data['logged_in'] = False
            store.put('user', **user_data)
            self.manager.current = 'login'

class QuizPenjumlahanScreen(Screen):
    current_score = 0
    current_question = 0
    total_questions = 20

    def on_pre_enter(self):
        """Reset state and start the timer."""
        self.time_left = 10
        self.current_score = 0
        self.current_question = 0
        self.ids.progress_bar.value = 0
        self.update_timer_label()
        Clock.schedule_interval(self.update_timer, 1)
        self.generate_question()

    def update_timer(self, dt):
        """Update the timer and progress bar."""
        if self.time_left > 0:
            self.time_left -= 1
            self.update_timer_label()
            self.ids.progress_bar.value += (100 / 10)
        else:
            Clock.unschedule(self.update_timer)
            self.generate_question()

    def update_timer_label(self):
        """Update the timer label."""
        self.ids.timer_label.text = f"0:{self.time_left:02d}"

    def generate_question(self):
        """Generate a new math question."""
        import random

        if self.current_question < self.total_questions:
            self.time_left = 10
            self.update_timer_label()
            self.ids.progress_bar.value = 0
            number1 = random.randint(1, 10)
            number2 = random.randint(1, 10)
            correct_answer = number1 + number2

            wrong_answers = set()
            while len(wrong_answers) < 3:
                wrong_answer = random.randint(1, 20)
                if wrong_answer != correct_answer:
                    wrong_answers.add(wrong_answer)

            options = list(wrong_answers) + [correct_answer]
            random.shuffle(options)

            self.ids.question_label.text = (
                f"[b]{number1} + {number2} = [color=#FF0000]?[/color][/b]"
            )
            self.ids.question_label.markup = True
            for i, option in enumerate(options):
                self.ids[f"option_{i+1}"].text = str(option)

            self.current_question += 1
            Clock.unschedule(self.update_timer)
            Clock.schedule_interval(self.update_timer, 1)
        else:
            self.end_quiz()

    def update_score_label(self):
        """Update the score label in the UI."""
        self.ids.score_label.text = str(self.current_score)

    def check_answer(self, selected_answer):
        """Check if the selected answer is correct."""
        question_text = self.ids.question_label.text
        clean_question = question_text.replace('[b]', '').replace('[/b]', '').replace('[color=#FF0000]', '').replace('[/color]', '').strip()
        math_expression = clean_question.split('=')[0].strip()

        try:
            correct_answer = eval(math_expression)
            if int(selected_answer) == correct_answer:
                self.current_score += 5
                self.update_score_label()
            self.generate_question()
        except Exception as e:
            print(f"Error while evaluating the answer: {e}")

    def update_score_in_store(self):
        """Update the score in the JSON store for Level 1."""
        if store.exists('user'):
            user_data = store.get('user')
            user_data['score_level1'] = max(
                user_data.get('score_level1', 0), self.current_score
            )
            user_data['total_score'] = (
                user_data.get('score_level1', 0) +
                user_data.get('score_level2', 0) +
                user_data.get('score_level3', 0)
            )
            store.put('user', **user_data)

    def go_to_homepage(self):
        """Navigate to the homepage."""
        self.manager.current = 'homepage'

    def end_quiz(self):
        """Handle the end of the quiz."""
        Clock.unschedule(self.update_timer)
        self.update_score_in_store()

        layout = BoxLayout(orientation="vertical", spacing=dp(10), padding=dp(20))

        score_label = Label(
            text=str(self.current_score),
            font_size=sp(32),
            color=(0, 0, 0, 1),
            size_hint=(1, None),
            height=dp(50),
            halign="center",
            valign="middle",
        )
        layout.add_widget(score_label)

        exit_button = Button(
            text="KELUAR",
            size_hint=(1, None),
            height=dp(50),
            background_color=(1, 0, 0, 1),
            color=(1, 1, 1, 1),
            on_release=lambda *args: (self.go_to_homepage(), popup.dismiss()),
        )
        layout.add_widget(exit_button)

        popup = Popup(
            title="Total Score",
            content=layout,
            size_hint=(0.8, 0.4),
            auto_dismiss=False,
            background="",
            background_color=(1, 1, 1, 1),
            title_color=(0, 0, 0, 1),
            title_size=sp(24),
            title_align="center",
        )
        popup.open()

class ImageButton(ButtonBehavior, Image):
    pass

class QuizPenguranganScreen(Screen):
    current_score = 0
    current_question = 0
    total_questions = 20

    def on_pre_enter(self):
        """Reset state and start the timer."""
        self.time_left = 10
        self.current_score = 0
        self.current_question = 0
        self.ids.progress_bar.value = 0
        self.update_timer_label()
        Clock.schedule_interval(self.update_timer, 1)
        self.generate_question()

    def update_timer(self, dt):
        """Update the timer and progress bar."""
        if self.time_left > 0:
            self.time_left -= 1
            self.update_timer_label()
            self.ids.progress_bar.value += (100 / 10)
        else:
            Clock.unschedule(self.update_timer)
            self.generate_question()

    def update_timer_label(self):
        """Update the timer label."""
        self.ids.timer_label.text = f"0:{self.time_left:02d}"

    def generate_question(self):
        """Generate a new math question."""
        if self.current_question < self.total_questions:
            self.time_left = 10
            self.update_timer_label()
            self.ids.progress_bar.value = 0
            number1 = random.randint(5, 20)
            number2 = random.randint(1, number1)
            correct_answer = number1 - number2

            wrong_answers = set()
            while len(wrong_answers) < 3:
                wrong_answer = random.randint(-10, 20)
                if wrong_answer != correct_answer:
                    wrong_answers.add(wrong_answer)

            options = list(wrong_answers) + [correct_answer]
            random.shuffle(options)

            self.ids.question_label.text = (
                f"[b]{number1} - {number2} = [color=#FF0000]?[/color][/b]"
            )
            self.ids.question_label.markup = True
            for i, option in enumerate(options):
                self.ids[f"option_{i+1}"].text = str(option)

            self.current_question += 1
            Clock.unschedule(self.update_timer)
            Clock.schedule_interval(self.update_timer, 1)
        else:
            self.end_quiz()

    def update_score_label(self):
        """Update the score label in the UI."""
        self.ids.score_label.text = str(self.current_score)

    def check_answer(self, selected_answer):
        """Check if the selected answer is correct."""
        question_text = self.ids.question_label.text
        clean_question = question_text.replace('[b]', '').replace('[/b]', '').replace('[color=#FF0000]', '').replace('[/color]', '').strip()
        math_expression = clean_question.split('=')[0].strip()

        try:
            correct_answer = eval(math_expression)
            if int(selected_answer) == correct_answer:
                self.current_score += 5
                self.update_score_label()
            self.generate_question()
        except Exception as e:
            print(f"Error while evaluating the answer: {e}")

    def update_score_in_store(self):
        """Update the score in the JSON store for Level 2."""
        if store.exists('user'):
            user_data = store.get('user')
            user_data['score_level2'] = max(
                user_data.get('score_level2', 0), self.current_score
            )
            user_data['total_score'] = (
                user_data.get('score_level1', 0) +
                user_data.get('score_level2', 0) +
                user_data.get('score_level3', 0)
            )
            store.put('user', **user_data)

    def go_to_homepage(self):
        """Navigate to the homepage."""
        self.manager.current = 'homepage'

    def end_quiz(self):
        """Handle the end of the quiz."""
        Clock.unschedule(self.update_timer)
        self.update_score_in_store()

        layout = BoxLayout(orientation="vertical", spacing=dp(10), padding=dp(20))

        score_label = Label(
            text=str(self.current_score),
            font_size=sp(32),
            color=(0, 0, 0, 1),
            size_hint=(1, None),
            height=dp(50),
            halign="center",
            valign="middle",
        )
        layout.add_widget(score_label)

        exit_button = Button(
            text="KELUAR",
            size_hint=(1, None),
            height=dp(50),
            background_color=(1, 0, 0, 1),
            color=(1, 1, 1, 1),
            on_release=lambda *args: (self.go_to_homepage(), popup.dismiss()),
        )
        layout.add_widget(exit_button)

        popup = Popup(
            title="Total Score",
            content=layout,
            size_hint=(0.8, 0.4),
            auto_dismiss=False,
            background="",
            background_color=(1, 1, 1, 1),
            title_color=(0, 0, 0, 1),
            title_size=sp(24),
            title_align="center",
        )
        popup.open()

class QuizPerkalianScreen(Screen):
    current_score = 0
    current_question = 0
    total_questions = 20

    def on_pre_enter(self):
        """Reset state and start the timer."""
        self.time_left = 10
        self.current_score = 0
        self.current_question = 0
        self.ids.progress_bar.value = 0
        self.update_timer_label()
        Clock.schedule_interval(self.update_timer, 1)
        self.generate_question()

    def update_timer(self, dt):
        """Update the timer and progress bar."""
        if self.time_left > 0:
            self.time_left -= 1
            self.update_timer_label()
            self.ids.progress_bar.value += (100 / 10)
        else:
            Clock.unschedule(self.update_timer)
            self.generate_question()

    def update_timer_label(self):
        """Update the timer label."""
        self.ids.timer_label.text = f"0:{self.time_left:02d}"

    def generate_question(self):
        """Generate a new math question."""
        if self.current_question < self.total_questions:
            self.time_left = 10
            self.update_timer_label()
            self.ids.progress_bar.value = 0
            number1 = random.randint(1, 12)
            number2 = random.randint(1, 12)
            correct_answer = number1 * number2

            wrong_answers = set()
            while len(wrong_answers) < 3:
                wrong_answer = random.randint(1, 144)
                if wrong_answer != correct_answer:
                    wrong_answers.add(wrong_answer)

            options = list(wrong_answers) + [correct_answer]
            random.shuffle(options)

            self.ids.question_label.text = (
                f"[b]{number1} \u00D7 {number2} = [color=#FF0000]?[/color][/b]"
            )
            self.ids.question_label.markup = True
            for i, option in enumerate(options):
                self.ids[f"option_{i+1}"].text = str(option)

            self.current_question += 1
            Clock.unschedule(self.update_timer)
            Clock.schedule_interval(self.update_timer, 1)
        else:
            self.end_quiz()

    def update_score_label(self):
        """Update the score label in the UI."""
        self.ids.score_label.text = str(self.current_score)

    def check_answer(self, selected_answer):
        """Check if the selected answer is correct."""
        question_text = self.ids.question_label.text
        clean_question = question_text.replace('[b]', '').replace('[/b]', '').replace('[color=#FF0000]', '').replace('[/color]', '').strip()
        math_expression = clean_question.split('=')[0].strip()

        try:
            correct_answer = eval(math_expression.replace('\u00D7', '*'))
            if int(selected_answer) == correct_answer:
                self.current_score += 5
                self.update_score_label()
            self.generate_question()
        except Exception as e:
            print(f"Error while evaluating the answer: {e}")

    def update_score_in_store(self):
        """Update the score in the JSON store for Level 3."""
        if store.exists('user'):
            user_data = store.get('user')
            user_data['score_level3'] = max(
                user_data.get('score_level3', 0), self.current_score
            )
            user_data['total_score'] = (
                user_data.get('score_level1', 0) +
                user_data.get('score_level2', 0) +
                user_data.get('score_level3', 0)
            )
            store.put('user', **user_data)

    def go_to_homepage(self):
        """Navigate to the homepage."""
        self.manager.current = 'homepage'

    def end_quiz(self):
        """Handle the end of the quiz."""
        Clock.unschedule(self.update_timer)
        self.update_score_in_store()

        layout = BoxLayout(orientation="vertical", spacing=dp(10), padding=dp(20))

        score_label = Label(
            text=str(self.current_score),
            font_size=sp(32),
            color=(0, 0, 0, 1),
            size_hint=(1, None),
            height=dp(50),
            halign="center",
            valign="middle",
        )
        layout.add_widget(score_label)

        exit_button = Button(
            text="KELUAR",
            size_hint=(1, None),
            height=dp(50),
            background_color=(1, 0, 0, 1),
            color=(1, 1, 1, 1),
            on_release=lambda *args: (self.go_to_homepage(), popup.dismiss()),
        )
        layout.add_widget(exit_button)

        popup = Popup(
            title="Total Score",
            content=layout,
            size_hint=(0.8, 0.4),
            auto_dismiss=False,
            background="",
            background_color=(1, 1, 1, 1),
            title_color=(0, 0, 0, 1),
            title_size=sp(24),
            title_align="center",
        )
        popup.open()

class MyApp(App):
    def build(self):
        Builder.load_file('main.kv')
        sm = ScreenManager()

        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(HomePage(name='homepage'))
        sm.add_widget(QuizPenjumlahanScreen(name='quiz_penjumlahan'))
        sm.add_widget(QuizPenguranganScreen(name='quiz_pengurangan'))
        sm.add_widget(QuizPerkalianScreen(name='quiz_perkalian'))

        if store.exists('user'):
            user_data = store.get('user')
            if user_data.get('logged_in', False):
                sm.current = 'homepage'
            else:
                sm.current = 'login'
        else:
            sm.current = 'register'

        return sm

if __name__ == '__main__':
    MyApp().run()
