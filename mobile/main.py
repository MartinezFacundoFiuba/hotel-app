import kivy 
from kivy.app import App 
from kivy.uix.boxlayout import BoxLayout      
from kivy.uix.button import Button 
from kivy.uix.image import Image 
from kivy.uix.screenmanager import ScreenManager, Screen 
import requests  
from kivy.lang import Builder 
import json  
from kivy.uix.label import Label  
from kivy.uix.image import AsyncImage  
from kivy.graphics import Color, Rectangle

class HotelScreen(Screen):
    pass

class HotelPhotosScreen(Screen):
    def __init__(self, **kwargs):
        super(HotelPhotosScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)  
        self.add_widget(self.layout)
        self.load_hotels()

    def load_hotels(self):
        url = 'http://127.0.0.1:5002/hoteles'
        response = requests.get(url)
        if response.status_code == 200:
            hotels = json.loads(response.text)
            print(hotels)
            for hotel in hotels:
                self.add_hotel_info(hotel)

    def add_hotel_info(self, hotel):
        
        hotel_container = BoxLayout(orientation='horizontal', size_hint_y=None, height=200, padding=10) 
        hotel_container.canvas.before.clear()  
        with hotel_container.canvas.before:
            Color(0, 0, 0, 1)  
            Rectangle(pos=hotel_container.pos, size=hotel_container.size)  

        hotel_image = AsyncImage(source=f'assets/images/{hotel["id"]}.jpg', size_hint=(None, None), size=(200, 200)) 
        hotel_container.add_widget(hotel_image) 

        text_container = BoxLayout(orientation='vertical', size_hint=(None, None), size=(200, 200), padding=10)
        text_container.add_widget(Label(text=hotel['nombre'], color=(1, 1, 1, 1), font_size='20sp', bold=True))  
        text_container.add_widget(Label(text=hotel['ciudad'], color=(1, 1, 1, 1)))  
        text_container.add_widget(Label(text=hotel['provincia'], color=(1, 1, 1, 1)))  
        
        hotel_container.add_widget(text_container) 
        self.layout.add_widget(hotel_container)

class MyRoot(ScreenManager):
    def __init__(self, **kwargs):
        super(MyRoot, self).__init__(**kwargs)
        self.add_widget(HotelScreen(name='hotel'))
        self.add_widget(HotelPhotosScreen(name='hotel_photos'))

    def go_to_hotels(self):
        self.current = 'hotel_photos'

class MainApp(App):
    def build(self):
        Builder.load_file('templates/hotel.kv') 
        return MyRoot() 

if __name__ == '__main__':
    MainApp().run()
