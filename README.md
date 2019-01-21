# Meneetz
CZ3002 Assignment - Group Se7en


## Requirements

1. `Python=3.6`
2. `Postgres`

## Installation

1. Clone the repository: `git clone git@github.com:MIlhamDedi/meneetz.git`.
2. `cd meneetz`.
3. Create new virtualenv `venv`: `virtualenv venv -p python3.6 | source venv/bin/activate`.
4. Install dependencies: `pip install -r requirements.txt`.
5. Set `meneetz` database in local Postgres and update `settings.py` user definition.
6. Run first migration `python manage.py migrate` then run the project with `python manage.py runserver`.