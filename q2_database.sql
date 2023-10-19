-- Database Summary --
/*Database created to be used as a reference for API.
It contains data about cocktails recipes*/

-- For readability purpose PascalCase will be used for naming

/*For normalisation the next set of rules has been applied to the tables in the database:
	-Non-key attributes are dependent on the primary key only
    -There are no groups repeated
    -Every table has a primary key
    -There are no mixed types in a single column
    -There are no table that is the result of joining other tables
 So, the only data repeated in the database is that contained in the columns used as foreign keys
*/

-- For testing purposes
-- Drop database cocktails;

-- create and use the DB --
Create Database IF NOT EXISTS Cocktails;
Use Cocktails;

-- create table containing cocktail name and information --
Create Table IF NOT EXISTS CocktailsName (
CocktailId INT auto_increment NOT NULL,
CocktailName VARCHAR(30) NOT NULL,
Calories INT,
CountryOrigin VARCHAR(30),
Alcoholic BOOL NOT NULL,
Primary key (CocktailId)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- create table with a list of alcoholic beverages and their alcohol percentage
Create Table IF NOT EXISTS AlcoholicBeverages (
AlcoholicBeverage VARCHAR(30) NOT NULL,
AlcoholPercentage INT NOT NULL,
Primary key (AlcoholicBeverage)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- create table listing wet ingredients matching cocktailId --
-- provides the amount of the ingredient needed for the recipe in ml. --
Create Table IF NOT EXISTS WetIngredients (
WetIngredient VARCHAR(30) NOT NULL,
CocktailId INT NOT NULL,
AmountMl INT,
Primary key (WetIngredient, CocktailID)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- create table listing dry ingredients matching cocktailId --
-- provides the amount of the ingredient needed for the recipe 
-- in gr., tea spoons and/or units
Create Table IF NOT EXISTS DryIngredients (
DryIngredient VARCHAR(30) NOT NULL,
CocktailId INT NOT NULL,
AmountTeaSpoons INT,
AmountUnits INT,
WeightGr INT,
Primary key (DryIngredient, CocktailID)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- 
-- Populate tables --
INSERT INTO CocktailsName 
(CocktailName, Calories, CountryOrigin, Alcoholic)
VALUES
('Daiquiri', 264, 'Cuba', TRUE),
('Caipirinha', 390, 'Brazil', TRUE),
('Mojito', 99, 'Cuba', TRUE),
('Bloody Mary', 111, 'France', TRUE),
('Sex on the Beach', 326, 'United States', TRUE),
('Margarita', 170, 'Mexico', TRUE);


INSERT INTO AlcoholicBeverages
(AlcoholicBeverage, AlcoholPercentage)
VALUES
('White Tequila', 38),
('Triple Sec', 39),
('White Rum', 37.5),
('Cachaça', 45),
('Vodka', 70),
('Whiskey', 43),
('Absinthe', 71);


INSERT INTO WetIngredients 
(WetIngredient, CocktailId, AmountMl)
VALUES
('White Tequila', 6, 50),
('Triple Sec', 6, 25),
('Lemon juice', 6, 25),
('White rum', 1, 60),
('Lime juice', 1, 20),
('Cachaça', 2, 60),
('White rum', 3, 45),
('Lime juice', 3, 20),
('Sparkling water', 3, 20),
('Vodka', 4, 45),
('Tomato juice', 4, 90),
('Limon juice', 4, 15),
('Worcestersire sauce', 4, 5),
('Tabasco', 4, 2),
('Vodka', 5, 40),
('Peach juice', 5, 20),
('Orange juice', 5, 40),
('Blueberry juice', 5, 40);

INSERT INTO DryIngredients 
(DryIngredient, CocktailId, AmountTeaSpoons, AmountUnits, WeightGr)
VALUES
('Salt',6, NULL, NULL, 3),
('Sugar', 1, 2, NULL, 30),
('Ice', 1, NULL, 4, NULL),
('Lime', 2, NULL, 1, NULL),
('White cane sugar', 2, 4, NULL, NULL),
('Spearmint', 3, NULL, 6, NULL),
('White cane sugar', 3, 2, NULL, NULL),
('Celery salt', 4, NULL, NULL, 2.5),
('Black pepper', 4, NULL, NULL, 1);

