-- Create database if you haven't already. Note: uncomment the next line to create the database if it doesn't exist.
CREATE DATABASE foodshop;
 GO

USE foodshop;
GO

IF OBJECT_ID('users', 'U') IS NULL
BEGIN
    CREATE TABLE users (
        id BIGINT IDENTITY(1,1) PRIMARY KEY,
        username VARCHAR(50) NOT NULL UNIQUE,
        email VARCHAR(100) NOT NULL,
        password VARCHAR(255) NOT NULL,
        role VARCHAR(20) DEFAULT 'CUSTOMER',
        locked BIT DEFAULT 0
    );
END

IF NOT EXISTS (
    SELECT 1
    FROM users
    WHERE username = 'owner'
)
BEGIN
    INSERT INTO users
    (
        username,
        email,
        password,
        role,
        locked
    )
    VALUES
    (
        'owner',
        'owner@foodshop.com',
        'password',
        'OWNER',
        0
    );
END
GO

-- ==========================================
-- DEMO CUSTOMER
-- ==========================================

IF NOT EXISTS (
    SELECT 1
    FROM users
    WHERE username = 'customer'
)
BEGIN
    INSERT INTO users
    (
        username,
        email,
        password,
        role,
        locked
    )
    VALUES
    (
        'customer',
        'customer@foodshop.com',
        'password',
        'CUSTOMER',
        0
    );
END
GO


IF OBJECT_ID('foods', 'U') IS NULL
BEGIN
    CREATE TABLE foods (
        id BIGINT IDENTITY(1,1) PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        description TEXT,
        price DECIMAL(10, 2) NOT NULL,
        image_url VARCHAR(255),
        category VARCHAR(50)
    );
END

-- Insert dummy foods based on the frontend HTML data
IF NOT EXISTS (SELECT 1 FROM foods)
BEGIN
    INSERT INTO foods (name, description, price, image_url, category) VALUES
    ('Vegetable Combo', 'A healthy mix of fresh vegetables for family meals.', 3.50, 'https://images.unsplash.com/photo-1566385101042-1a0aa0c1268c?auto=format&fit=crop&w=800&q=80', 'vegetables'),
    ('Fresh Broccoli', 'Green broccoli rich in vitamins and fiber.', 2.80, 'https://images.unsplash.com/photo-1584270354949-c26b0d5b4a0c?auto=format&fit=crop&w=800&q=80', 'vegetables'),
    ('Organic Carrots', 'Sweet and crunchy carrots for healthy cooking.', 2.20, 'https://images.unsplash.com/photo-1445282768818-728615cc910a?auto=format&fit=crop&w=800&q=80', 'vegetables'),
    ('Fresh Tomatoes', 'Juicy tomatoes for salads, soups, and sauces.', 2.50, 'https://images.unsplash.com/photo-1592924357228-91a4daadcfea?auto=format&fit=crop&w=800&q=80', 'vegetables'),
    ('Fresh Beef', 'High-quality beef, safely packed and delivered.', 6.50, 'https://images.unsplash.com/photo-1603048297172-c92544798d5a?auto=format&fit=crop&w=800&q=80', 'meat'),
    ('Chicken Breast', 'Fresh chicken breast, perfect for healthy dishes.', 4.80, 'https://images.unsplash.com/photo-1604503468506-a8da13d82791?auto=format&fit=crop&w=800&q=80', 'meat'),
    ('Fresh Salmon', 'Premium salmon with rich flavor and nutrients.', 8.90, 'https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?auto=format&fit=crop&w=800&q=80', 'meat'),
    ('Fresh Shrimp', 'Clean and fresh shrimp for seafood dishes.', 7.20, 'https://images.unsplash.com/photo-1565680018434-b513d5e5fd47?auto=format&fit=crop&w=800&q=80', 'meat'),
    ('Orange Juice', 'Fresh orange juice with natural vitamin C.', 1.80, 'https://images.unsplash.com/photo-1600271886742-f049cd451bba?auto=format&fit=crop&w=800&q=80', 'drinks'),
    ('Fresh Milk', 'Pure fresh milk for daily nutrition.', 2.10, 'https://images.unsplash.com/photo-1563636619-e9143da7973b?auto=format&fit=crop&w=800&q=80', 'drinks'),
    ('Iced Coffee', 'Refreshing iced coffee for busy mornings.', 2.50, 'https://images.unsplash.com/photo-1517701604599-bb29b565090c?auto=format&fit=crop&w=800&q=80', 'drinks'),
    ('Green Tea', 'Healthy green tea with a fresh taste.', 1.60, 'https://images.unsplash.com/photo-1556679343-c7306c1976bc?auto=format&fit=crop&w=800&q=80', 'drinks'),
    ('Chicken Burger', 'A tasty and convenient meal for busy days.', 2.20, 'https://images.unsplash.com/photo-1551782450-a2132b4ba21d?auto=format&fit=crop&w=800&q=80', 'snacks'),
    ('French Fries', 'Crispy fries served hot and delicious.', 1.90, 'https://images.unsplash.com/photo-1630384060421-cb20d0e0649d?auto=format&fit=crop&w=800&q=80', 'snacks'),
    ('Chocolate Cake', 'Soft and sweet chocolate cake for dessert.', 3.20, 'https://images.unsplash.com/photo-1578985545062-69928b1d9587?auto=format&fit=crop&w=800&q=80', 'snacks'),
    ('Potato Chips', 'Crispy potato chips for light snacks.', 1.50, 'https://images.unsplash.com/photo-1566478989037-eec170784d0b?auto=format&fit=crop&w=800&q=80', 'snacks');
END
