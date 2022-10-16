people = [
    {"name":"harry", "house" : "Griffins"},
    {"name":"Cho", "house" : "Ravens"},
    {"name":"draco", "house" : "Slythreins"}
]

people.sort(key=lambda person:person["name"])

print(people)