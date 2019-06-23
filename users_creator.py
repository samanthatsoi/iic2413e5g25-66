from faker import Faker
import random
import json
import os

fake = Faker("es_MX")
teams = ["Colo-Colo", "Universidad Catolica", "Universidad de Chile", "Cobreloa", "OHiggins", "Palestino"]

users = []

for i in range(5000):
    nombre = fake.name()
    ciudad = fake.city()
    email = fake.ascii_free_email()
    team = random.choice(teams)
    avenger = "Tony Stark"
    persona = {"uid": i, "city": ciudad, "email": email, "team": team, "avenger": avenger, "name": nombre}
    users.append(persona)

#Escribir JSON

cwd = os.getcwd()

with open(cwd + "/users.json", "w") as file:
    json.dump(users, file)
