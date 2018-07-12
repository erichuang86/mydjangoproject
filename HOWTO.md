## Setup python,Django in PyCharm Community
### install python3 and PyCharm
### pip install Django, version 2.0.7
### add django to System PATH,
C:\Users\eric_huang\AppData\Local\Programs\Python\Python36-32\Lib\site-packages\django\bin

### create django project and app
	a) cd D:\pycharm_project
	b) D:\pycharm_project>django-admin startproject mydjangoproject
	c) D:\pycharm_project\mydjangoproject\mydjangoproject>django-admin startapp mytest
	d) D:\pycharm_project\mydjangoproject>python manage.py migrate
\*Note: DO NOT use myapp as app name, otherwise report module not found error.\*

### create django project in Pycharm, 
	a)Working Directory, D:\pycharm_project\mydjangoproject
	b)create project the existing files and code
	c)PyCharm settings(File->settings->project:current project name->Project Interpreter) set Interpreter


### run Debug server for Django project in PyCharm Community Edition
	a) In Run -> Edit Configurations create new configuration
	b) Script: path_to/manage.py
	c) Script parameters: runserver

### write and test your code and upload to Github

