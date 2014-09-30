# pg_change_owner
Change owner on every table view and sequence in a PostgreSql database.

This simple python script can help you on change owner of table, sequences and view.

The script use PostgreSql CLI 'psql' for to do owner changes.

For to use you have to set database name and new owner that you want.

'''
python pg_change_owner -d [DATABASE_NAME] -o [OWNER]
'''

Important this script is made for a standard Ubuntu Installation, so you have to roun the script with postgres system user.