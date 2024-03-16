Student Management System API
First you need to create virtual Environment. After that install requirements.txt.
import postman collections - https://api.postman.com/collections/22946176-186f2049-8160-49a1-ab6a-d2ffc5b5b731?access_key=PMAT-01HS34SYY7T6XADB8V89KE8C6J

http://127.0.0.1:8000/api/student-class - This url is used for the GET and POST student class. \method - POST\GET ||
http://127.0.0.1:8000/api/register-student   - This url working for the register Student and Get All student List. \method - POST\GET ||
http://127.0.0.1:8000/api/login-student - This url working for login user and generate jwt  Refresh Token and Access Token, through the mobile_number and password. when user is activated then user login . \method - POST\ ||
http://127.0.0.1:8000/api/update-student - This url working for the updating deleting user profile details and all. \method - GET\PUT\DELETE ||
http://127.0.0.1:8000/api/perm-student/14 - This url working for the give permission for the login only admin user can give permission another user. \method - PATCH ||
