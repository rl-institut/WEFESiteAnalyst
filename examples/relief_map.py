import requests
from pprint import pprint

# API KEY
API_key = "9cddbbca1be9c649a31f575746aa221f"

# This stores the url relief
base_url = "http://maps.openweathermap.org/maps/2.0/relief/"

# This will ask the user to enter coordinates
# city_id = input("Enter a city ID : ")
z = "1"
x = "90"
y = "8"

layer_name = "hello"
# This is final url. This is concatenation of base_url, API_key and city_id
Final_url = base_url +"{"+ z + "}/{" + x + "}/{" + y + "}appid=" + API_key

# this variable contains the JSON data which the API returns
reliefmap = requests.get(Final_url).json()

# JSON data is difficult to visualize, so you need to pretty print
pprint(reliefmap)


#http://maps.openweathermap.org/maps/2.0/relief/{z}/{x}/{y}?appid={API key}