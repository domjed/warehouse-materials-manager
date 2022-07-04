# warehouse-materials-manager

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)

## General info
The app was written to facilite management of raw materials stored in a warehouse. Update of current stock status can be done by clicking "Add new material trade" button on main page. Afterwards, the user is redirected to form filling page. Once material data is provided and saved it can be wieved together with other historical entries. It can be done by clicking "Go to saved trades" button. The user has a possibility to sort and filter results as per miscelaneous criteria. If neccessary, provided input can be wieved again, modified or pernamently removed from database. For better app navigation, unfolding menu at the top of a page is added.
	
## Technologies
Project is created with:
* Python v3.10.4
* Flask v2.0.2
* Flask-SQLAlchemy v2.5.1
* HTML5
* Bootstrap v4.3.1 (https://getbootstrap.com/)

## Setup
Once all above mentioned dependencies are installed, run the project via command prompt by executing python app.py. This file is
placed in main folder of the application:

```
1. cd -> [main project directory path e.g.: cd ./warehouse-manager-app-main]
2. $ python app.py
3. The app is ready to be used locally
```
