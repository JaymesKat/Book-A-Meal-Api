# Book-A-Meal-Api
> Book-A-Meal-API is an API  that allow customers to make food orders and helps food vendors know what the customers' orders and manage them.

This project was done during the Andela Bootcamp Cohort 7

## Technologies used

* Python 3
* Flask
* Virtualenv

## Installation

Run the following commands to have your project setup

Clone the repository

```sh
git clone https://github.com/Jpkat92/Book-A-Meal-Api/tree/develop
```

Change to project directory

```sh
cd Book-A-Meal-Api
```

Create and launch the virtual environment

```sh
virtualenv venv
source venv\scripts\activate (Linux/iOS)
venv\Scripts\activate
```

Install dependencies

```sh
pip install -r requirements.txt
```
## Features

Customers can;
* Register
* Login
* View a daily menu of meal options
* Place an order by selecting meal options

Food Vendors/Caterers can;
* Login
* View customer order details
* Setup daily menu


## How to  run tests

Navigate to the `tests` directory 

```sh
cd tests
```
Run the tests 

```sh
pytest
```