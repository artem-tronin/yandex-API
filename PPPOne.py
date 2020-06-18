import os
import sys
import pygame
import requests

area = input()
marks = list(map(str, input().split()))
geocode_request_area = f'https://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&format=json&geocode={area}'
geocode_response_area = requests.get(geocode_request_area)

geocode_request_marks = [f'https://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&format=json&geocode=Москва {i}' for i in marks]
geocode_response_marks = [requests.get(j) for j in geocode_request_marks]


if not geocode_response_area:
    print('Ошибка выполнения geocode запроса')
    print(geocode_request_area)
    print("Http статус:", geocode_response_area.status_code, "(", geocode_response_area.reason, ")")
    for i in geocode_request_marks:
        print(i)
        print("Http статус:", i.status_code, "(", i.reason, ")")
    sys.exit(1)


json_response_area = geocode_response_area.json()
envelope = json_response_area['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['boundedBy']['Envelope']
lower_corner = envelope['lowerCorner'].replace(' ', ',')
upper_corner = envelope['upperCorner'].replace(' ', ',')

json_response_marks = [i.json() for i in geocode_response_marks]
marks_position = [i['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'] for i in json_response_marks]
for i in range(len(marks_position)):
    marks_position[i] = marks_position[i].replace(' ', ',')
    f = marks_position[i]
    marks_position[i] += ',round'
marks_position = '~'.join(marks_position)
print(marks_position)
map_request = f'https://static-maps.yandex.ru/1.x/?l=map&pt={marks_position}&bbox={lower_corner}~{upper_corner}'
map_response = requests.get(map_request)

if not map_response:
    print('Ошибка выполнения static запроса')
    print(map_request)
    print("Http статус:", map_response.status_code, "(", map_response.reason, ")")
    sys.exit(1)


map_file = 'map.png'
with open(map_file, 'wb') as file:
    file.write(map_response.content)

pygame.init()
screen = pygame.display.set_mode((600, 450))
screen.blit(pygame.image.load(map_file), (0,0))
pygame.display.flip()
while pygame.event.wait().type != pygame.QUIT:
    print(pygame.event.wait().type)
print(pygame.event.wait().type)

pygame.quit()

os.remove(map_file)
