import os

images_path = 'ImagesAttendance'
index = 0
for filename in os.listdir(images_path):
    f = os.path.join(images_path, filename)
    lista = filename.split('.')
    if lista[1] == '2':
        new_name = 'User.1.' + lista[2] + '.png'
    else:
        new_name = 'User.2.' + lista[2] + '.png'
    os.rename('ImagesAttendance/' + filename, 'ImagesAttendance/' + new_name)



for filename in os.listdir(images_path):
    print(filename)
