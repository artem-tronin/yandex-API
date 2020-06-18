import os
import sys
import pygame
import requests
import keyboard

area = input().split()
geocode_request = []
geocode_response = []
for i in area:
    geocode_request.append(
        f'https://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&format=json&geocode={i}')
    geocode_response.append(requests.get(geocode_request[-1]))

if not [i for i in geocode_response]:
    print('Ошибка выполнения geocode запроса')
    print(geocode_request)
    print("Http статус:", i.status_code, "(", i.reason, ")")
    sys.exit(1)
else:
    json_response = []
    envelope = []
    lower_corner = []
    upper_corner = []
    for i in geocode_response:
        json_response.append(i.json())
        envelope.append(
            json_response[-1]['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['boundedBy'][
                'Envelope'])
        lower_corner.append(envelope[-1]['lowerCorner'])
        upper_corner.append(envelope[-1]['upperCorner'])

        low1 = float(lower_corner[-1][:lower_corner[-1].index(' ')])
        low2 = float(lower_corner[-1][lower_corner[-1].index(' ')+1:])
        up1 = float(upper_corner[-1][:upper_corner[-1].index(' ')])
        up2 = float(upper_corner[-1][upper_corner[-1].index(' ')+1:])
        lower_corner[-1] = str(low1)+','+str(low2)
        upper_corner[-1] = str(up1)+','+str(up2)
        flag = False
        if low1>180:
            low1-=360
            flag = True
        elif low1<-180:
            low1+=360
            flag = True

        if low2>180:
            low2-=360
            flag = True
        elif low2<-180:
            low2+=360
            flag = True

        if up1 > 180:
            up1 -= 360
            flag = True
        elif up1 < -180:
            up1 += 360
            flag = True

        if up2 > 180:
            up2 -= 360
            flag = True
        elif up2 < -180:
            up2 += 360
            flag = True

        if flag:
            lower_corner[-1], upper_corner[-1] = upper_corner[-1], lower_corner[-1]

map_request = [f'https://static-maps.yandex.ru/1.x/?l=sat,skl&bbox={lower_corner[i]}~{upper_corner[i]}' for i in range(len(lower_corner))]
map_response = [requests.get(i) for i in map_request]

for i in map_request:
    if not i:
        print('Ошибка выполнения static запроса')
        print(i)
        print("Http статус:", i.status_code, "(", i.reason, ")")
        sys.exit(1)

map_files = [f'map{i}.png' for i in range(len(map_response))]
for i in range(len(map_files)):
    with open(map_files[i], 'wb') as file:
        file.write(map_response[i].content)

pygame.init()
screen = pygame.display.set_mode((600, 450))
screen.blit(pygame.image.load(map_files[0]), (0, 0))
pygame.display.flip()
i = 1
while True:
    if pygame.event.wait().type == pygame.QUIT:
        break

    for j in pygame.key.get_pressed():
        if j != 0:
            screen.blit(pygame.image.load(map_files[i]), (0, 0))
            pygame.display.flip()
            i += 1
            if i > len(map_files) - 1:
                i = 0

print(pygame.event.wait().type)

pygame.quit()
for i in range(len(map_files)):
    os.remove(map_files[i])
