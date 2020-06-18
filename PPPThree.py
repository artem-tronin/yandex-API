import os
import sys
import pygame
import requests

area = input()
geocode_request = f'https://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&format=json&geocode={area}'
geocode_response = requests.get(geocode_request)

if not geocode_response:
    print('Ошибка выполнения geocode запроса')
    print(geocode_request)
    print("Http статус:", geocode_response.status_code, "(", geocode_response.reason, ")")
    sys.exit(1)
else:
    json_response = geocode_response.json()
    envelope = json_response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['boundedBy']['Envelope']
    lower_corner = envelope['lowerCorner']
    upper_corner = envelope['upperCorner']
lower_corner = lower_corner.replace(' ', ',')
upper_corner = upper_corner.replace(' ', ',')

map_request = f'https://static-maps.yandex.ru/1.x/?l=map&bbox={lower_corner}~{upper_corner}'
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
