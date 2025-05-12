<!-- для активации работы django -->
django-admin startproject config .



<!-- Снести базу и восстановит ее -->
1. Удалить базу через SSMS
2. Создать БД: python manage.py ccdb
3 и 4. НА СВЯКИЙ СЛУЧАЙ: python manage.py makemigrations и python manage.py migrate      
5. Создать админа: python manage.py ccsu   
6. Загрузить в базу данных файлы из dogs.json: python manage.py loaddata dogs.json       