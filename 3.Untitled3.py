import requests

ip = requests.get("https://www.dmiseu.edu.zm").text
print("Public IP:", ip)
