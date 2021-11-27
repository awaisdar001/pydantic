Data Mapping Script using pydantic
================================
This is simple script that will pull the newest articles from the provided API every 5 minutes,
then map them into a format defined in the `models.py` file (`class Article`) and finally print
them out.

Compatibility
-------------
This project is developed and tested with `python3.8`

Prerequisites
-------------
In order to set up this script, make sure you have python's `pip` package installed on your system.

Makefile
--------
The project adds a make file for running most common commands. These commands
should be run inside the virtualenv.

Instructions to run the script
------------------------------
1. Clone the Repo in your local machine.

       git clone https://github.com/awaisdar001/pydantic.git

2. Create a python3 virtualenv and activate it.

       python3 -m venv ~/venvs/venv-mapping
       source ~/venvs/venv-mapping/bin/activate

3. Install requirements inside of the virtual env
   
       make requirements

4. Run script
   
       make run 

_if Makefile fails on your system, try running the script manually._

      python3 mapping/main.py

What did I Learn
--------------------------
1. Learning `pydantic` - 3 hours
2. API design - 1 hour
3. Parser & Mapping for Article details - 2 hours
4. Understanding `sections` information & writing re-usable parser - 2 hours
5. Data validation for `pydantic` - 1 hour
6. I/O implementation + Type hints + docstrings - 1.5 hour
7. Wrapping up: `Makefile`, `ReadMe.md` & `.gitignore` and VCS.  
