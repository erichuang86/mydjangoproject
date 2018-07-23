###  missing 1 required positional argument: 'on_delete'
	>issue
	vent = models.ForeignKey(Event)
    TypeError: __init__() missing 1 required positional argument: 'on_delete'
    >solution
    event = models.ForeignKey(Event,on_delete=models.CASCADE,)
    Since Django 2.x, on_delete is required.
	Deprecated since version 1.9: on_delete will become a required argument in Django 2.0. In older versions it defaults to CASCADE.
	
### from Crypto.Cipher import AES ModuleNotFoundError: No module named 'Crypto'
    Solution A
    pip uninstall crypto
    pip install pycrypto (Microsoft Visual C++ 14.0 is required)
    a) Download .whl file from https://www.lfd.uci.edu/~gohlke/pythonlibs/#pymssql
    b) install the .whl file
    c) pip install pymssql-2.1.3-cp36-cp36m- win32.whl
    
    Solution B
    pip install pycryptodome
### Run test
    D:\pycharm_project\mydjangoproject>python manage.py test tests.sec_interface_test.request_auth
    
    