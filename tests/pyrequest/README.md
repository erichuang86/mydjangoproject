### create db guest_test
    1.CREATE DATABASE guest_test CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
    2.D:\mydjangoproject>python manage.py migrate

### clear up the database
    SET FOREIGN_KEY_CHECKS = 0; 
    TRUNCATE table sign_event;
    TRUNCATE table sign_guest; 
    SET FOREIGN_KEY_CHECKS = 1;

### reference
    https://github.com/defnngj/pyrequest
    https://github.com/defnngj/guest2