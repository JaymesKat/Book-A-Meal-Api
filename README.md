# Book-A-Meal-Api
> Book-A-Meal-API is an API  that allow customers to make food orders and helps food vendors know what the customers' orders and manage them. This project was done during the Andela Bootcamp Cohort 7

[![Build Status](https://travis-ci.org/Jpkat92/Book-A-Meal-Api.svg?branch=develop)](https://travis-ci.org/Jpkat92/Book-A-Meal-Api)
[![Coverage Status](https://coveralls.io/repos/github/Jpkat92/Book-A-Meal-Api/badge.svg)](https://coveralls.io/github/Jpkat92/Book-A-Meal-Api)
[![Code Climate](https://codeclimate.com/github/codeclimate/codeclimate/badges/gpa.svg)](https://codeclimate.com/github/Jpkat92/Book-A-Meal-Api)

## Features

Customers can;
* Sign up
* Login
* View a daily menu of meal options
* Place an order by selecting meal options

Administrators/Caterers can;
* Login
* Create, retrieve, update and delete meal options 
* Setup daily menu
* View customer orders

## Technologies used

* Python 3
* Flask
* Virtualenv

## Installation

Run the following commands to have your project setup

Clone the repository

```sh
git clone https://github.com/Jpkat92/Book-A-Meal-Api.git
```

Change to project directory

```sh
cd Book-A-Meal-Api
```

Create and launch the virtual environment

```sh
virtualenv venv
Run 'source venv/bin/activate' on Linux or macOS
Run 'venv\Scripts\activate' on Windows
```

Install dependencies

```sh
pip install -r requirements.txt
```



## How to  run tests

Navigate to the `tests` directory 

```sh
cd tests
```
Run the tests 

```sh
pytest
```
