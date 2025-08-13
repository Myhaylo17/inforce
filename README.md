Lunch Voting  — an internal company service that helps employees choose a place for lunch.  
Each restaurant uploads its daily menu, and employees vote for it before lunch.  
The system stores voting results and allows retrieving them at any time during the current day.

---

 API Features
User authentication (JWT)
Create restaurant
Upload restaurant menu (a separate menu for each day)
Create employee
Get current day's menu
Get voting results for the current day

---

 Tech Stack
Backend: Django + Django REST Framework (DRF)
Database: MySQL
Authentication:JWT 
Testing: Pytest

You can add restaurants/menus through the admin panel or through the httpie module by writing commands, 
you can check the menu votes and which restaurants are open today: admin panel or through the httpie module by writing commands.


At any moment you can see which restaurants are open today or which restaurant won the vote today.


run the program classically with the command python manage.py runserver 
Log in to the account via the url api/token
check restaurants etc in the admin panel
