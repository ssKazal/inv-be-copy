# VaidInventoryBE

Instruction on how to set-up project

```
git clone https://github.com/VaidTech/VaidInventoryBE.git
```
```
pip install -r requirements
```
```
Create database;
```
```
Create a .env file in the same directory as src/ folder. with basic info from demo.env file.
```
```
python manage.py makemigrations inventory
```
```
python manage.py migrate
```
```
python manage.py create_groups_and_permissions.py
```
```
python manage.py runserver
```
