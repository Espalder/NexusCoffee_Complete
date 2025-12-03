-- ==========================================================
-- Nexus Coffee – Base de datos completa (MySQL 8.x) – VERSIÓN CORREGIDA
-- ==========================================================
DROP DATABASE IF EXISTS nexus_coffee;
CREATE DATABASE IF NOT EXISTS nexus_coffee CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE nexus_coffee;

-- 1. CATEGORIAS ---------------------------------------------
CREATE TABLE categorias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE NOT NULL,
    descripcion TEXT,
    INDEX idx_nombre (nombre)
);

-- 2. USUARIOS -----------------------------------------------
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    rol VARCHAR(20) NOT NULL CHECK (rol IN ('admin', 'vendedor', 'inventario')),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    activo BOOLEAN DEFAULT TRUE,
    INDEX idx_username (username),
    INDEX idx_rol (rol)
);

-- 3. PRODUCTOS ----------------------------------------------
CREATE TABLE productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    categoria_id INT NOT NULL,
    precio DECIMAL(10,2) NOT NULL CHECK (precio >= 0),
    stock INT NOT NULL CHECK (stock >= 0),
    stock_minimo INT DEFAULT 10 CHECK (stock_minimo > 0),
    descripcion TEXT,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    activo BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (categoria_id) REFERENCES categorias(id) ON DELETE RESTRICT,
    INDEX idx_categoria (categoria_id),
    INDEX idx_nombre (nombre)
);

-- 4. CLIENTES -----------------------------------------------
CREATE TABLE clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    telefono VARCHAR(20),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    activo BOOLEAN DEFAULT TRUE,
    INDEX idx_nombre (nombre),
    INDEX idx_email (email)
);

-- 5. VENTAS -------------------------------------------------
CREATE TABLE ventas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT NOT NULL,
    total DECIMAL(10,2) NOT NULL CHECK (total >= 0),
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_id INT,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE RESTRICT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE SET NULL,
    INDEX idx_fecha (fecha),
    INDEX idx_cliente (cliente_id)
);

-- 6. DETALLES_VENTA -----------------------------------------
CREATE TABLE detalles_venta (
    id INT AUTO_INCREMENT PRIMARY KEY,
    venta_id INT NOT NULL,
    producto_id INT NOT NULL,
    cantidad INT NOT NULL CHECK (cantidad > 0),
    precio_unitario DECIMAL(10,2) NOT NULL CHECK (precio_unitario >= 0),
    subtotal DECIMAL(10,2) NOT NULL CHECK (subtotal >= 0),
    FOREIGN KEY (venta_id) REFERENCES ventas(id) ON DELETE CASCADE,
    FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE RESTRICT,
    INDEX idx_venta (venta_id),
    INDEX idx_producto (producto_id)
);

-- 7. CONFIGURACION ------------------------------------------
CREATE TABLE configuracion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    clave VARCHAR(50) UNIQUE NOT NULL,
    valor VARCHAR(255) NOT NULL,
    descripcion TEXT
);

-- 8. AUDITORIA ----------------------------------------------
CREATE TABLE auditoria (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tabla VARCHAR(50) NOT NULL,
    accion VARCHAR(20) NOT NULL,
    usuario_id INT,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    detalles TEXT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE SET NULL
);

-- 9. PROVEEDORES --------------------------------------------
CREATE TABLE proveedores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    telefono VARCHAR(20),
    direccion TEXT,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    activo BOOLEAN DEFAULT TRUE,
    INDEX idx_nombre (nombre)
);

-- 10. ENTRADAS_INVENTARIO -----------------------------------
CREATE TABLE entradas_inventario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    producto_id INT NOT NULL,
    proveedor_id INT,
    cantidad INT NOT NULL CHECK (cantidad > 0),
    costo DECIMAL(10,2) NOT NULL CHECK (costo >= 0),
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_id INT,
    FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE RESTRICT,
    FOREIGN KEY (proveedor_id) REFERENCES proveedores(id) ON DELETE SET NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE SET NULL,
    INDEX idx_producto (producto_id),
    INDEX idx_fecha (fecha)
);

-- 11. TRIGGER: ACTUALIZAR STOCK EN VENTAS -------------------
DELIMITER //
CREATE TRIGGER actualizar_stock_venta AFTER INSERT ON detalles_venta
FOR EACH ROW
BEGIN
    UPDATE productos SET stock = stock - NEW.cantidad WHERE id = NEW.producto_id;
    IF (SELECT stock FROM productos WHERE id = NEW.producto_id) < 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Stock insuficiente para el producto';
    END IF;
END//
DELIMITER ;

-- 12. TRIGGER: AUDITORÍA DE VENTAS --------------------------
DELIMITER //
CREATE TRIGGER auditoria_ventas AFTER INSERT ON ventas
FOR EACH ROW
BEGIN
    INSERT INTO auditoria (tabla, accion, usuario_id, detalles)
    VALUES ('ventas', 'INSERT', NEW.usuario_id, CONCAT('Venta ID: ', NEW.id, ' para cliente ID: ', NEW.cliente_id));
END//
DELIMITER ;

-- 13. INSERTAR CATEGORÍAS -----------------------------------
INSERT INTO categorias (nombre, descripcion) VALUES
('Bebidas Calientes', 'Cafés y bebidas calientes clásicas'),
('Tés e infusiones', 'Variedad de tés e infusiones naturales'),
('Bebidas Frías', 'Bebidas refrescantes y heladas'),
('Bebidas Especiales', 'Bebidas de temporada y especiales'),
('Panadería', 'Productos horneados frescos'),
('Postres', 'Dulces y postres deliciosos'),
('Comida', 'Sándwiches, ensaladas y comidas ligeras');

-- 14. INSERTAR USUARIOS -------------------------------------
INSERT INTO usuarios (username, password, nombre, rol) VALUES
('admin', SHA2('admin123', 256), 'Administrador Principal', 'admin'),
('vendedor1', SHA2('venta123', 256), 'Vendedor de Turno', 'vendedor'),
('vendedor2', SHA2('venta456', 256), 'Vendedor Auxiliar', 'vendedor'),
('inventario1', SHA2('stock123', 256), 'Gestor de Inventario', 'inventario'),
('inventario2', SHA2('stock456', 256), 'Asistente de Inventario', 'inventario');

-- 15. INSERTAR PRODUCTOS (80 productos) ---------------------
INSERT INTO productos (nombre, categoria_id, precio, stock, stock_minimo, descripcion) VALUES
-- Bebidas Calientes (1)
('Espresso', 1, 22.00, 50, 15, 'Café puro, intenso y aromático, 30 ml de pureza italiana'),
('Espresso Doble', 1, 28.00, 40, 12, 'Doble shot de espresso para los amantes del café fuerte'),
('Americano', 1, 25.00, 45, 15, 'Espresso con agua caliente, suave y sabroso'),
('Café con Leche', 1, 32.00, 35, 12, 'Mitad café, mitad leche vaporizada, clásico y reconfortante'),
('Cappuccino', 1, 35.00, 30, 10, 'Espresso, leche vaporizada y espuma cremosa en proporción perfecta'),
('Cappuccino Italiano', 1, 38.00, 25, 8, 'Cappuccino tradicional con cacao amargo espolvoreado'),
('Latte', 1, 38.00, 35, 12, 'Espresso con leche vaporizada y una capa fina de espuma'),
('Latte Vanilla', 1, 42.00, 30, 10, 'Latte con jarabe de vainilla y crema batida'),
('Latte Caramelo', 1, 42.00, 30, 10, 'Latte con salsa de caramelo y crema batida'),
('Mocha', 1, 40.00, 25, 8, 'Espresso con chocolate, leche vaporizada y crema'),
('Mocha Blanco', 1, 42.00, 20, 8, 'Mocha con chocolate blanco en lugar de chocolate negro'),
('Macchiato', 1, 30.00, 30, 10, 'Espresso "manchado" con una pequeña cantidad de leche'),
('Macchiato Caramelo', 1, 38.00, 25, 8, 'Macchiato con caramelo y leche vaporizada'),
('Flat White', 1, 36.00, 30, 10, 'Café similar al latte pero con menos espuma'),
('Cortado', 1, 32.00, 35, 12, 'Espresso con una pequeña cantidad de leche caliente'),

-- Tés e infusiones (2)
('Té Negro', 2, 22.00, 40, 15, 'Té negro premium, fuerte y aromático'),
('Té Verde', 2, 24.00, 35, 12, 'Té verde japonés, ligero y refrescante'),
('Té de Hierbas', 2, 26.00, 30, 10, 'Infusión natural de hierbas seleccionadas'),
('Té Chai', 2, 35.00, 25, 8, 'Té negro con especias indias y leche'),
('Matcha Latte', 2, 45.00, 20, 6, 'Té verde matcha con leche vaporizada'),
('Té Earl Grey', 2, 28.00, 30, 10, 'Té negro con bergamota, clásico inglés'),

-- Bebidas Frías (3)
('Cold Brew', 3, 32.00, 30, 10, 'Café extraído en frío durante 24 horas, suave y dulce'),
('Iced Coffee', 3, 28.00, 35, 12, 'Café tradicional servido con hielo'),
('Iced Latte', 3, 38.00, 30, 10, 'Latte servido frío con hielo'),
('Iced Mocha', 3, 42.00, 25, 8, 'Mocha frío con crema batida'),
('Frappuccino Café', 3, 45.00, 30, 10, 'Bebida fría mezclada con café y crema'),
('Frappuccino Mocha', 3, 48.00, 25, 8, 'Frappuccino con chocolate y crema'),
('Frappuccino Caramelo', 3, 48.00, 25, 8, 'Frappuccino con caramelo y crema'),
('Smoothie Frutas del Bosque', 3, 42.00, 20, 8, 'Mezcla de frutas del bosque natural'),
('Smoothie Mango', 3, 40.00, 20, 8, 'Smoothie cremoso de mango'),
('Smoothie Verde', 3, 45.00, 15, 5, 'Smoothie saludable con frutas y vegetales'),
('Jugo de Naranja Natural', 3, 32.00, 30, 10, 'Jugo exprimido al momento'),
('Jugo Verde', 3, 35.00, 25, 8, 'Jugo de vegetales y frutas frescas'),
('Licuado de Plátano', 3, 38.00, 20, 8, 'Licuado cremoso de plátano con leche'),
('Licuado de Fresa', 3, 40.00, 20, 8, 'Licuado de fresa natural'),

-- Bebidas Especiales (4)
('Pumpkin Spice Latte', 4, 48.00, 15, 5, 'Latte con sabor a calabaza y especias'),
('Eggnog Latte', 4, 52.00, 12, 4, 'Latte tradicional navideño'),
('Peppermint Mocha', 4, 46.00, 18, 6, 'Mocha con sabor a menta'),
('Té Matcha Frío', 4, 40.00, 20, 6, 'Té matcha servido frío con hielo'),
('Golden Milk', 4, 38.00, 15, 5, 'Bebida ayurvédica con cúrcuma y especias'),
('Chai Latte Helado', 4, 42.00, 18, 6, 'Chai latte servido frío con hielo'),

-- Panadería (5)
('Croissant', 5, 25.00, 30, 10, 'Croissant francés hojaldrado, mantequilloso y dorado'),
('Croissant de Almendra', 5, 32.00, 20, 8, 'Croissant relleno de crema de almendra'),
('Croissant de Chocolate', 5, 30.00, 25, 8, 'Croissant con barra de chocolate belga'),
('Pain au Chocolat', 5, 28.00, 25, 8, 'Masa hojaldrada con chocolate'),
('Muffin Arándano', 5, 22.00, 25, 10, 'Muffin esponjoso con arándanos frescos'),
('Muffin Chocolate', 5, 24.00, 25, 10, 'Muffin con chispas de chocolate'),
('Muffin Plátano', 5, 22.00, 25, 10, 'Muffin húmedo de plátano'),
('Muffin Zanahoria', 5, 24.00, 20, 8, 'Muffin de zanahoria con nueces'),
('Bagel', 5, 20.00, 30, 12, 'Pan en forma de rosca, tradicional judío'),
('Bagel de Queso', 5, 25.00, 20, 8, 'Bagel cubierto con queso crema'),
('Donut Glaseado', 5, 18.00, 35, 15, 'Donut clásico con glaseado de azúcar'),
('Donut de Chocolate', 5, 22.00, 30, 12, 'Donut cubierto con chocolate'),
('Donut de Fresa', 5, 22.00, 30, 12, 'Donut con glaseado de fresa'),
('Donut Boston Cream', 5, 25.00, 25, 10, 'Donut relleno de crema y chocolate'),
('Scone', 5, 20.00, 25, 10, 'Pan dulce inglés, perfecto con té'),
('Scone de Arándano', 5, 22.00, 20, 8, 'Scone con arándanos secos'),
('Danés de Queso', 5, 28.00, 20, 8, 'Danés relleno de queso crema'),
('Danés de Frutas', 5, 26.00, 20, 8, 'Danés con frutas confitadas'),
('Palmerita', 5, 15.00, 40, 15, 'Masa hojaldrada con azúcar'),
('Palmerita de Chocolate', 5, 18.00, 30, 12, 'Palmerita con chocolate'),

-- Postres (6)
('Tarta de Queso', 6, 35.00, 15, 6, 'Tarta de queso crema con base de galleta'),
('Tarta de Queso de Fresa', 6, 38.00, 12, 4, 'Tarta de queso con topping de fresa'),
('Tarta de Chocolate', 6, 40.00, 10, 4, 'Tarta de chocolate negro intenso'),
('Tarta de Limón', 6, 36.00, 12, 4, 'Tarta ácida de limón con merengue'),
('Tarta de Manzana', 6, 34.00, 15, 5, 'Tarta tradicional de manzana'),
('Brownie', 6, 25.00, 25, 10, 'Brownie de chocolate denso y rico'),
('Brownie de Nuez', 6, 28.00, 20, 8, 'Brownie con nueces caramelizadas'),
('Blondie', 6, 24.00, 20, 8, 'Brownie de vainilla con chispas de chocolate'),
('Cookie de Chocolate', 6, 15.00, 40, 15, 'Galleta grande con chispas de chocolate'),
('Cookie de Avena', 6, 18.00, 35, 12, 'Galleta de avena con pasas'),
('Cookie de Mantequilla', 6, 12.00, 50, 20, 'Galleta clásica de mantequilla'),
('Macarons', 6, 8.00, 30, 12, 'Macarons franceses (por pieza)'),
('Cupcake de Vainilla', 6, 22.00, 20, 8, 'Cupcake de vainilla con buttercream'),
('Cupcake de Chocolate', 6, 24.00, 20, 8, 'Cupcake de chocolate con ganache'),
('Cupcake Red Velvet', 6, 26.00, 15, 6, 'Cupcake red velvet con cream cheese'),
('Cheesecake de Frutas', 6, 42.00, 10, 4, 'Cheesecake con topping de frutas'),
('Tiramisú', 6, 38.00, 12, 4, 'Postre italiano con café y mascarpone'),
('Profiteroles', 6, 32.00, 15, 5, 'Bolitas de choux rellenas de crema'),
('Éclairs', 6, 28.00, 18, 6, 'Éclairs de chocolate o vainilla'),
('Tarta de Frutas', 6, 40.00, 8, 3, 'Tarta fresca con frutas de temporada'),

-- Comida (7)
('Sándwich de Jamón y Queso', 7, 45.00, 20, 8, 'Clásico sándwich de jamón y queso'),
('Sándwich de Pavo', 7, 48.00, 18, 6, 'Sándwich de pavo con verduras'),
('Sándwich de Pollo', 7, 50.00, 18, 6, 'Sándwich de pollo grillado'),
('Sándwich de Atún', 7, 46.00, 15, 5, 'Sándwich de atún con mayonesa'),
('Sándwich Veggie', 7, 42.00, 15, 5, 'Sándwich vegetariano con verduras frescas'),
('Wrap de Pollo', 7, 52.00, 15, 5, 'Tortilla rellena de pollo y vegetales'),
('Wrap de Pavo', 7, 50.00, 15, 5, 'Wrap de pavo con verduras'),
('Wrap Veggie', 7, 46.00, 12, 4, 'Wrap vegetariano con hummus'),
('Croissant de Jamón y Queso', 7, 35.00, 15, 6, 'Croissant relleno de jamón y queso'),
('Panini de Pollo', 7, 55.00, 12, 4, 'Panini grillado de pollo'),
('Panini de Vegetales', 7, 48.00, 10, 4, 'Panini de vegetales asados'),
('Ensalada César', 7, 58.00, 12, 4, 'Ensalada con pollo, lechuga romana y aderezo césar'),
('Ensalada Griega', 7, 52.00, 10, 4, 'Ensalada con queso feta y aceitunas'),
('Ensalada de Pollo', 7, 55.00, 12, 4, 'Ensalada con pechuga de pollo grillada'),
('Sopa del Día', 7, 35.00, 15, 5, 'Sopa casera del día'),
('Quiche de Verduras', 7, 38.00, 10, 4, 'Quiche casero de verduras'),
('Quiche de Queso', 7, 40.00, 10, 4, 'Quiche de queso y huevo'),
('Empanada de Pollo', 7, 25.00, 20, 8, 'Empanada argentina de pollo'),
('Empanada de Carne', 7, 28.00, 18, 6, 'Empanada argentina de carne'),
('Empanada de Queso', 7, 22.00, 20, 8, 'Empanada de queso y cebolla');

-- 16. CLIENTES DE EJEMPLO -----------------------------------
INSERT INTO clientes (nombre, email, telefono) VALUES
('Juan Pérez García', 'juan.perez@email.com', '555-1234'),
('María Fernández López', 'maria.fernandez@email.com', '555-5678'),
('Carlos Rodríguez Martínez', 'carlos.rodriguez@email.com', '555-9012'),
('Ana González Sánchez', 'ana.gonzalez@email.com', '555-3456'),
('Luis Martínez Díaz', 'luis.martinez@email.com', '555-7890'),
('Sofía López Hernández', 'sofia.lopez@email.com', '555-2345'),
('Diego Sánchez Ramírez', 'diego.sanchez@email.com', '555-6789'),
('Valentina Torres Flores', 'valentina.torres@email.com', '555-0123'),
('Andrés Castro Morales', 'andres.castro@email.com', '555-4567'),
('Lucía Méndez Vargas', 'lucia.mendez@email.com', '555-8901'),
('Manuel Silva Rojas', 'manuel.silva@email.com', '555-2468'),
('Carmen Delgado Cruz', 'carmen.delgado@email.com', '555-1357'),
('Roberto Herrera Guzmán', 'roberto.herrera@email.com', '555-9876'),
('Patricia Mendoza Reyes', 'patricia.mendoza@email.com', '555-5432'),
('Fernando Aguilar Campos', 'fernando.aguilar@email.com', '555-8765');

-- 17. PROVEEDORES DE EJEMPLO --------------------------------
INSERT INTO proveedores (nombre, email, telefono, direccion) VALUES
('Café Suppliers Inc.', 'info@cafesuppliers.com', '555-1111', 'Calle Café 123, Ciudad'),
('Panadería Fresh', 'contact@panfresh.com', '555-2222', 'Avenida Pan 456, Pueblo'),
('Frutas Orgánicas', 'sales@frutasorg.com', '555-3333', 'Ruta Fruta 789, Villa'),
('Lácteos Premium', 'info@lacteosprem.com', '555-4444', 'Camino Leche 101, Aldea'),
('Especias Global', 'contact@especiasglobal.com', '555-5555', 'Plaza Especia 202, Metrópoli');

-- 18. CONFIGURACIÓN GENERAL ---------------------------------
INSERT INTO configuracion (clave, valor, descripcion) VALUES
('stock_minimo_default', '10', 'Stock mínimo predeterminado para nuevos productos'),
('tema_actual', 'claro', 'Tema actual de la aplicación'),
('iva_porcentaje', '16', 'Porcentaje de IVA para ventas'),
('moneda', 'PEN', 'Moneda para precios'),
('nombre_cafeteria', 'Nexus Coffee', 'Nombre de la cafetería'),
('direccion_cafeteria', 'Cafetería Moderna', 'Dirección de la cafetería'),
('telefono_cafeteria', '555-CAFE', 'Teléfono de contacto'),
('email_cafeteria', 'contacto@nexus-coffee.com', 'Email de contacto');

-- 19. ENTRADAS DE INVENTARIO -------------------------------
INSERT INTO entradas_inventario (producto_id, proveedor_id, cantidad, costo, usuario_id) VALUES
(1, 1, 100, 1000.00, 4),
(41, 2, 50, 500.00, 4),
(22, 1, 80, 800.00, 5),
(61, 3, 30, 300.00, 5),
(81, 4, 40, 400.00, 4);

-- 20. VENTAS DE EJEMPLO -------------------------------------
INSERT INTO ventas (cliente_id, total, fecha, usuario_id) VALUES
(1, 125.50, DATE_SUB(NOW(), INTERVAL 1 DAY), 2),
(2, 89.75, DATE_SUB(NOW(), INTERVAL 1 DAY), 2),
(3, 156.25, DATE_SUB(NOW(), INTERVAL 2 DAY), 3),
(4, 78.90, DATE_SUB(NOW(), INTERVAL 2 DAY), 3),
(5, 203.45, DATE_SUB(NOW(), INTERVAL 3 DAY), 2),
(6, 95.30, DATE_SUB(NOW(), INTERVAL 3 DAY), 2),
(7, 67.80, DATE_SUB(NOW(), INTERVAL 4 DAY), 3),
(8, 142.60, DATE_SUB(NOW(), INTERVAL 4 DAY), 3),
(9, 88.45, DATE_SUB(NOW(), INTERVAL 5 DAY), 2),
(10, 112.75, DATE_SUB(NOW(), INTERVAL 5 DAY), 2),
(11, 134.20, DATE_SUB(NOW(), INTERVAL 6 DAY), 3),
(12, 76.35, DATE_SUB(NOW(), INTERVAL 6 DAY), 3),
(13, 167.90, DATE_SUB(NOW(), INTERVAL 7 DAY), 2),
(14, 93.25, DATE_SUB(NOW(), INTERVAL 7 DAY), 2),
(15, 145.80, DATE_SUB(NOW(), INTERVAL 8 DAY), 3);

-- 21. DETALLES DE VENTA (CORREGIDOS: solo IDs 1-80) --------
INSERT INTO detalles_venta (venta_id, producto_id, cantidad, precio_unitario, subtotal) VALUES
(1, 1, 2, 22.00, 44.00), 
(1, 7, 1, 38.00, 38.00), 
(1, 61, 1, 35.00, 35.00), 
(1, 69, 1, 12.00, 12.00),
(2, 5, 1, 35.00, 35.00), 
(2, 9, 1, 42.00, 42.00), 
(2, 69, 1, 12.00, 12.00),
(3, 6, 1, 38.00, 38.00), 
(3, 10, 1, 40.00, 40.00), 
(3, 21, 1, 28.00, 28.00), 
(3, 25, 1, 45.00, 45.00), 
(3, 68, 1, 15.00, 15.00),
(4, 4, 1, 32.00, 32.00), 
(4, 14, 1, 36.00, 36.00), 
(4, 55, 1, 20.00, 20.00), 
(4, 41, 1, 25.00, 25.00),
(5, 1, 3, 22.00, 66.00), 
(5, 22, 2, 32.00, 64.00), 
(5, 41, 1, 25.00, 25.00), 
(5, 61, 1, 35.00, 35.00), 
(5, 1, 1, 22.00, 22.00),
(6, 2, 1, 28.00, 28.00), 
(6, 23, 1, 28.00, 28.00), 
(6, 42, 1, 32.00, 32.00), 
(6, 62, 1, 38.00, 38.00),
(7, 3, 2, 25.00, 50.00), 
(7, 24, 1, 38.00, 38.00),
(8, 8, 2, 42.00, 84.00), 
(8, 43, 1, 30.00, 30.00),
(9, 11, 1, 42.00, 42.00), 
(9, 44, 2, 28.00, 56.00),
(10, 12, 1, 30.00, 30.00), 
(10, 45, 1, 22.00, 22.00), 
(10, 64, 1, 36.00, 36.00),
(11, 13, 2, 38.00, 76.00), 
(11, 46, 1, 24.00, 24.00),
(12, 15, 1, 32.00, 32.00), 
(12, 47, 1, 22.00, 22.00),
(13, 16, 3, 22.00, 66.00), 
(13, 48, 1, 24.00, 24.00),
(14, 17, 1, 24.00, 24.00), 
(14, 49, 1, 20.00, 20.00),
(15, 18, 1, 26.00, 26.00), 
(15, 50, 2, 25.00, 50.00);

-- 22. VISTAS ÚTILES -----------------------------------------
CREATE OR REPLACE VIEW reporte_ventas AS
SELECT v.id, c.nombre AS cliente, v.total, v.fecha, u.nombre AS usuario, COUNT(dv.id) AS num_productos
FROM ventas v
LEFT JOIN clientes c ON v.cliente_id = c.id
LEFT JOIN usuarios u ON v.usuario_id = u.id
LEFT JOIN detalles_venta dv ON v.id = dv.venta_id
GROUP BY v.id;

CREATE OR REPLACE VIEW productos_stock_bajo AS
SELECT p.*, cat.nombre AS categoria, ROUND((p.stock / p.stock_minimo * 100), 2) AS porcentaje_stock
FROM productos p
JOIN categorias cat ON p.categoria_id = cat.id
WHERE p.stock <= p.stock_minimo;

CREATE OR REPLACE VIEW ventas_por_categoria AS
SELECT cat.nombre AS categoria, SUM(dv.subtotal) AS total_ventas, SUM(dv.cantidad) AS cantidad_vendida, COUNT(DISTINCT dv.venta_id) AS num_ventas
FROM detalles_venta dv
JOIN productos p ON dv.producto_id = p.id
JOIN categorias cat ON p.categoria_id = cat.id
GROUP BY cat.nombre;



-- 23. RESUMEN EJECUTIVO -------------------------------------
SELECT 'Base de datos Nexus Coffee creada exitosamente' AS mensaje;
SELECT 'Categorías agregadas: ' AS info, COUNT(*) AS total FROM categorias;
SELECT 'Productos agregados: ' AS info, COUNT(*) AS total FROM productos;
SELECT 'Clientes agregados: ' AS info, COUNT(*) AS total FROM clientes;
SELECT 'Ventas agregadas: ' AS info, COUNT(*) AS total FROM ventas;
SELECT 'Usuarios agregados: ' AS info, COUNT(*) AS total FROM usuarios;
SELECT 'Proveedores agregados: ' AS info, COUNT(*) AS total FROM proveedores;
SELECT 'Entradas de inventario agregadas: ' AS info, COUNT(*) AS total FROM entradas_inventario;
SELECT 'Ejemplos de productos:' AS info;
SELECT p.nombre, cat.nombre AS categoria, p.precio, p.stock FROM productos p JOIN categorias cat ON p.categoria_id = cat.id LIMIT 5;

-- ==========================================================
-- FIN DEL ARCHIVO – IMPORTA ESTE SQL COMPLETO
-- ==========================================================