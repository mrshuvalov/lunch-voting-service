# Lunch Voting Service

This API provides endpoints to facilitate the process of voting to decide where to have lunch.

## Endpoints

### `POST /accounts/register/`

Registers a new user account.

**Request Body:**
{ "login": "shuvalov_nv", "username": "shuvalov_nv", "password": "qwerty!1234", "password_confirm": "qwerty!1234" }

Markdown



### `POST /accounts/login/`

Logs in a registered user.

**Request Body:**
{ "login": "shuvalov_nv", "password": "qwerty!1234" }

Markdown



### `POST /companies/`

Creates a new company.

**Request Body:**
{ "name": "MindTales" }

Markdown



### `POST /restaurants/`

Creates a new restaurant.

**Request Body:**
{ "name": "Kata" }

Markdown



### `POST /menus/`

Creates a new menu for a restaurant on a specific date.

**Request Body:**
{ "date": "2023-05-10", "restaurant": 1, "items": [ { "name": "Rolls", "price": 20000, "weight": 400 } ] }

Markdown



### `POST /vote` (Version 1.0)

Registers a vote for a single menu.

**Request Body:**
{ "menu_id": 4 }

Markdown



### `POST /vote` (Version 2.0)

Registers a vote for multiple menus in descending order of preference.

**Request Body:**
{ "menu_id_1": 4, "menu_id_2": 3, "menu_id_3": 2 }

Markdown



### `GET /get_vote_results/`

Retrieves the current vote results.