Hi team! A few notes:

1. You need a .env file at the project root. It should contain MYSQL_HOST, MYSQL_PORT, MYSQL_DB, MYSQL_USER, MYSQL_PASSWORD variables. This info is in the Discord.
2. Run the api locally with the terminal (in VSCode, CTRL+`) command: uvicorn main:app --reload
3. There is a directory structure here for entities. Patron will be a good example.
4. Each entity directory should have a models.py to define the database schema mySQL-side. Per Gemini, It represents the internal database structure. It includes everything, like password hashes, internal state flags, join keys, etc. Use the following command to auto-generate this: sqlacodegen "mysql+pymysql://USERNAME:PASSWORD@HOST:PORT/DATABASE_NAME" --tables TABLE_NAME > LOCATION_FOR_RESULT_PY_FILE
5. Each entity directory will have a schemas.py file. Per Gemini, it represents your public API contract. It's what you expose to the outside world. This has to have a simple base model for the entity and then base models for various operations (CRUD for example). Unfortunately, this is a manual thing.
6. Each entity directory will have a services.py file. This is where we define any logic for retrieval/manipulation. For testing, we can have CRUD and other functions here, but Views and Stored Procedures in mySQL should suffice.
7. Each entity directory will have a router.py file. This governs the actual HTTP requests/responses.
