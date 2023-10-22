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
/* Columns: Id (to uniquely identify cocktails) is table's primery key
			CocktailName, Calories, CountryOrigin, ALcoholic 
            (Value showing if the selected cocktails contains ALcohol or not)*/
Create Table IF NOT EXISTS CocktailsInfo (
Id INT auto_increment NOT NULL,
CocktailName VARCHAR(30) NOT NULL,
Calories INT,
CountryOrigin VARCHAR(30),
Alcoholic BOOL NOT NULL,
Primary key (Id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- create table listing all ingredients and their Id --
CREATE TABLE IF NOT EXISTS Ingredients (
    IngredientId INT AUTO_INCREMENT NOT NULL,
    IngredientName VARCHAR(30) NOT NULL,
    PRIMARY KEY (IngredientId)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- create table listing ingredients matching cocktailId (through a composite primary key) --
-- provides the amount of the ingredient needed for the recipe in ml., gr., tea spoons and/or units --
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

/* -- COMMENTED BY NOW, TO BE USED IF NEEDED --
-- create archive table for the recipes removed from the menu through the API --
CREATE TABLE IF NOT EXISTS RecipesArchive (
    CocktailName VARCHAR(30) NOT NULL
    IngredientId INT NOT NULL,
    AmountMl INT DEFAULT NULL,
    AmountTeaSpoons INT DEFAULT NULL,
    AmountUnits INT DEFAULT NULL,
    WeightGr FLOAT DEFAULT NULL,
    PRIMARY KEY (CocktailName, IngredientId),
    FOREIGN KEY (IngredientId) REFERENCES Ingredients(IngredientId)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;*/


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


INSERT INTO Ingredients(IngredientName) 
VALUES
('Salt'),
('Sugar'),
('Ice'),
('Lime'),
('White cane sugar'),
('Spearmint'),
('Celery salt'),
('Black pepper'),
('Lime juice'),
('Lemon juice'),
('Cherry'),
('Sparkling water'),
('Tomato juice'),
('Worcestersire sauce'),
('Tabasco'),
('Peach juice'),
('Orange juice'),
('Blueberry juice'),
('Granadine'),
('Pineapple juice'),
('Soda water'),
('White Tequila'),
('Triple Sec'),
('White Rum'),
('Cachaça'),
('Vodka'),
('Whiskey'),
('Absinthe'),
('Vermouth'), 
('Citron Vodka'),
('Cointreau'),
('Proseco'),
('Aperol');

-- Testing
-- SELECT *
-- FROM Ingredients;

INSERT INTO CocktailIngredients (CocktailId, IngredientId, AmountTeaSpoons, AmountUnits, WeightGr)
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

INSERT INTO Ingredients 
(IngredientId, CocktailId, AmountMl)
VALUES
(22, 6, 50),
(23, 6, 25),
(10, 6, 25),
(24, 1, 60),
(9, 1, 20),
(25, 2, 60),
(24, 3, 45),
(9, 3, 20),
(12, 3, 20),
(26, 4, 45),
(13, 4, 90),
(10, 4, 15),
(14, 4, 5),
(15, 4, 2),
(26, 5, 40),
(16, 5, 20),
(17, 5, 40),
(18, 5, 40),
(19, 8, 30),
(12, 8, 50),
(17, 7, 50),
(20, 7, 20),
(10, 7, 10),
(32, 9, 40),
(33, 9, 40),
(21, 9, 5),
(22, 10, 50),
(23, 10, 25),
(10, 10, 25);


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
 - ('Lemon juice', 6, 10) (in ml) to modify San Francisco recipe
 - ('Vodka', 6, 10) (in ml) to add alcohol to the San Francisco recipe ***ALCOHOLIC must be changed to TRUE***
 - ('Mango', 1, 1) (in units) to make Daiquiri a Mango Daiquiri ++Calories will rise to 295++
*/




