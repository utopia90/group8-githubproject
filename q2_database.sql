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
Create Table IF NOT EXISTS CocktailsInfo (
Id INT auto_increment NOT NULL,
CocktailName VARCHAR(30) NOT NULL,
Calories INT,
CountryOrigin VARCHAR(30),
Alcoholic BOOL NOT NULL,
Primary key (Id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- create table with a list of alcoholic beverages and their alcohol percentage
Create Table IF NOT EXISTS AlcoholicBeverages (
AlcoholicBeverage VARCHAR(30) NOT NULL,
AlcoholPercentage FLOAT NOT NULL,
Primary key (AlcoholicBeverage)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- create table listing ingredients matching cocktailId --
-- provides the amount of the ingredient needed for the recipe in ml., gr., tea spoons and/or units --
CREATE TABLE IF NOT EXISTS Ingredients (
    IngredientId INT AUTO_INCREMENT NOT NULL,
    IngredientName VARCHAR(30) NOT NULL,
    PRIMARY KEY (IngredientId)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Intermediary table that links cocktails with the ingredients we use.
CREATE TABLE IF NOT EXISTS CocktailIngredients (
    CocktailId INT NOT NULL,
    IngredientId INT NOT NULL,
    AmountMl INT DEFAULT NULL,
    AmountTeaSpoons INT DEFAULT NULL,
    AmountUnits INT DEFAULT NULL,
    WeightGr FLOAT DEFAULT NULL,
    PRIMARY KEY (CocktailId, IngredientId),
    FOREIGN KEY (CocktailId) REFERENCES CocktailsInfo(Id),
    FOREIGN KEY (IngredientId) REFERENCES Ingredients(IngredientId)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Populate tables --
INSERT INTO CocktailsInfo
(CocktailName, Calories, CountryOrigin, Alcoholic)
VALUES
('Daiquiri', 264, 'Cuba', TRUE),
('Caipirinha', 390, 'Brazil', TRUE),
('Mojito', 99, 'Cuba', TRUE),
('Bloody Mary', 111, 'France', TRUE),
('Sex on the Beach', 326, 'United States', TRUE),
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


INSERT INTO Ingredients(IngredientName) 
VALUES
('Salt'),
('Sugar'),
('Ice'),
('Lime'),
('White cane sugar'),
('Spearmint'),
('White cane sugar'),
('Celery salt'),
('Black pepper'),
('Lime juice'),
('Lemon juice'),
('Cherry'),
('Sugar');

INSERT INTO CocktailIngredients (CocktailId,IngredientId, AmountTeaSpoons, AmountUnits, WeightGr)
VALUES
(6,1, NULL, NULL, 2),
(1,2, NULL, 30, NULL),
(1,3, NULL, 4, NULL),
(2,4, NULL, 1, NULL),
(2,5, 4, NULL, NULL),
(3,6, NULL, 6, NULL),
(3,7, 2, NULL, NULL),
(4,8,NULL, NULL, 2.5),
(4,9, NULL, NULL, 1),
(8,10, NULL, NULL,2),
(8,11,4, NULL, NULL),
(8,12, NULL, 2, NULL),
(7,13,NULL, NULL,5),
(9,13,NULL, NULL, 1);


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



