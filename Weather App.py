from tkinter.constants import BOTTOM, TOP
import requests
import datetime
import tkinter as tk
import os

class WeatherGUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.key = os.environ['weather_app']
        self.create_widgets()

    def create_widgets(self):
        self.name = tk.Label(self,
            text = 'Provided by openweathermap.org'
            )
        self.name.pack(side=TOP)

        self.city_label = tk.Label(self,
            text='Enter city',)
        self.city_label.pack()

        self.city_entry = tk.Entry(self)
        self.city_entry.pack()

        self.enter_button = tk.Button(self,
            text='ENTER',
            command=self.set_location)
        self.enter_button.pack()

        self.weather_label = tk.Label(self,
            text='Current Weather')
        self.weather_label.pack()

        self.weather_text_box = tk.Text(self,
            height=10,
            width=50)
        self.weather_text_box.pack()

        self.quit = tk.Button(self,
            text='EXIT',
            command=self.master.destroy)
        self.quit.pack()
    
    def set_location(self):
        self.location = self.city_entry.get()
        self.city_entry.delete(0, tk.END)
        self.weather_text_box.insert("1.0", 'Retrieving weather data for {}...'.format(self.location))
        self.load_data()
        self.display()
    def display(self):
        for i, n in enumerate(self.weather_data):
            self.weather_text_box.insert(str(float(i+2)), "\n{:<17} {:<10}".format(n, self.weather_data[n]))
    def convert_to_c(self, k):
        return (round(k-273.15))
    def convert_to_f(self, k):
        return round((k-273.15) * 9/5 + 32)
    def convert_to_mph(self, m):
        return round(m*2.23694, 2)

    def load_data(self):
        self.complete_api_link = "https://api.openweathermap.org/data/2.5/weather?q=" + self.location + "&appid=" + self.key
        self.api_link = requests.get(self.complete_api_link)
        self.api_data = self.api_link.json()
        # self.api_data = {'coord': {'lon': -115.1372, 'lat': 36.175}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 313.65, 'feels_like': 310.13, 'temp_min': 310.84, 'temp_max': 317.14, 'pressure': 1013, 'humidity': 7}, 'visibility': 10000, 'wind': {'speed': 2.57, 'deg': 40}, 'clouds': {'all': 1}, 'dt': 1623865752, 'sys': {'type': 1, 'id': 6171, 
        #                 'country': 'US', 'sunrise': 1623846178, 
        #                 'sunset': 1623898786}, 'timezone': -25200, 'id': 5506956, 'name': 'Las Vegas', 'cod': 200}
        # print(self.api_data)
        if self.api_data['cod'] == '404':
            self.weather_text_box.insert('2.0', 'Invalid City: {}, Please check your city name.'.format(self.location))
        else:
            self.weather_data = {
                datetime.datetime.now().strftime('%A %I:%M%p') : "", 
                self.api_data['name'] : self.api_data['sys']['country'],
                "The skies are" : self.api_data['weather'][0]['main'],
                "Temperature" : self.convert_to_f(self.api_data['main']['temp']),
                "High" : self.convert_to_f(self.api_data['main']['temp_max']),
                "Low" : self.convert_to_f(self.api_data['main']['temp_min']),
                "Feels like" : self.convert_to_f(self.api_data['main']['feels_like']),
                "Humidity (%)" : self.api_data['main']['humidity'], #default value = %
                "Wind Speed (mph)" : self.convert_to_mph(self.api_data['wind']['speed']),
                "Direction" : self.api_data['wind']['deg'],
                "Sunrise" : datetime.datetime.fromtimestamp(self.api_data['sys']['sunrise']).strftime('%A %I:%M%p'),
                "Sunset" : datetime.datetime.fromtimestamp(self.api_data['sys']['sunset']).strftime('%A %I:%M%p')
                }
            if self.api_data['sys']['country'] != 'US':
                self.weather_data['Temperature'] = self.convert_to_c(self.api_data['main']['temp'])
                self.weather_data['High'] = self.convert_to_c(self.api_data['main']['temp_max'])
                self.weather_data['Low'] = self.convert_to_c(self.api_data['main']['temp_min'])
                self.weather_data['Feels like'] = self.convert_to_c(self.api_data['main']['feels_like'])
    def get_location(self):
        return self.location

root = tk.Tk()
root.title('Weather App')
app = WeatherGUI(master=root)
app.mainloop()

