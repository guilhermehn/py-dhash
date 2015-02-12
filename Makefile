all: createdb

createdb:
	sqlite3 dhash.db < sql_scripts/create_commands.txt

pip:
	sudo pip install -r requirements.txt

.PHONY: all
