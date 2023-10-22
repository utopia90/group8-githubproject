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
AlcoholicBeverageID INT auto_increment NOT NULL,
AlcoholicBeverage VARCHAR(30) NOT NULL,
AlcoholPercentage FLOAT NOT NULL,
Primary key (AlcoholicBeverageID)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- create table listing ingredients matching cocktailId --
-- provides the amount of the ingredient needed for the recipe in ml., gr., tea spoons and/or units --
Create Table IF NOT EXISTS Ingredients (
Ingredient VARCHAR(30) NOT NULL,
CocktailId INT NOT NULL,
AmountMl INT default NULL,
AmountTeaSpoons INT default NULL,
AmountUnits INT default NULL,
WeightGr FLOAT default NULL,
AlcoholicBeverageID INT default NULL,
Primary key (Ingredient, CocktailID),
Foreign key (CocktailID) REFERENCES CocktailsName(CocktailID),
Foreign key (AlcoholicBeverageID) REFERENCES AlcoholicBeverages(AlcoholicBeverageID)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- Populate tables --
INSERT INTO CocktailsName 
(CocktailName, Calories, CountryOrigin, Alcoholic)
VALUES
('Daiquiri', 264, 'Cuba', TRUE),
('Caipirinha', 390, 'Brazil', TRUE),
('Mojito', 99, 'Cuba', TRUE),
('Bloody Mary', 111, 'France', TRUE),
('Sex on the Beach', 326, 'United States', TRUE),
('Margarita', 170, 'Mexico', TRUE),
('San Francisco', 160, 'United States', FALSE),
('Shirley Temple', 97, 'United States', FALSE),
('Aperol Spritz', 100, 'Italy', TRUE),
('Margarita', 170, 'Mexico', TRUE);


INSERT INTO AlcoholicBeverages
(AlcoholicBeverage, AlcoholPercentage)
VALUES
('White Tequila', 38),
('Triple Sec', 39),
('White Rum', 37.5),
('Cachaça', 45),
('Vodka', 50),
('Whiskey', 43),
('Absinthe', 71),
('Vermouth', 15), 
('Citron Vodka', 40),
('Cointreau', 40),
('Proseco', 11),
('Aperol', 11);

INSERT INTO Ingredients 
(Ingredient, CocktailId, AmountMl, AlcoholicBeverageID)
VALUES
('White Tequila', 6, 50, 1),
('Triple Sec', 6, 25, 2),
('Lemon juice', 6, 25, NULL),
('White rum', 1, 60, 3),
('Lime juice', 1, 20, NULL),
('Cachaça', 2, 60, 4),
('White rum', 3, 45, 3),
('Lime juice', 3, 20, NULL),
('Sparkling water', 3, 20, NULL),
('Vodka', 4, 45, 5),
('Tomato juice', 4, 90, NULL),
('Limon juice', 4, 15, NULL),
('Worcestersire sauce', 4, 5, NULL),
('Tabasco', 4, 2, NULL),
('Vodka', 5, 40, 5),
('Peach juice', 5, 20, NULL),
('Orange juice', 5, 40, NULL),
('Blueberry juice', 5, 40, NULL),
('Granadine', 8, 30, NULL),
('Sparkling water', 8, 50, NULL),
('Orange juice', 7, 50, NULL),
('Pineapple juice', 7, 20, NULL),
('Lemon juice', 7, 10, NULL),
('Proseco', 9, 40, 11),
('Aperol', 9, 40, 12),
('Soda water', 9, 5, NULL),
('White Tequila', 10, 50, 1),
('Triple sec', 10, 25, 2),
('Lemon juice', 10, 25, NULL);

INSERT INTO Ingredients 
(Ingredient, CocktailId, AmountTeaSpoons, AmountUnits, WeightGr)
VALUES
('Salt',6, NULL, NULL, 3),
('Sugar', 1, 2, NULL, 30),
('Ice', 1, NULL, 4, NULL),
('Lime', 2, NULL, 1, NULL),
('White cane sugar', 2, 4, NULL, NULL),
('Spearmint', 3, NULL, 6, NULL),
('White cane sugar', 3, 2, NULL, NULL),
('Celery salt', 4, NULL, NULL, 2.5),
('Black pepper', 4, NULL, NULL, 1),
('Lime juice', 8, 4, NULL, NULL),
('Lemon juice', 8, 4, NULL, NULL),
('Cherry', 8, NULL, 2, NULL),
('Sugar', 7, 1, NULL, NULL),
('Salt', 10, NULL, NULL, 1);


-- For testing porpuses
-- SELECT *
-- FROM Ingredients;



-- Extra data to be used for adding or modifying recipes --
/* New recipes:
- ('White russian', 216, 'Belgium', TRUE) ingredients(ml) -> ('Vodka', 50), ('Coffee liquor', 20), ('Cream milk', 30)
- ('Cosmopolitan', 134, 'United States', TRUE) ingredients(ml) -> ('Vodka Citron', 40), ('Cointreau', 15), ('Lime juice', 15), ('Cranberry juice', 30)
											   ingredients(units) -> ('Lemon rind', 1)
- ('Manhattan', 160, 'United States', TRUE) ingredients(ml) -> ('Whiskey', 50), ('Vermouth rosso', 20), ('Angostura', 2)
- ('Old Fashioned', 205, 'United States', TRUE) ingredients(ml) -> ('Boubon', 45), ('Cold water', 10), ('Angostura bitter', 1)
												ingredients(units) -> ('Cane sugar cube', 1)
- 

Adding:
 - ('Lemon juice', 7, 10) (in ml) to modify San Francisco recipe
 - ('Vodka', 7, 10) (in ml) to add alcohol to the San Francisco recipe ***ALCOHOLIC must be changed to TRUE***
 - ('Mango', 1, 1) (in units) to make Daiquiri a Mango Daiquiri ++Calories will rise to 295++
*/



