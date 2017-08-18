from flask import Flask, render_template, request
import requests
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, ForeignKey, exists
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from flask.ext.heroku import Heroku
import json
import sys

##################################################################################
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
        Step 19: to check the total recipes in teh database go to "localhost:5000/totalrecipes"
'''
##################################################################################
#apiKey = "kTzgTwqO1zmshSLKmuobb6QvVJhWp1M3CUwjsnPd3OEIyHhYs2"
##################################################################################

app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisisasecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres://Kookinwats@ec2-54-163-237-25.compute-1.amazonaws.com:5432/d6nnmpc09qqr2n'
#app.config['SERVER_NAME'] = 'localhost:5000'

heroku = Heroku(app)
db = SQLAlchemy(app)

ingredients = db.Table('ingredients',
        db.Column('recipe_id', db.Integer,db.ForeignKey('recipe.id'), primary_key=True),
        db.Column('ingredient_id',db.Integer,db.ForeignKey('ingredient.id'), primary_key=True)
)

cuisines = db.Table('cuisines',
        db.Column('recipe_id', db.Integer,db.ForeignKey('recipe.id'), primary_key=True),
        db.Column('cuisine_id',db.Integer,db.ForeignKey('cuisine.id'), primary_key=True)
)

dishtypes = db.Table('dishtypes',
        db.Column('recipe_id', db.Integer,db.ForeignKey('recipe.id'), primary_key=True),
        db.Column('dishtype_id',db.Integer,db.ForeignKey('dishtype.id'), primary_key=True)
)

diets = db.Table('diets',
        db.Column('recipe_id', db.Integer,db.ForeignKey('recipe.id'), primary_key=True),
        db.Column('diet_id',db.Integer,db.ForeignKey('diet.id'), primary_key=True)
)

equipments = db.Table('equipments',
        db.Column('recipe_id', db.Integer,db.ForeignKey('recipe.id'), primary_key=True),
        db.Column('equipment_id',db.Integer,db.ForeignKey('equipment.id'), primary_key=True)
)

class Recipe(db.Model):
    __tablename__ = 'recipe'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255),nullable=False)
    imageUrl = db.Column(db.String, nullable=False)

    #One-to-One relationship between Recipe and Detail
    detail = relationship("Detail", uselist=False, back_populates="recipe")
    #One-to-One relationship between Recipe and NutritionFact
    nutritionfact = relationship("NutritionFact", uselist=False, back_populates="recipe")
    #One-to-Many relationship between Recipe and SimilarRecipe
    similarrecipes = db.relationship('SimilarRecipe', backref="recipe", cascade="all, delete-orphan" , lazy='dynamic')
    #One-to-Many relationship between Recipe and Instructions
    instructions = db.relationship('Instruction', backref="recipe", cascade="all, delete-orphan" , lazy='dynamic')
    #Many-to-Many relationship between Recipe and Ingredient
    ingredients = db.relationship('Ingredient', secondary=ingredients, lazy='subquery', backref=db.backref('recipes',lazy=True))
    #Many-to-Many relationship between Recipe and Cuisine
    cuisines = db.relationship('Cuisine', secondary=cuisines, lazy='subquery', backref=db.backref('recipes',lazy=True))
    #Many-to-Many relationship between Recipe and DishType
    dishtypes = db.relationship('DishType', secondary=dishtypes, lazy='subquery', backref=db.backref('recipes',lazy=True))
    #Many-to-Many relationship between Recipe and Diet
    diets = db.relationship('Diet', secondary=diets, lazy='subquery', backref=db.backref('recipes',lazy=True))
    #Many-to-Many relationship between Recipe and Equipment
    equipments = db.relationship('Equipment', secondary=equipments, lazy='subquery', backref=db.backref('recipes',lazy=True))

class Detail(db.Model):
    __tablename__ = 'detail'
    id = db.Column(db.Integer, primary_key=True)
    recipeSourceName = db.Column(db.String, nullable=False)
    recipeSourceUrl = db.Column(db.String, nullable=False)
    readyInMinutes = db.Column(db.Integer, nullable=False)
    servings = db.Column(db.Integer, nullable=False)
    pricePerServing = db.Column(db.Integer, nullable=False)
    saveCount = db.Column(db.Integer, nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))
    recipe = relationship("Recipe", back_populates="detail")

class Cuisine(db.Model):
    __tablename__ = 'cuisine'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

class DishType(db.Model):
    __tablename__ = 'dishtype'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

class Diet(db.Model):
    __tablename__ = 'diet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

class Equipment(db.Model):
    __tablename__ = 'equipment'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    imageUrl = db.Column(db.String, nullable=False)

class NutritionFact(db.Model):
    __tablename__ = 'nutritionfact'
    id = db.Column(db.Integer, primary_key=True)
    vegetarian = db.Column(db.Boolean, nullable=False)
    vegan = db.Column(db.Boolean, nullable=False)
    glutenFree = db.Column(db.Boolean, nullable=False)
    dairyFree = db.Column(db.Boolean, nullable=False)
    calories = db.Column(db.String, nullable=False)
    fat = db.Column(db.String, nullable=False)
    saturatedFat = db.Column(db.String, nullable=False)
    carbohydrates = db.Column(db.String, nullable=False)
    sugar = db.Column(db.String, nullable=False)
    cholesterol = db.Column(db.String, nullable=False)
    sodium = db.Column(db.String, nullable=False)
    protein = db.Column(db.String, nullable=False)
    fiber = db.Column(db.String, nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))
    recipe = relationship("Recipe", back_populates="nutritionfact")

class SimilarRecipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    similarRecipe_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(255),nullable=False)
    imageUrl = db.Column(db.String, nullable=False)
    readyInMinutes = db.Column(db.Integer, nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'),nullable=False)

class Instruction(db.Model):
    __tablename__ = 'instruction'
    id = db.Column(db.Integer, primary_key=True)
    stepNumber = db.Column(db.Integer, nullable=False)
    stepDescription = db.Column(db.String, nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'),nullable=False)

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255),unique=True,nullable=False)
    imageUrl = db.Column(db.String, nullable=False)
    #One-to-Many relationship between Ingredient and ingredientAmount
    ingredientamounts = db.relationship('ingredientAmount', backref="ingredient", cascade="all, delete-orphan" , lazy='dynamic')

class ingredientAmount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    unit = db.Column(db.String(20), nullable=False)
    originalString = db.Column(db.String, nullable=False)
    recipe_id = db.Column(db.Integer, nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'),nullable=False)

@app.route('/totalrecipes')
def totalRecipes():
    total = Recipe.query.count()
    return '<h1>Total Recipes in the Database: '+str(total)+'</h1>'

@app.route('/print')
def printRecipe():

    searchID = 694901
    #x = Ingredient.query.filter(ingredients.any(id=9292)).all()
    x = Ingredient.query.join(Ingredient.recipes).filter_by(id=searchID).all()
    r = Recipe.query.get(searchID)

    return render_template('print.html', ingredient=x, recipe=r )

@app.route('/addRecipe/<apiKey>')
def addRecipe(apiKey):
    totalRequests = 0
    ifCommit = True
    #get a random recipe
    randomCount = 2 # this can't be 1
    totalRequests += 1
    random = requests.get('https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/random?limitLicense=true&number=' + str(randomCount) ,
    headers={
    "X-Mashape-Key": apiKey,
    "Accept": "application/json"
      }
    )
    for i in range(0,randomCount-1):
        #get similar recipes of the random recipe
        totalRequests += 1
        s = requests.get('https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/' +str(random.json()["recipes"][i]["id"])+ '/similar',
        headers={
        "X-Mashape-Key": apiKey,
        "Accept": "application/json"
          }
        )
        similarJson = s.json()

        similar_list = []
        slist = ''

        similarAddList =[]
        #saves all the similar recipes' Ids to similar_list

        for similar in similarJson:
            similar_list.append(similar["id"])
            slist += str(similar["id"]) + ', '

        for sl in similar_list:
            with db.session.no_autoflush:
                #checks if the recipe already exists in the database
                if Recipe.query.get(sl):
                    return 'recipe already exists'

                else:
                    totalRequests += 1
                    searchRequest = requests.get('https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/'+str(sl)+'/information?includeNutrition=true',
                    headers={
                    "X-Mashape-Key": apiKey,
                    "Accept": "application/json"
                      }
                    )
                    json = searchRequest.json()

                    #return str(len(json["cuisines"]))
                    if len(json["analyzedInstructions"]) == 1 and len(json["cuisines"]):#!= 0 and len(json["dishTypes"]) != 0:# and len(json["diets"]) != 0:

                        jRecipeID = json["id"]

            ######################################################################################################################################################################################
                        # Creates a new Recipe Object
                        recipeObj = Recipe(id=jRecipeID,
                                           title = json["title"],
                                           imageUrl = json["image"]
                                           )
            ######################################################################################################################################################################################
                        cuisineString = ''
                        for cuisines in json["cuisines"]:
                            cuisineString += cuisines + ', '
                        if "sourceName" in json:
                            detailObj = Detail( recipeSourceUrl = json["sourceUrl"],
                                                recipeSourceName = json["sourceName"],
                                                readyInMinutes = json["readyInMinutes"],
                                                servings = json["servings"],
                                                pricePerServing = json["pricePerServing"]/100,
                                                saveCount = 0,
                                                recipe_id = jRecipeID,
                                                recipe = recipeObj
                                                )
                        else:
                            detailObj = Detail( recipeSourceUrl = json["sourceUrl"],
                                                recipeSourceName = '',
                                                readyInMinutes = json["readyInMinutes"],
                                                servings = json["servings"],
                                                pricePerServing = json["pricePerServing"]/100,
                                                saveCount = 0,
                                                recipe_id = jRecipeID,
                                                recipe = recipeObj
                                                )

            ######################################################################################################################################################################################
                        nutritionfactObj = NutritionFact (  vegetarian = json["vegetarian"],
                                                            vegan = json["vegan"],
                                                            glutenFree = json["glutenFree"],
                                                            dairyFree = json["dairyFree"],
                                                            calories = str(json["nutrition"]["nutrients"][0]["amount"]) + ' ' + json["nutrition"]["nutrients"][0]["unit"],
                                                            fat = str(json["nutrition"]["nutrients"][1]["amount"]) + ' ' + json["nutrition"]["nutrients"][1]["unit"],
                                                            saturatedFat = str(json["nutrition"]["nutrients"][2]["amount"]) + ' ' + json["nutrition"]["nutrients"][2]["unit"],
                                                            carbohydrates = str(json["nutrition"]["nutrients"][3]["amount"]) + ' ' + json["nutrition"]["nutrients"][3]["unit"],
                                                            sugar = str(json["nutrition"]["nutrients"][4]["amount"]) + ' ' + json["nutrition"]["nutrients"][4]["unit"],
                                                            cholesterol = str(json["nutrition"]["nutrients"][5]["amount"]) + ' ' + json["nutrition"]["nutrients"][5]["unit"],
                                                            sodium = str(json["nutrition"]["nutrients"][6]["amount"]) + ' ' + json["nutrition"]["nutrients"][6]["unit"],
                                                            protein = str(json["nutrition"]["nutrients"][7]["amount"]) + ' ' + json["nutrition"]["nutrients"][7]["unit"],
                                                            fiber = str(json["nutrition"]["nutrients"][14]["amount"]) + ' ' + json["nutrition"]["nutrients"][14]["unit"],
                                                            recipe_id = json["id"],
                                                            recipe = recipeObj
                                                        )
            ######################################################################################################################################################################################
                        if len(json["analyzedInstructions"]) == 1:
                            upperRange = len(json["analyzedInstructions"][0]["steps"])
                            e_list = []

                            for ins in range(0,upperRange):
                                insNumber = json["analyzedInstructions"][0]["steps"][ins]["number"]
                                insStep = json["analyzedInstructions"][0]["steps"][ins]["step"]

                                instructionObj = Instruction(stepNumber = insNumber,
                                                             stepDescription = insStep,
                                                             recipe_id = jRecipeID
                                                             )
                                recipeObj.instructions.append(instructionObj)

                                for eq in range(0, len(json["analyzedInstructions"][0]["steps"][ins]["equipment"])):
                                    e = json["analyzedInstructions"][0]["steps"][ins]["equipment"][eq]
                                    if e["name"] in e_list:
                                        pass
                                    else:
                                        if Equipment.query.filter_by(name=e["name"]).first():
                                            recipeObj.equipments.append(Equipment.query.filter_by(name=e["name"]).first())
                                        else:
                                            if "image" in e:
                                                e_image = e["image"]
                                            else:
                                                e_image = ""
                                            equipmentObj = Equipment(name=e["name"], imageUrl=e_image)
                                            recipeObj.equipments.append(equipmentObj)
                                            db.session.add(equipmentObj)
                                            db.session.commit()
                                        e_list.append(e["name"])

            ######################################################################################################################################################################################
                        cuisineUpperRange = len(json["cuisines"])
                        for i in range(0,cuisineUpperRange):
                            #print (json["cuisines"][i])
                            if Cuisine.query.filter_by(name=json["cuisines"][i]).first():
                                recipeObj.cuisines.append(Cuisine.query.filter_by(name=json["cuisines"][i]).first())
                            else:
                                cuisineObj = Cuisine(name=json["cuisines"][i])
                                recipeObj.cuisines.append(cuisineObj)
                                db.session.add(cuisineObj)

                        dishtypeUpperRange = len(json["dishTypes"])
                        for i in range(0,dishtypeUpperRange):
                            if DishType.query.filter_by(name=json["dishTypes"][i]).first():
                                recipeObj.dishtypes.append(DishType.query.filter_by(name=json["dishTypes"][i]).first())
                            else:
                                dishtypeObj = DishType(name=json["dishTypes"][i])
                                recipeObj.dishtypes.append(dishtypeObj)
                                db.session.add(dishtypeObj)

                        dietUpperRange = len(json["diets"])
                        for i in range(0,dietUpperRange):
                            if Diet.query.filter_by(name=json["diets"][i]).first():
                                recipeObj.diets.append(Diet.query.filter_by(name=json["diets"][i]).first())
                            else:
                                dietObj = Diet(name=json["diets"][i])
                                recipeObj.diets.append(dietObj)
                                db.session.add(dietObj)

            ######################################################################################################################################################################################
                        iupperRange = len(json["extendedIngredients"])
                        i_list= []
                        for i in range(0,iupperRange):
                            with db.session.no_autoflush:
                                if "id" in json["extendedIngredients"][i]:
                                    ingID = json["extendedIngredients"][i]["id"]
                                    ingName = json["extendedIngredients"][i]["name"]
                                    ingImage = json["extendedIngredients"][i]["image"]
                                    ingAmount = json["extendedIngredients"][i]["amount"]
                                    ingUnit = json["extendedIngredients"][i]["unit"]
                                    ingOriginalString = json["extendedIngredients"][i]["originalString"]
                                    #print (ingName)

                                    ingredientamountObj = ingredientAmount(recipe_id = jRecipeID,
                                                                           amount = ingAmount,
                                                                           unit = ingUnit,
                                                                           originalString = ingOriginalString,
                                                                           ingredient_id = ingID
                                                                           )
                                    print (str(ingID) + ingName)
                                    if ingID in i_list:
                                        print ('no')
                                        pass
                                    else:
                                        if Ingredient.query.get(ingID):
                                            Ingredient.query.get(ingID).ingredientamounts.append(ingredientamountObj)
                                            db.session.add(ingredientamountObj)
                                            recipeObj.ingredients.append(Ingredient.query.get(ingID))
                                        else:
                                            ingredientObj = Ingredient(id=ingID, name=ingName, imageUrl=ingImage)
                                            ingredientObj.ingredientamounts.append(ingredientamountObj)
                                            recipeObj.ingredients.append(ingredientObj)
                                            db.session.add(ingredientamountObj)
                                            db.session.add(ingredientObj)
                                            db.session.commit()
                                        i_list.append(ingID)
                                        print('yes')

                        #print (iupperRange)

                        if len(json["analyzedInstructions"]) == 1:
                            db.session.add(recipeObj)
                            similarAddList.append(jRecipeID)
                            print ("New recipe has been added")

        if(ifCommit):
            db.session.commit()

            for i in similarAddList:
                for si in similarAddList:
                    if(i == si):
                        pass
                    else:
                        for s in similarJson:
                            if si == s["id"]:
                                imageUrlString = 'https://spoonacular.com/recipeImages/' + s["image"]
                                similarrecipeObj = SimilarRecipe(similarRecipe_id = s["id"],
                                                                title = s["title"],
                                                                imageUrl = imageUrlString,
                                                                readyInMinutes = s["readyInMinutes"],
                                                                recipe_id = i
                                                                )
                                Recipe.query.get(i).similarrecipes.append(similarrecipeObj)

            db.session.commit()
            print ("Committed")

    return '<h1>Total Recipes: ' + str(Recipe.query.count()) + '<br>Total Similar Recipes: ' + str(SimilarRecipe.query.count()) + '<br>Total Requests: ' + str(totalRequests) + '</h1>'

@app.route('/')
def index():
    return '<h1>This is the home page</h1>'

if __name__ == '__main__':
    app.run(debug=True)
