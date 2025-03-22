from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.graphics import Color, Rectangle, Ellipse
from kivy.clock import Clock
import random
import pyttsx3  # Для голосового вывода (тест на ПК)

# Устанавливаем тёмную тему
Window.clearcolor = (0.05, 0.05, 0.1, 1)
Window.size = (400, 600)

class TempConverter(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Динамический фон
        with self.canvas.before:
            self.bg_color = Color(0.1, 0.2, 0.4, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)
            self.bind(pos=self.update_rect, size=self.update_rect)

        # Основной контейнер
        self.main_layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10), size_hint=(0.8, 0.6), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.add_widget(self.main_layout)

        # Стили
        label_style = {'color': (0.4, 0.8, 1, 1), 'font_size': dp(20), 'bold': True}
        input_style = {
            'background_normal': '', 'background_color': (0.15, 0.15, 0.25, 1),
            'foreground_color': (1, 1, 1, 1), 'font_size': dp(16), 'multiline': False,
            'halign': 'center', 'padding': [dp(8), dp(8), dp(8), dp(8)], 'border': (10, 10, 10, 10)
        }

        # Словарь для хранения TextInput
        self.inputs = {}

        # Поля ввода
        scales = [
            ('Кельвин (K)', 'kelvin'),
            ('Цельсий (°C)', 'celsius'),
            ('Фаренгейт (°F)', 'fahrenheit'),
            ('Реомюр (°Ré)', 'reaumur'),
            ('Ранкин (°R)', 'rankine')
        ]

        for label_text, scale in scales:
            self.main_layout.add_widget(Label(text=label_text, **label_style))
            input_field = TextInput(**input_style)
            input_field.bind(text=lambda instance, value, s=scale: self.update_temps(instance, s))
            self.inputs[scale] = input_field
            self.main_layout.add_widget(input_field)

        # Кнопка очистки
        clear_btn = Button(text='Очистить', size_hint=(1, 0.1), background_color=(0, 0.6, 1, 1), font_size=dp(16))
        clear_btn.bind(on_press=self.clear_fields)
        self.main_layout.add_widget(clear_btn)

        # Слайдер для температуры
        self.slider = Slider(min=0, max=500, value=273.15, size_hint=(1, 0.1), pos_hint={'center_x': 0.5, 'y': 0.65})
        self.slider.bind(value=self.on_slider_change)
        self.add_widget(self.slider)

        # Авторство справа
        self.author_label = Label(
            text='Автор: Куан Балабаев',
            color=(0, 0.8, 1, 1),
            font_size=dp(28),
            bold=True,
            size_hint=(None, None),
            size=(dp(250), dp(100)),
            pos_hint={'right': 0.95, 'top': 0.95}
        )
        self.add_widget(self.author_label)

        # Цитаты
        self.quotes = [
            "«Физика — это поэзия природы.» — Альберт Эйнштейн",
            "«Температура — это мера хаоса.» — Людвиг Больцман",
            "«Наука — это способ удивляться.» — Ричард Фейнман",
            "«Всё измеряется в Кельвинах.» — Уильям Томсон",
            "«Знание — это сила.» — Фрэнсис Бэкон",
            "«Природа говорит на языке математики.» — Галилео Галилей",
            "«Энергия — это жизнь Вселенной.» — Никола Тесла",
            "«Наука начинается с измерений.» — Майкл Фарадей",
            "«Холод и тепло — две стороны одной медали.» — Джеймс Максвелл",
            "«Физика объясняет, как движется мир.» — Исаак Ньютон",
            "«Температура — ключ к пониманию энергии.» — Неизвестный",
            "«Мир — это лаборатория физика.» — Роберт Милликен"
        ]
        self.quote_label = Label(
            text=random.choice(self.quotes),
            color=(0.6, 0.6, 0.8, 1),
            font_size=dp(14),
            italic=True,
            size_hint=(1, 0.1),
            pos_hint={'center_x': 0.5, 'y': 0.05}
        )
        self.add_widget(self.quote_label)
        Clock.schedule_interval(self.change_quote, 5)

        # 3D-термометр (имитация)
        with self.canvas:
            Color(1, 0, 0, 1)
            self.thermometer = Rectangle(pos=(dp(20), dp(100)), size=(dp(20), dp(100)))
        self.temp_level = 0

        # Голосовой движок (тест на ПК)
        self.engine = pyttsx3.init()
        self.voice_btn = Button(text='Голос', size_hint=(0.2, 0.1), pos_hint={'x': 0.05, 'y': 0.85}, background_color=(0, 0.8, 0.6, 1))
        self.voice_btn.bind(on_press=self.speak_temp)
        self.add_widget(self.voice_btn)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def update_temps(self, instance, scale, from_slider=False):
        try:
            value = float(instance.text) if instance.text else 0
            if scale == 'kelvin':
                k = value
            elif scale == 'celsius':
                k = value + 273.15
            elif scale == 'fahrenheit':
                k = (value - 32) * 5/9 + 273.15
            elif scale == 'reaumur':
                k = value * 5/4 + 273.15
            elif scale == 'rankine':
                k = value * 5/9

            self.inputs['kelvin'].text = f'{k:.2f}'
            self.inputs['celsius'].text = f'{(k - 273.15):.2f}'
            self.inputs['fahrenheit'].text = f'{(k - 273.15) * 9/5 + 32:.2f}'
            self.inputs['reaumur'].text = f'{(k - 273.15) * 4/5:.2f}'
            self.inputs['rankine'].text = f'{k * 9/5:.2f}'

            # Обновляем фон и термометр
            self.update_background(k)
            self.update_thermometer(k)
            if not from_slider:
                self.slider.value = k

        except ValueError:
            pass

    def on_slider_change(self, instance, value):
        self.update_temps(self.inputs['kelvin'], 'kelvin', from_slider=True)
        self.inputs['kelvin'].text = f'{value:.2f}'

    def clear_fields(self, instance):
        for input_field in self.inputs.values():
            input_field.text = ''
        self.slider.value = 273.15
        self.update_background(273.15)
        self.update_thermometer(0)

    def change_quote(self, dt):
        self.quote_label.text = random.choice(self.quotes)

    def update_background(self, kelvin):
        """Динамический фон в зависимости от температуры"""
        if kelvin < 273.15:  # Холод
            self.bg_color.rgba = (0.1, 0.2, 0.6, 1)  # Синий
        elif kelvin > 373.15:  # Жара
            self.bg_color.rgba = (0.6, 0.2, 0.1, 1)  # Красный
        else:  # Норма
            self.bg_color.rgba = (0.1, 0.2, 0.4, 1)  # Нейтральный

    def update_thermometer(self, kelvin):
        """Обновление термометра"""
        height = min(max((kelvin / 500) * dp(200), dp(10)), dp(200))  # Ограничение высоты
        self.thermometer.size = (dp(20), height)

    def speak_temp(self, instance):
        """Голосовое озвучивание температуры"""
        kelvin = float(self.inputs['kelvin'].text) if self.inputs['kelvin'].text else 0
        celsius = kelvin - 273.15
        self.engine.say(f"Температура: {kelvin:.1f} Кельвинов или {celsius:.1f} градусов Цельсия")
        self.engine.runAndWait()

class TempApp(App):
    def build(self):
        return TempConverter()

if __name__ == '__main__':
    TempApp().run()
