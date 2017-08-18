'''
README: Step 1: Change apiKey variable with your key
        Step 2: Make sure to use the database I uploaded on github. That is our main database.
        Step 3: Change app.config[SQLALCHEMY_DATABASE_URI] with the path where your database is located.
        Step 4: open CMD and go to (cd) this folder. Name of the folder is database_populator
        Step 5: Make sure you are inside the project folder
        Step 6: Type "sqlite3 recipeDatabase.db"
        Step 7: Type ".tables"
        Step 8: Type ".exit"
        Step 9: Type "python"
        Step 10: Type "from app import db"
        Step 11: wait for it to finish loading and then type "db.create_all()"
        Step 12: Type "exit()"
        Step 13: Make sure you are the only one running the program and that your database is updated. Coordinate with others.
                 If im running adding recipes right now and you try to add recipes too at the same time, you wouldn't have the updated database.
                 Therefore, we need to take turns.
                 Run program. Type "python app.py"
        Step 14: open browser and go to "localhost:5000/addRecipe"
        Step 15: In your command line you should be able to see something like this:
                    2069balsamic vinegar
                    yes
                    1004blue cheese
                    yes
                    11098brussels sprouts
                    yes
                    4053olive oil
                    yes
                    10410123pancetta
                    yes
                    New recipe has been added
                    Committed
                    Committed
        Step 16: After this, it should show in the page the number of recipes you have in the database.
        Step 17: Sometimes it will only show this:
                    Committed
                    Comiited

                This means it didnt add any recipe. This is okay. The program only looks for complete recipe. If it's not, it rejects it
                Just refresh the page to run the pogram again. Keep doing this until you think you've added enough.
                I added 20 Recipes so I guess lets do a minimum of 20 Recipes? Just keep refreshing until you reach the quota
        Step 18: After a succesful run, it is recommended to make a copy of the database and then run again. Stop the program and make a copy of the database.
                This is your backup just in case something happens.
'''     Step 19: to check the total recipes in teh database go to "localhost:5000/totalrecipes"
        Step 20: After you are done, update the database on github so that the next person who is going to be running the program
                 will have the updated database.
