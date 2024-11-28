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

class ReservationsScreen(Screen):
    pass

class MyRoot(ScreenManager):
    def __init__(self, **kwargs):
        super(MyRoot, self).__init__(**kwargs)
        self.add_widget(HotelScreen(name='hotel'))
        self.add_widget(HotelPhotosScreen(name='hotel_photos'))
        self.add_widget(ReservationsScreen(name='reservas'))

    def go_to_hotels(self):
        self.current = 'hotel_photos'

class MainApp(App):
    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)
        self.table_layout = None 

    def build(self):
        self.layout = BoxLayout(orientation='vertical') 
        Builder.load_file('templates/hotel.kv') 
        self.layout.add_widget(MyRoot()) 
        return self.layout  

    def load_reservations(self, email):
        url = f'http://127.0.0.1:5002/reservas/{email}'
        response = requests.get(url)
        if response.status_code == 200 and response.json() != []:
            reservas = response.json()
            self.show_reservations(reservas) 
        else:
            print("No se encontraron reservas para este correo.")
            return False

    def show_reservations(self, reservas):
        self.table_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        self.table_layout.bind(minimum_height=self.table_layout.setter('height'))

        headers = ['ID', 'Usuario', 'Hotel', 'Habitación', 'Fecha Inicial', 'Fecha Final', 'Estado', 'Cancelar']
        header_layout = BoxLayout(size_hint_y=None, height=40)
        for header in headers:
            header_layout.add_widget(Label(text=header, bold=True, size_hint_x=None, width=175))
        self.table_layout.add_widget(header_layout)

        for reserva in reservas:
            row_layout = BoxLayout(size_hint_y=None, height=40, spacing=25)
            row_layout.add_widget(Label(text=str(reserva['id']), size_hint_x=None, width=150))
            row_layout.add_widget(Label(text=str(reserva['usuario']), size_hint_x=None, width=150))
            row_layout.add_widget(Label(text=str(reserva['hotel']), size_hint_x=None, width=150))
            row_layout.add_widget(Label(text=str(reserva['habitacion']), size_hint_x=None, width=150))
            row_layout.add_widget(Label(text=self.format_date(reserva['fecha_inicial']), size_hint_x=None, width=150))
            row_layout.add_widget(Label(text=self.format_date(reserva['fecha_final']), size_hint_x=None, width=150))
            row_layout.add_widget(Label(text=str(reserva['estado']), size_hint_x=None, width=150))
            cancel_button = Button(text='Cancelar', size_hint_x=None, width=150)
            cancel_button.bind(on_press=lambda instance, r=reserva, row=row_layout: self.cancel_reservation(r, row)) 
            row_layout.add_widget(cancel_button)

            self.table_layout.add_widget(row_layout) 

        self.layout.add_widget(self.table_layout) 

    def cancel_reservation(self, reserva, row_layout):
        url = f'http://127.0.0.1:5002/hospedaje/{reserva["id"]}'
        response = requests.delete(url)
        if response.status_code == 200:
            print(f"Reserva con ID {reserva['id']} cancelada correctamente.")
            self.table_layout.remove_widget(row_layout) 
        else:
            print(f"Error al cancelar reserva con ID {reserva['id']}.")

    def format_date(self, date_str):
        from datetime import datetime
        date_obj = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %Z')
        return date_obj.strftime('%d %B %Y')

    def clear_reservation_table(self):
        self.layout.clear_widgets()
        self.layout.add_widget(MyRoot())  

if __name__ == '__main__':
    MainApp().run()
