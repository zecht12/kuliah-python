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
from kivy.uix.widget import Widget
import random
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.core.audio import SoundLoader

FONT_PATH = "assets/font/luckiestguy.ttf"
store = JsonStore('user_data.json')

def play_sound(sound_path):
    """Play a sound from the given path."""
    sound = SoundLoader.load(sound_path)
    if sound:
        sound.play()

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
            play_sound("assets/musik/masuk.mp3")
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
                play_sound("assets/musik/masuk.mp3")
                self.manager.current = 'homepage'
            else:
                print("Login failed: Invalid username or password.")
        else:
            print("No user registered. Please register first.")

class HomePage(Screen):
    background_music = None

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

    def create_popup(self, title, message, on_confirm, confirm_text="MULAI", cancel_text="BATAL"):
        """Helper to create a styled popup."""
        content = BoxLayout(orientation="vertical", spacing=dp(5), padding=(dp(20), dp(20), dp(20), dp(20)))

        label = Label(
            text=message,
            font_size=sp(18),
            halign="center",
            valign="middle",
            size_hint=(1, None),
            height=dp(100),
            color=(1, 1, 1, 1),
            font_name=FONT_PATH
        )
        label.bind(size=label.setter('text_size'))
        content.add_widget(label)

        button_layout = BoxLayout(
            orientation="horizontal",
            spacing=dp(20),
            size_hint=(1, None),
            height=dp(80),
        )

        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.8, 0.5),
            auto_dismiss=False,
            background="assets/Board_popup.png",
            separator_color=(0, 0, 0, 0),
            title_color=(1, 1, 1, 1),
            title_size=sp(24),
            title_align="center",
            title_font=FONT_PATH,
        )

        confirm_button = Button(
            text=confirm_text,
            size_hint=(1, None),
            height=dp(80),
            background_normal="assets/BUTTON.png",
            background_down="assets/BUTTON.png",
            color=(1, 1, 1, 1),
            font_name=FONT_PATH,
            on_release=lambda *args: (on_confirm(popup), popup.dismiss()),
        )
        button_layout.add_widget(confirm_button)

        if cancel_text:
            cancel_button = Button(
                text=cancel_text,
                size_hint=(1, None),
                height=dp(80),
                background_normal="assets/BUTTON.png",
                background_down="assets/BUTTON.png",
                color=(1, 1, 1, 1),
                font_name=FONT_PATH,
                on_release=popup.dismiss,
            )
            button_layout.add_widget(cancel_button)

        content.add_widget(button_layout)
        popup.open()

    def show_popup(self, title, message, on_confirm, confirm_text="MULAI", cancel_text="BATAL"):
        """Wrapper for creating and showing a popup."""
        self.create_popup(title, message, on_confirm, confirm_text, cancel_text)

    def start_level_1(self, popup):
        """Start Level 1 quiz."""
        popup.dismiss()
        self.manager.current = "quiz_penjumlahan"

    def on_pre_enter(self):
        if not self.background_music:
            self.background_music = SoundLoader.load("assets/musik/background.mp3")
            if self.background_music:
                self.background_music.loop = True
                self.background_music.volume = 0.5
                self.background_music.play()

        if store.exists('user'):
            user_data = store.get('user')
            username = user_data.get('name', 'User')
            total_score = user_data.get('total_score', 0)
            self.ids.name_label.text = f"{username}"
            self.ids.score_label.text = f"{total_score}"

    def start_quiz_pengurangan(self, popup):
        """Start Level 2 Pengurangan quiz."""
        popup.dismiss()
        self.manager.current = "quiz_pengurangan"

    def start_quiz_perkalian(self, popup):
        """Start Quiz Perkalian."""
        popup.dismiss()
        self.manager.current = "quiz_perkalian"

    def toggle_logout(self):
        """Show logout popup."""
        self.show_logout_popup()

    def show_level_popup(self):
        """Display popup for Level 1 Penjumlahan."""
        self.create_popup(
            title="Memulai Quiz",
            message="Apakah Anda ingin memulai\nLevel 1 Penjumlahan?",
            on_confirm=lambda popup: self.start_level_1(popup),
        )

    def show_quiz_pengurangan_popup(self):
        """Display popup for Level 2 Pengurangan."""
        self.create_popup(
            title="Memulai Quiz",
            message="Apakah Anda ingin memulai\nLevel 2 Pengurangan?",
            on_confirm=lambda popup: self.start_quiz_pengurangan(popup),
        )

    def show_quiz_perkalian_popup(self):
        """Display popup for Quiz Perkalian."""
        self.create_popup(
            title="Memulai Quiz",
            message="Apakah Anda ingin memulai\nQuiz Perkalian?",
            on_confirm=lambda popup: self.start_quiz_perkalian(popup),
        )

    def show_logout_popup(self):
        """Display a popup dialog for logging out."""
        self.create_popup(
            title="Keluar Dari Game",
            message="Anda yakin ingin keluar?",
            on_confirm=lambda popup: self.logout(),
            confirm_text="KELUAR",
            cancel_text="LANJUTKAN",
        )

    def logout(self, *args):
        """Handle user logout."""
        if store.exists('user'):
            user_data = store.get('user')
            user_data['logged_in'] = False
            store.put('user', **user_data)
            self.manager.current = 'login'

    def on_leave(self):
        if self.background_music:
            self.background_music.stop()
            self.background_music.unload()
            self.background_music = None

class QuizPenjumlahanScreen(Screen):
    current_score = 0
    current_question = 0
    total_questions = 20
    timer_sound = None
    win_sound = None
    lose_sound = None
    keluar_sound = None

    def on_pre_enter(self):
        """Inisialisasi sebelum masuk ke layar."""
        self.time_left = 10
        self.current_score = 0
        self.current_question = 0
        self.ids.progress_bar.value = 0
        self.update_timer_label()
        self.generate_question()
        self.load_sounds()
        Clock.schedule_interval(self.update_timer, 1)

    def on_leave(self):
        """Membersihkan sumber daya saat meninggalkan layar."""
        Clock.unschedule(self.update_timer)
        self.stop_and_unload_sounds()

    def load_sounds(self):
        """Memuat file suara yang digunakan."""
        if not self.timer_sound:
            self.timer_sound = SoundLoader.load("assets/musik/waktu.mp3")
            if self.timer_sound:
                self.timer_sound.loop = True
                self.timer_sound.volume = 0.5
                self.timer_sound.play()

        if not self.win_sound:
            self.win_sound = SoundLoader.load("assets/musik/menang.mp3")

        if not self.lose_sound:
            self.lose_sound = SoundLoader.load("assets/musik/kalah.mp3")

        if not self.keluar_sound:
            self.keluar_sound = SoundLoader.load("assets/musik/keluar.mp3")

    def stop_and_unload_sounds(self):
        """Menghentikan dan membuang suara yang dimuat."""
        if self.timer_sound:
            self.timer_sound.stop()
            self.timer_sound.unload()
            self.timer_sound = None
        if self.win_sound:
            self.win_sound.unload()
            self.win_sound = None
        if self.lose_sound:
            self.lose_sound.unload()
            self.lose_sound = None
        if self.keluar_sound:
            self.keluar_sound.unload()
            self.keluar_sound = None

    def play_keluar_sound(self):
        """Memainkan suara 'keluar'."""
        if self.keluar_sound:
            self.keluar_sound.play()

    def play_lose_sound(self):
        """Memainkan suara 'kalah'."""
        if self.lose_sound:
            self.lose_sound.play()

    def back_button_pressed(self):
        self.play_lose_sound()
        Clock.schedule_once(lambda dt: self.go_to_homepage(), 0.5)

    def update_timer(self, dt):
        """Memperbarui timer dan progress bar."""
        if self.time_left > 0:
            self.time_left -= 1
            self.update_timer_label()
            self.ids.progress_bar.value += (100 / 10)
        else:
            Clock.unschedule(self.update_timer)
            self.generate_question()

    def update_timer_label(self):
        """Memperbarui label timer di UI."""
        self.ids.timer_label.text = f"0:{self.time_left:02d}"

    def generate_question(self):
        """Menghasilkan pertanyaan matematika baru."""
        import random

        if self.current_question < self.total_questions:
            self.time_left = 10
            self.update_timer_label()
            self.ids.progress_bar.value = 0

            number1 = random.randint(1, 20)
            number2 = random.randint(1, 20)
            correct_answer = number1 + number2

            wrong_answers = set()
            while len(wrong_answers) < 3:
                wrong_answer = random.randint(1, 40)
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

    def check_answer(self, selected_answer):
        """Memeriksa jawaban yang dipilih oleh pengguna."""
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

    def update_score_label(self):
        """Memperbarui skor di UI."""
        self.ids.score_label.text = str(self.current_score)

    def update_score_in_store(self):
        """Memperbarui skor ke JSON store."""
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

    def update_status_level1(self):
        """Mengupdate status_level1 menjadi 'Sudah selesai' di JSON store."""
        if store.exists('user'):
            user_data = store.get('user')
            user_data['status_level1'] = "Sudah selesai"
            store.put('user', **user_data)

    def end_quiz(self):
        """Mengakhiri permainan."""
        Clock.unschedule(self.update_timer)
        if self.timer_sound:
            self.timer_sound.stop()

        if self.win_sound:
            self.win_sound.play()
        self.update_score_in_store()
        self.update_status_level1()

        self.show_popup(
            title="Total Score",
            message=f"Your score is: {self.current_score}",
            on_confirm=lambda popup: self.handle_keluar(popup),
            confirm_text="KELUAR",
            cancel_text=None,
        )

    def handle_keluar(self, popup):
        """Memainkan suara 'keluar' dan kembali ke homepage."""
        self.play_keluar_sound()
        Clock.schedule_once(lambda dt: self.go_to_homepage(), 0.5)

    def go_to_homepage(self):
        """Navigasi ke homepage."""
        self.manager.current = 'homepage'

    def show_popup(self, title, message, on_confirm, confirm_text="KELUAR", cancel_text="BATAL"):
        """Membuat dan menampilkan popup."""
        self.create_popup(title, message, on_confirm, confirm_text, cancel_text)

    def create_popup(self, title, message, on_confirm, confirm_text="MULAI", cancel_text="BATAL"):
        """Helper to create a styled popup."""
        content = BoxLayout(orientation="vertical", spacing=dp(5), padding=(dp(20), dp(20), dp(20), dp(20)))

        label = Label(
            text=message,
            font_size=sp(18),
            halign="center",
            valign="middle",
            size_hint=(1, None),
            height=dp(100),
            color=(1, 1, 1, 1),
            font_name=FONT_PATH
        )
        label.bind(size=label.setter('text_size'))
        content.add_widget(label)

        button_layout = BoxLayout(
            orientation="horizontal",
            spacing=dp(20),
            size_hint=(1, None),
            height=dp(80),
        )

        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.8, 0.5),
            auto_dismiss=False,
            background="assets/Board_popup.png",
            separator_color=(0, 0, 0, 0),
            title_color=(1, 1, 1, 1),
            title_size=sp(24),
            title_align="center",
            title_font=FONT_PATH,
        )

        confirm_button = Button(
            text=confirm_text,
            size_hint=(1, None),
            height=dp(80),
            background_normal="assets/BUTTON.png",
            background_down="assets/BUTTON.png",
            color=(1, 1, 1, 1),
            font_name=FONT_PATH,
            on_release=lambda *args: (on_confirm(popup), popup.dismiss()),
        )
        button_layout.add_widget(confirm_button)

        if cancel_text:
            cancel_button = Button(
                text=cancel_text,
                size_hint=(1, None),
                height=dp(80),
                background_normal="assets/BUTTON.png",
                background_down="assets/BUTTON.png",
                color=(1, 1, 1, 1),
                font_name=FONT_PATH,
                on_release=popup.dismiss,
            )
            button_layout.add_widget(cancel_button)

        content.add_widget(button_layout)
        popup.open()

class ImageButton(ButtonBehavior, Image):
    pass

class QuizPenguranganScreen(Screen):
    current_score = 0
    current_question = 0
    total_questions = 20
    timer_sound = None
    win_sound = None
    lose_sound = None
    keluar_sound = None

    def on_pre_enter(self):
        """Reset state and start the timer."""
        self.time_left = 10
        self.current_score = 0
        self.current_question = 0
        self.ids.progress_bar.value = 0
        self.update_timer_label()
        self.generate_question()

        if not self.timer_sound:
            self.timer_sound = SoundLoader.load("assets/musik/waktu.mp3")
            if self.timer_sound:
                self.timer_sound.loop = True
                self.timer_sound.volume = 0.5
                self.timer_sound.play()

        if not self.win_sound:
            self.win_sound = SoundLoader.load("assets/musik/menang.mp3")
        if not self.lose_sound:
            self.lose_sound = SoundLoader.load("assets/musik/kalah.mp3")
        if not self.keluar_sound:
            self.keluar_sound = SoundLoader.load("assets/musik/keluar.mp3")
            if not self.keluar_sound:
                print("Failed to load keluar sound!")

        Clock.schedule_interval(self.update_timer, 1)

    def play_keluar_sound(self):
        """Play the 'keluar' sound."""
        if self.keluar_sound:
            self.keluar_sound.play()
        else:
            print("Keluar sound not loaded!")

    def back_button_pressed(self):
        self.play_lose_sound()
        Clock.schedule_once(lambda dt: self.go_to_homepage(), 0.5)

    def play_lose_sound(self):
        """Play the 'lose' sound."""
        if self.lose_sound:
            self.lose_sound.play()
        else:
            print("Lose sound not loaded!")

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

    def show_popup(self, title, message, on_confirm, confirm_text="KELUAR", cancel_text="BATAL"):
        """Wrapper for creating and showing a popup."""
        self.create_popup(title, message, on_confirm, confirm_text, cancel_text)

    def create_popup(self, title, message, on_confirm, confirm_text="MULAI", cancel_text="BATAL"):
        """Helper to create a styled popup."""
        content = BoxLayout(orientation="vertical", spacing=dp(5), padding=(dp(20), dp(20), dp(20), dp(20)))

        label = Label(
            text=message,
            font_size=sp(18),
            halign="center",
            valign="middle",
            size_hint=(1, None),
            height=dp(100),
            color=(1, 1, 1, 1),
            font_name=FONT_PATH
        )
        label.bind(size=label.setter('text_size'))
        content.add_widget(label)

        button_layout = BoxLayout(
            orientation="horizontal",
            spacing=dp(20),
            size_hint=(1, None),
            height=dp(80),
        )

        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.8, 0.5),
            auto_dismiss=False,
            background="assets/Board_popup.png",
            separator_color=(0, 0, 0, 0),
            title_color=(1, 1, 1, 1),
            title_size=sp(24),
            title_align="center",
            title_font=FONT_PATH,
        )

        confirm_button = Button(
            text=confirm_text,
            size_hint=(1, None),
            height=dp(80),
            background_normal="assets/BUTTON.png",
            background_down="assets/BUTTON.png",
            color=(1, 1, 1, 1),
            font_name=FONT_PATH,
            on_release=lambda *args: (on_confirm(popup), popup.dismiss()),
        )
        button_layout.add_widget(confirm_button)

        if cancel_text:
            cancel_button = Button(
                text=cancel_text,
                size_hint=(1, None),
                height=dp(80),
                background_normal="assets/BUTTON.png",
                background_down="assets/BUTTON.png",
                color=(1, 1, 1, 1),
                font_name=FONT_PATH,
                on_release=popup.dismiss,
            )
            button_layout.add_widget(cancel_button)

        content.add_widget(button_layout)
        popup.open()

    def update_status_level2(self):
        """Update status_level2 to 'Sudah selesai' in JSON store."""
        if store.exists('user'):
            user_data = store.get('user')
            user_data['status_level2'] = "Sudah selesai"
            store.put('user', **user_data)

    def end_quiz(self):
        """Handle the end of the quiz."""
        Clock.unschedule(self.update_timer)
        if self.timer_sound:
            self.timer_sound.stop()

        if self.win_sound:
            self.win_sound.play()

        self.update_score_in_store()
        self.update_status_level2()

        self.show_popup(
            title="Total Score",
            message=f"Your score is: {self.current_score}",
            on_confirm=lambda popup: self.handle_keluar(popup),
            confirm_text="KELUAR",
            cancel_text=None,
        )

    def handle_keluar(self, popup):
        """Play 'keluar' sound and navigate to the homepage."""
        self.play_keluar_sound()
        Clock.schedule_once(lambda dt: self.go_to_homepage(), 0.5)

    def on_leave(self):
        """Clean up when leaving the screen."""
        Clock.unschedule(self.update_timer)
        if self.timer_sound:
            self.timer_sound.stop()
            self.timer_sound.unload()
            self.timer_sound = None

class QuizPerkalianScreen(Screen):
    current_score = 0
    current_question = 0
    total_questions = 20
    timer_sound = None
    win_sound = None
    lose_sound = None
    keluar_sound = None

    def on_pre_enter(self):
        """Reset state and start the timer."""
        self.time_left = 10
        self.current_score = 0
        self.current_question = 0
        self.ids.progress_bar.value = 0
        self.update_timer_label()
        self.generate_question()
        self.load_sounds()
        Clock.schedule_interval(self.update_timer, 1)

    def on_leave(self):
        """Clean up resources when leaving the screen."""
        Clock.unschedule(self.update_timer)
        self.stop_and_unload_sounds()

    def load_sounds(self):
        """Load sound files."""
        if not self.timer_sound:
            self.timer_sound = SoundLoader.load("assets/musik/waktu.mp3")
            if self.timer_sound:
                self.timer_sound.loop = True
                self.timer_sound.volume = 0.5
                self.timer_sound.play()

        if not self.win_sound:
            self.win_sound = SoundLoader.load("assets/musik/menang.mp3")

        if not self.lose_sound:
            self.lose_sound = SoundLoader.load("assets/musik/kalah.mp3")

        if not self.keluar_sound:
            self.keluar_sound = SoundLoader.load("assets/musik/keluar.mp3")

    def stop_and_unload_sounds(self):
        """Stop and unload sound resources."""
        if self.timer_sound:
            self.timer_sound.stop()
            self.timer_sound.unload()
            self.timer_sound = None
        if self.win_sound:
            self.win_sound.unload()
            self.win_sound = None
        if self.lose_sound:
            self.lose_sound.unload()
            self.lose_sound = None
        if self.keluar_sound:
            self.keluar_sound.unload()
            self.keluar_sound = None

    def play_keluar_sound(self):
        """Play the 'keluar' sound."""
        if self.keluar_sound:
            self.keluar_sound.play()

    def back_button_pressed(self):
        self.play_lose_sound()
        Clock.schedule_once(lambda dt: self.go_to_homepage(), 0.5)

    def play_lose_sound(self):
        """Play the 'lose' sound."""
        if self.lose_sound:
            self.lose_sound.play()

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
        """Generate a new multiplication question."""
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
            else:
                self.play_lose_sound()
            self.generate_question()
        except Exception as e:
            print(f"Error while evaluating the answer: {e}")

    def update_score_label(self):
        """Update the score label in the UI."""
        self.ids.score_label.text = str(self.current_score)

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

    def update_status_level3(self):
        """Update status_level3 to 'Sudah selesai' in JSON store."""
        if store.exists('user'):
            user_data = store.get('user')
            user_data['status_level3'] = "Sudah selesai"
            store.put('user', **user_data)

    def end_quiz(self):
        """Handle the end of the quiz."""
        Clock.unschedule(self.update_timer)
        if self.timer_sound:
            self.timer_sound.stop()

        if self.win_sound:
            self.win_sound.play()

        self.update_score_in_store()
        self.update_status_level3()

        self.show_popup(
            title="Total Score",
            message=f"Your score is: {self.current_score}",
            on_confirm=lambda popup: self.handle_keluar(popup),
            confirm_text="KELUAR",
            cancel_text=None,
        )

    def show_popup(self, title, message, on_confirm, confirm_text="MULAI", cancel_text="BATAL"):
        """Wrapper for creating and showing a popup."""
        self.create_popup(title, message, on_confirm, confirm_text, cancel_text)

    def create_popup(self, title, message, on_confirm, confirm_text="MULAI", cancel_text="BATAL"):
        """Helper to create a styled popup."""
        content = BoxLayout(orientation="vertical", spacing=dp(5), padding=(dp(20), dp(20), dp(20), dp(20)))

        label = Label(
            text=message,
            font_size=sp(18),
            halign="center",
            valign="middle",
            size_hint=(1, None),
            height=dp(100),
            color=(1, 1, 1, 1),
            font_name=FONT_PATH
        )
        label.bind(size=label.setter('text_size'))
        content.add_widget(label)

        button_layout = BoxLayout(
            orientation="horizontal",
            spacing=dp(20),
            size_hint=(1, None),
            height=dp(80),
        )

        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.8, 0.5),
            auto_dismiss=False,
            background="assets/Board_popup.png",
            separator_color=(0, 0, 0, 0),
            title_color=(1, 1, 1, 1),
            title_size=sp(24),
            title_align="center",
            title_font=FONT_PATH,
        )

        confirm_button = Button(
            text=confirm_text,
            size_hint=(1, None),
            height=dp(80),
            background_normal="assets/BUTTON.png",
            background_down="assets/BUTTON.png",
            color=(1, 1, 1, 1),
            font_name=FONT_PATH,
            on_release=lambda *args: (on_confirm(popup), popup.dismiss()),
        )
        button_layout.add_widget(confirm_button)

        if cancel_text:
            cancel_button = Button(
                text=cancel_text,
                size_hint=(1, None),
                height=dp(80),
                background_normal="assets/BUTTON.png",
                background_down="assets/BUTTON.png",
                color=(1, 1, 1, 1),
                font_name=FONT_PATH,
                on_release=popup.dismiss,
            )
            button_layout.add_widget(cancel_button)

        content.add_widget(button_layout)
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
