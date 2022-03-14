# Вход в контейнер
docker exec -it 1d3da06dcf1f bash 
# чтение файла
cat <filename>

gunicorn -w 4 -b 127.0.0.1:4000 myproject:app
