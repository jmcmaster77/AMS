-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Versión del servidor:         11.1.2-MariaDB - mariadb.org binary distribution
-- SO del servidor:              Win64
-- HeidiSQL Versión:             12.7.0.6850
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Volcando estructura de base de datos para ams
CREATE DATABASE IF NOT EXISTS `ams` /*!40100 DEFAULT CHARACTER SET latin1 COLLATE latin1_general_ci */;
USE `ams`;

-- Volcando estructura para tabla ams.clientes
CREATE TABLE IF NOT EXISTS `clientes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fullname` varchar(70) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci DEFAULT NULL,
  `tipod` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci DEFAULT NULL,
  `documento` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci DEFAULT NULL,
  `numero` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci DEFAULT NULL,
  `email` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci DEFAULT NULL,
  `direccion` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci DEFAULT NULL,
  `fecha` datetime DEFAULT NULL,
  `deleted` tinyint(2) DEFAULT NULL,
  `id_u` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_clientes_usuarios` (`id_u`),
  CONSTRAINT `FK_clientes_usuarios` FOREIGN KEY (`id_u`) REFERENCES `usuarios` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla ams.clientes: ~3 rows (aproximadamente)
INSERT INTO `clientes` (`id`, `fullname`, `tipod`, `documento`, `numero`, `email`, `direccion`, `fecha`, `deleted`, `id_u`) VALUES
	(1, 'Jorge Eloy Martin', 'C', '15332813', '04142993487', 'jmcmaster77@gmail.com', 'Calle real de Altavista casa #163', '2024-07-02 23:09:00', 0, 1),
	(2, 'Ailyn Perez', 'C', '15615860', '04242873596', 'ailynperez@gmail.com', ' Valles del tuy, cartanal sector 6 calle 4 casa 8  ', '2024-07-04 01:20:19', 0, 1),
	(3, 'Eunice Coraspe', 'C', '3805449', '04127333654', 'eunicecoraspe@gmail.com', 'Altavista calle real #163 apto 2 ', '2024-07-26 04:20:31', 0, 1);

-- Volcando estructura para tabla ams.compras
CREATE TABLE IF NOT EXISTS `compras` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_p` int(11) NOT NULL,
  `nfact` varchar(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_spanish_ci NOT NULL DEFAULT '',
  `fechaf` date NOT NULL,
  `productos` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `tcompra` varchar(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_spanish_ci NOT NULL,
  `mpago` varchar(15) CHARACTER SET utf8mb3 COLLATE utf8mb3_spanish_ci NOT NULL,
  `pagada` tinyint(4) NOT NULL DEFAULT 0,
  `totalc` float(10,2) NOT NULL DEFAULT 0.00,
  `fecha` datetime NOT NULL,
  `deleted` tinyint(4) NOT NULL DEFAULT 0,
  `id_u` int(11) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  KEY `FK_proveedor` (`id_p`),
  KEY `FK_usuario` (`id_u`),
  CONSTRAINT `FK_proveedor` FOREIGN KEY (`id_p`) REFERENCES `proveedores` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `FK_usuario` FOREIGN KEY (`id_u`) REFERENCES `usuarios` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla ams.compras: ~7 rows (aproximadamente)
INSERT INTO `compras` (`id`, `id_p`, `nfact`, `fechaf`, `productos`, `tcompra`, `mpago`, `pagada`, `totalc`, `fecha`, `deleted`, `id_u`) VALUES
	(1, 1, '1101', '2024-07-10', '{"productos": [{"id": 1, "nombre": "Spt 12 Morocho", "cantidad": 4, "costo": 25.0}, {"id": 2, "nombre": "Alicate de Electricista", "cantidad": 7, "costo": 4.35}, {"id": 3, "nombre": "Alicate de presion recto", "cantidad": 10, "costo": 4.0}]}', 'Credito', 'Otro', 1, 170.45, '2024-07-16 11:16:07', 0, 1),
	(2, 1, '1102', '2024-07-10', '{"productos": [{"id": 1, "nombre": "Spt 12 Morocho", "cantidad": 10, "costo": 25.0}, {"id": 2, "nombre": "Alicate de Electricista", "cantidad": 10, "costo": 4.45}, {"id": 3, "nombre": "Alicate de presion recto", "cantidad": 20, "costo": 7.0}, {"id": 4, "nombre": "Set Rachet 1/4 46 pzas", "cantidad": 10, "costo": 8.5}]}', 'Contado', 'Efectivo', 1, 519.50, '2024-07-16 22:33:53', 0, 1),
	(3, 3, '3301', '2024-07-10', '{"productos": [{"id": 4, "nombre": "Set Rachet 1/4 46 pzas", "cantidad": 10, "costo": 8.9}]}', 'Contado', 'Efectivo', 1, 89.00, '2024-07-17 01:09:32', 0, 1),
	(4, 2, 'GA1745', '2024-07-08', '{"productos": [{"id": 13, "nombre": "Grifo Lavaplatos Doble", "cantidad": 2, "costo": 7.0}]}', 'Contado', 'Efectivo', 1, 14.00, '2024-07-17 09:04:42', 0, 1),
	(5, 2, 'GA1757', '2024-07-09', '{"productos": [{"id": 14, "nombre": "Grifo Lavamanos 30cm", "cantidad": 10, "costo": 12.0}, {"id": 13, "nombre": "Grifo Lavaplatos Doble", "cantidad": 8, "costo": 7.0}, {"id": 5, "nombre": "Tornillos Drywall 6x1 p25", "cantidad": 20, "costo": 2.0}, {"id": 6, "nombre": "Tornillo No 10 combo p50", "cantidad": 50, "costo": 4.0}, {"id": 12, "nombre": "Pintura Mate Clase A Cu\\u00f1ete", "cantidad": 5, "costo": 25.0}, {"id": 11, "nombre": "Martillo de Bola Madera", "cantidad": 3, "costo": 5.0}, {"id": 10, "nombre": "Martillo Madera 16", "cantidad": 4, "costo": 5.0}, {"id": 9, "nombre": "Martillo Hoteche", "cantidad": 3, "costo": 6.0}, {"id": 8, "nombre": "Mazo de goma", "cantidad": 2, "costo": 6.0}, {"id": 7, "nombre": "Set Destornilladores 6p", "cantidad": 12, "costo": 5.5}]}', 'Contado', 'Efectivo', 1, 672.00, '2024-07-17 09:07:51', 0, 1),
	(7, 3, 'MR123', '2024-07-01', '{"productos": [{"id": 9, "nombre": "Martillo Hoteche", "cantidad": 3, "costo": 7.0}, {"id": 10, "nombre": "Martillo Madera 16", "cantidad": 3, "costo": 7.0}]}', 'Contado', 'Efectivo', 1, 42.00, '2024-07-23 04:37:35', 1, 1),
	(8, 3, 'MR127', '2024-07-11', '{"productos": [{"id": 9, "nombre": "Martillo Hoteche", "cantidad": 4, "costo": 7.5}, {"id": 10, "nombre": "Martillo Madera 16", "cantidad": 2, "costo": 6.8}]}', 'Contado', 'Efectivo', 1, 43.60, '2024-07-23 05:26:44', 1, 1);

-- Volcando estructura para tabla ams.presupuestos
CREATE TABLE IF NOT EXISTS `presupuestos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_c` int(11) DEFAULT NULL,
  `productos` longtext CHARACTER SET utf8mb3 COLLATE utf8mb3_spanish_ci DEFAULT NULL,
  `bolivares` tinyint(4) DEFAULT NULL,
  `totalp` float DEFAULT NULL,
  `fecha` datetime DEFAULT NULL,
  `deleted` tinyint(4) DEFAULT NULL,
  `id_u` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_client` (`id_c`),
  KEY `FK_users` (`id_u`),
  CONSTRAINT `FK_client` FOREIGN KEY (`id_c`) REFERENCES `clientes` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `FK_users` FOREIGN KEY (`id_u`) REFERENCES `usuarios` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla ams.presupuestos: ~4 rows (aproximadamente)
INSERT INTO `presupuestos` (`id`, `id_c`, `productos`, `bolivares`, `totalp`, `fecha`, `deleted`, `id_u`) VALUES
	(1, 1, '{"productos": [{"id": 1, "nombre": "Spt 12 Morocho", "cantidad": 1, "precio": 32.5}]}', 1, 1194.05, '2024-07-25 01:14:12', 0, 1),
	(2, 2, '{"productos": [{"id": 12, "nombre": "Pintura Mate Clase A Cu\\u00f1ete", "cantidad": 4, "precio": 32.5}, {"id": 6, "nombre": "Tornillo No 10 combo p50", "cantidad": 1, "precio": 5.2}]}', 0, 135.2, '2024-07-25 05:35:54', 0, 1),
	(3, 1, '{"productos": [{"id": 5, "nombre": "Tornillos Drywall 6x1 p25", "cantidad": 3, "precio": 2.5}, {"id": 9, "nombre": "Martillo Hoteche", "cantidad": 1, "precio": 9.1}, {"id": 11, "nombre": "Martillo de Bola Madera", "cantidad": 1, "precio": 6.5}, {"id": 2, "nombre": "Alicate de Electricista", "cantidad": 1, "precio": 5.54}, {"id": 3, "nombre": "Alicate de presion recto", "cantidad": 1, "precio": 8.05}, {"id": 8, "nombre": "Mazo de goma", "cantidad": 1, "precio": 9.1}]}', 1, 1682.32, '2024-07-25 01:33:17', 1, 1),
	(4, 3, '{"productos": [{"id": 2, "nombre": "Alicate de Electricista", "cantidad": 2, "precio": 5.54}, {"id": 3, "nombre": "Alicate de presion recto", "cantidad": 1, "precio": 8.05}, {"id": 5, "nombre": "Tornillos Drywall 6x1 p25", "cantidad": 2, "precio": 2.5}, {"id": 7, "nombre": "Set Destornilladores 6p", "cantidad": 2, "precio": 7.15}, {"id": 8, "nombre": "Mazo de goma", "cantidad": 2, "precio": 9.1}]}', 1, 2080.59, '2024-07-26 04:21:29', 0, 1);

-- Volcando estructura para tabla ams.productos
CREATE TABLE IF NOT EXISTS `productos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `codigo` varchar(40) NOT NULL,
  `nombre` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_spanish_ci NOT NULL,
  `cantidad` int(11) NOT NULL DEFAULT 0,
  `costo` float(10,2) NOT NULL DEFAULT 0.00,
  `porcentaje` float(4,2) NOT NULL DEFAULT 0.00,
  `precio` float(10,2) NOT NULL DEFAULT 0.00,
  `categoria` varchar(30) CHARACTER SET utf8mb3 COLLATE utf8mb3_spanish_ci NOT NULL,
  `descripcion` varchar(150) CHARACTER SET utf8mb3 COLLATE utf8mb3_spanish_ci NOT NULL DEFAULT '',
  `imagen` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_spanish_ci NOT NULL,
  `fecha` datetime NOT NULL,
  `deleted` tinyint(4) NOT NULL DEFAULT 0,
  `id_u` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FK__usuarios` (`id_u`),
  CONSTRAINT `FK__usuarios` FOREIGN KEY (`id_u`) REFERENCES `usuarios` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla ams.productos: ~14 rows (aproximadamente)
INSERT INTO `productos` (`id`, `codigo`, `nombre`, `cantidad`, `costo`, `porcentaje`, `precio`, `categoria`, `descripcion`, `imagen`, `fecha`, `deleted`, `id_u`) VALUES
	(1, '01', 'Spt 12 Morocho', 13, 25.00, 30.00, 32.50, 'Cables', 'Cable morocho blanco numero Spt 12 ', '01.webp', '2024-07-24 02:04:34', 0, 1),
	(2, '02', 'Alicate de Electricista', 15, 4.45, 24.59, 5.54, 'Herrameinta', 'Alicate para electricista marca total', '02.webp', '2024-07-09 03:06:25', 0, 1),
	(3, '04', 'Alicate de presion recto', 27, 7.00, 15.00, 8.05, 'Herrameinta', 'Alicate de presion profesional 10 pulgadas', '04.webp', '2024-07-12 00:11:27', 0, 1),
	(4, 'R014', 'Set Rachet 1/4 46 pzas', 20, 8.90, 20.00, 10.68, 'Herrameinta', 'Juego Set Rachet 1/4 Dados Milimétricos Destornillador 46 piezas', 'R014.webp', '2024-07-17 01:12:13', 0, 1),
	(5, 'TD05', 'Tornillos Drywall 6x1 p25', 12, 2.00, 25.00, 2.50, 'Tornillos', 'Tornillos Drywall 6x1 pack 25 ', 'TD05.webp', '2024-07-17 08:32:16', 0, 1),
	(6, 'TC017', 'Tornillo No 10 combo p50', 19, 4.00, 30.00, 5.20, 'Tornillos', 'Combo Tornillo Tirafondo No. 10 Con Ramplug 50 Piezas', 'TC017.webp', '2024-07-17 08:34:13', 0, 1),
	(7, 'D06', 'Set Destornilladores 6p', 1, 5.50, 30.00, 7.15, 'Herrameinta', 'Juego Destornilladores Total Tools 6 Piezas Punta Imantada', 'D06.webp', '2024-07-17 08:36:16', 0, 1),
	(8, 'M115', 'Mazo de goma', 0, 7.00, 30.00, 9.10, 'Herrameinta', 'Mazo De Goma 225g / 8oz Tolsen', 'M115.webp', '2024-07-17 08:37:23', 0, 1),
	(9, 'M745', 'Martillo Hoteche', 6, 7.00, 30.00, 9.10, 'Herrameinta', 'Martillo Mango De Fibra 16oz Hoteche', 'M745.webp', '2024-07-17 08:38:20', 0, 1),
	(10, 'M744', 'Martillo Madera 16', 6, 7.00, 30.00, 9.10, 'Herrameinta', 'Martillo Forge Mango De Madera 16 Oz', 'M744.webp', '2024-07-17 08:39:36', 0, 1),
	(11, 'M375', 'Martillo de Bola Madera', 2, 5.00, 30.00, 6.50, 'Herrameinta', 'Martillo De Bola Cabo Madera 16 Onzas 54-191 Stanley', 'M375.webp', '2024-07-17 08:41:06', 0, 1),
	(12, 'P748', 'Pintura Mate Clase A Cuñete', 5, 25.00, 30.00, 32.50, 'Pinturas', 'Pintura Blanco Mate Clase A Maxigama Lavable Cuñete', 'P748.webp', '2024-07-17 08:47:20', 0, 1),
	(13, 'G74', 'Grifo Lavaplatos Doble', 10, 7.00, 30.00, 9.10, 'Griferia', 'Llave Grifo Lavaplatos Doble Cromada Cuerpo Bronce Tienda', 'G74.webp', '2024-07-17 08:49:44', 0, 1),
	(14, 'G235', 'Grifo Lavamanos 30cm', 10, 12.00, 30.00, 15.60, 'Griferia', 'Griferia De Lavamanos Satinada Alta 30cm En Acero Inoxidable', 'G235.webp', '2024-07-17 08:50:48', 0, 1);

-- Volcando estructura para tabla ams.proveedores
CREATE TABLE IF NOT EXISTS `proveedores` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fullname` varchar(70) CHARACTER SET latin1 COLLATE latin1_spanish_ci DEFAULT NULL,
  `tipod` varchar(5) CHARACTER SET latin1 COLLATE latin1_spanish_ci DEFAULT NULL,
  `documento` varchar(20) CHARACTER SET latin1 COLLATE latin1_spanish_ci DEFAULT NULL,
  `numero` varchar(20) CHARACTER SET latin1 COLLATE latin1_spanish_ci DEFAULT NULL,
  `email` varchar(50) CHARACTER SET latin1 COLLATE latin1_spanish_ci DEFAULT NULL,
  `direccion` varchar(200) CHARACTER SET latin1 COLLATE latin1_spanish_ci DEFAULT NULL,
  `fecha` datetime DEFAULT NULL,
  `deleted` tinyint(2) DEFAULT NULL,
  `id_u` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  KEY `FK_clientes_usuarios` (`id_u`) USING BTREE,
  CONSTRAINT `proveedores_ibfk_1` FOREIGN KEY (`id_u`) REFERENCES `usuarios` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC;

-- Volcando datos para la tabla ams.proveedores: ~3 rows (aproximadamente)
INSERT INTO `proveedores` (`id`, `fullname`, `tipod`, `documento`, `numero`, `email`, `direccion`, `fecha`, `deleted`, `id_u`) VALUES
	(1, 'Materiales Eléctricos JMC', 'R', 'J025478569', '02124758596', 'ventas@jmc.net', 'Municipio Libertador Av Lecuna', '2024-07-03 00:48:30', 0, 1),
	(2, 'Grifería Agüita', 'R', 'J405142526', '04242873596', 'lilap@aguita.com', 'Carretera Regional, sector xyz, parcela jupiter, galpon radamantis', '2024-07-03 00:51:45', 0, 1),
	(3, 'Metales Ricos', 'R', 'J205748569', '02125758585', 'ventas@metalesricos.com', 'en el muy muy lejano', '2024-07-04 01:21:15', 0, 1);

-- Volcando estructura para tabla ams.reversos
CREATE TABLE IF NOT EXISTS `reversos` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `id_t` int(11) DEFAULT 0,
  `id_p` int(11) NOT NULL DEFAULT 0,
  `cantidad` int(11) NOT NULL DEFAULT 0,
  `costo` float(10,2) NOT NULL DEFAULT 0.00,
  `precio` float(10,2) NOT NULL DEFAULT 0.00,
  `transaccion` varchar(15) NOT NULL,
  `fecha` datetime NOT NULL,
  `id_u` int(11) NOT NULL DEFAULT 0,
  `registrando` tinyint(4) NOT NULL,
  `reversado` tinyint(4) NOT NULL,
  PRIMARY KEY (`Id`),
  KEY `FK_user` (`id_u`),
  KEY `FK_productos` (`id_p`),
  CONSTRAINT `FK_productos` FOREIGN KEY (`id_p`) REFERENCES `productos` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `FK_user` FOREIGN KEY (`id_u`) REFERENCES `usuarios` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla ams.reversos: ~16 rows (aproximadamente)
INSERT INTO `reversos` (`Id`, `id_t`, `id_p`, `cantidad`, `costo`, `precio`, `transaccion`, `fecha`, `id_u`, `registrando`, `reversado`) VALUES
	(13, 1, 1, 14, 0.00, 0.00, 'venta', '2024-07-24 03:06:00', 1, 0, 0),
	(14, 2, 3, 30, 0.00, 0.00, 'venta', '2024-07-24 03:07:05', 1, 0, 0),
	(15, 2, 3, 29, 0.00, 0.00, 'venta', '2024-07-24 03:07:34', 1, 0, 0),
	(16, 2, 2, 17, 0.00, 0.00, 'compra', '2024-07-24 03:07:34', 1, 0, 0),
	(17, 3, 8, 4, 0.00, 0.00, 'venta', '2024-07-24 03:09:39', 1, 0, 0),
	(18, 3, 7, 12, 0.00, 0.00, 'compra', '2024-07-24 03:09:39', 1, 0, 0),
	(19, 3, 5, 20, 0.00, 0.00, 'compra', '2024-07-24 03:09:39', 1, 0, 0),
	(20, 4, 6, 50, 0.00, 0.00, 'venta', '2024-07-24 03:36:05', 1, 0, 0),
	(21, 5, 6, 46, 0.00, 0.00, 'venta', '2024-07-24 03:40:23', 1, 0, 0),
	(29, 6, 5, 17, 0.00, 0.00, 'venta', '2024-07-24 22:56:37', 1, 0, 0),
	(31, 8, 5, 15, 0.00, 0.00, 'venta', '2024-07-28 20:47:02', 1, 0, 0),
	(32, 8, 9, 7, 0.00, 0.00, 'compra', '2024-07-28 20:47:02', 1, 0, 0),
	(33, 8, 11, 3, 0.00, 0.00, 'compra', '2024-07-28 20:47:02', 1, 0, 0),
	(34, 8, 2, 16, 0.00, 0.00, 'compra', '2024-07-28 20:47:02', 1, 0, 0),
	(35, 8, 3, 28, 0.00, 0.00, 'compra', '2024-07-28 20:47:02', 1, 0, 0),
	(36, 8, 8, 1, 0.00, 0.00, 'compra', '2024-07-28 20:47:02', 1, 0, 0),
	(37, 9, 10, 7, 0.00, 0.00, 'venta', '2024-08-04 01:20:58', 1, 0, 0);

-- Volcando estructura para tabla ams.tasa
CREATE TABLE IF NOT EXISTS `tasa` (
  `id` tinyint(4) NOT NULL AUTO_INCREMENT,
  `valor` float(4,2) NOT NULL DEFAULT 0.00,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla ams.tasa: ~0 rows (aproximadamente)
INSERT INTO `tasa` (`id`, `valor`) VALUES
	(1, 37.77);

-- Volcando estructura para tabla ams.usuarios
CREATE TABLE IF NOT EXISTS `usuarios` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(20) DEFAULT NULL,
  `password` varchar(240) DEFAULT NULL,
  `fullname` varchar(70) DEFAULT NULL,
  `rol` tinyint(4) DEFAULT NULL,
  `fecha` datetime DEFAULT NULL,
  `deleted` tinyint(2) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla ams.usuarios: ~9 rows (aproximadamente)
INSERT INTO `usuarios` (`id`, `username`, `password`, `fullname`, `rol`, `fecha`, `deleted`) VALUES
	(1, 'jorgem', 'scrypt:32768:8:1$tDpKXZOT509GAmKj$000b7896646b110099205c62094aa07c94fd570595201c5844e09438a18ec740e443f7117ce4e13faeba78dcceec549ef781d3bd0bbed075167c575c5d6af5c1', 'Jorge Martin', 0, '2024-06-19 22:11:52', 0),
	(2, 'jorgeu', 'scrypt:32768:8:1$58Ysh1k2OOner559$0915cf48cec6db4f44b78459b3e1db3f2dbdc130001f27b048d4de3a54cd9f559082f5cfd2204b30ae607bfde546f2cc8ea31832d750926ad198ace7487e0e47', 'Jorge Martin', 1, '2024-06-19 19:24:02', 0),
	(3, 'pepe', 'scrypt:32768:8:1$WWUZfZar6vWFRa6p$5b134e9fba21a2f672fb2e78731b5adf4af50d0ffbe99eab8283f75c40f021086ec0c72bf415ad6803fff7beb48b8fb218cd97265cfb6c1ccec26be2e1ba5b36', 'Pepe Grillo', 1, '2024-06-24 12:31:47', 0),
	(4, 'eloym', 'scrypt:32768:8:1$xZM1awuv9YwxyJcQ$680a3a3f43fa3cc407b4cea2ba6f48770789c295038913940699be589ab4744e55e1318d5096bb01be9d4df1eb099b49fbdf254548a884cfb3ffff1698f5b980', 'Eloy Coraspe', 0, '2024-06-19 19:24:04', 0),
	(5, 'aperez', 'scrypt:32768:8:1$kK0TKdF31vpHBejv$2651631df02ffdc04a957efa22dd921ac27d3eaef9e8fb7317fd7f0d3a008ed8c3d556eb41d090a0566dd89d38bbaeb42c611cead7e47c29130f427f3f58ad72', 'Ailyn Perez', 0, '2024-06-19 19:24:15', 0),
	(6, 'onep', 'scrypt:32768:8:1$VSePypTmnn6SliLn$30aae93d274aabd6d467313b1ac7ce87a1b2a2095e0b8d239c9b26ce88b91ae53f37f16478259e7b6874ebd5b8c494db89a9fb6556d77f35ab2dde15ace739d6', 'One One', 0, '2024-06-20 21:14:37', 0),
	(7, 'doce', 'scrypt:32768:8:1$wcevCOa3snqHSM0T$5b11075538d88536234acd81d4be65309ed0dc1bfd477757a1ec511f75edacfc48e98343016c7c24997be75965ce0523c5f726d1a696743e7f67d78c2c5f385d', 'doce doce', 1, '2024-06-19 19:24:17', 0),
	(8, 'ocho', 'scrypt:32768:8:1$nMp2B2BNvN30VJLd$ce5afba3b9228c9bc777df21e57e6a4ecf5b93ec2264b9d64b1890520dad0a57a257dc33eed172bc3ec08e0d07ae17a922bb02ef0bc07a04848c888418680984', 'ocho ocho', 1, '2024-06-19 22:27:56', 1),
	(10, 'batman', 'scrypt:32768:8:1$X5QvC02u2lgTFNDB$dd011a8d91d8837acacad462a17ae740cae325252125ff756853eed4def87bb39d1056241b76c6b052b07da8be4885d818789a01590a4fddbda4b79c8d94c04e', 'Bruno Diaz', 1, '2024-06-19 21:52:49', 0);

-- Volcando estructura para tabla ams.ventas
CREATE TABLE IF NOT EXISTS `ventas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_c` int(11) NOT NULL,
  `productos` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci NOT NULL,
  `tventa` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci NOT NULL,
  `mpago` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci NOT NULL,
  `bolivares` tinyint(4) NOT NULL,
  `totalv` float(10,2) NOT NULL,
  `fecha` datetime NOT NULL,
  `deleted` tinyint(4) NOT NULL,
  `id_u` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_clientes` (`id_c`),
  KEY `FK_usuarios` (`id_u`),
  CONSTRAINT `FK_clientes` FOREIGN KEY (`id_c`) REFERENCES `clientes` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `FK_usuarios` FOREIGN KEY (`id_u`) REFERENCES `usuarios` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla ams.ventas: ~9 rows (aproximadamente)
INSERT INTO `ventas` (`id`, `id_c`, `productos`, `tventa`, `mpago`, `bolivares`, `totalv`, `fecha`, `deleted`, `id_u`) VALUES
	(1, 1, '{"productos": [{"id": 1, "nombre": "Spt 12 Morocho", "cantidad": 1, "precio": 32.5}]}', 'Contado', 'Efectivo', 1, 1194.05, '2024-07-24 03:06:00', 0, 1),
	(2, 1, '{"productos": [{"id": 3, "nombre": "Alicate de presion recto", "cantidad": 1, "precio": 8.05}, {"id": 2, "nombre": "Alicate de Electricista", "cantidad": 1, "precio": 5.54}]}', 'Contado', 'Efectivo', 1, 499.30, '2024-07-24 03:07:34', 0, 1),
	(3, 2, '{"productos": [{"id": 8, "nombre": "Mazo de goma", "cantidad": 2, "precio": 9.1}, {"id": 7, "nombre": "Set Destornilladores 6p", "cantidad": 1, "precio": 7.15}, {"id": 5, "nombre": "Tornillos Drywall 6x1 p25", "cantidad": 1, "precio": 2.5}]}', 'Credito', 'Tarjeta', 1, 1023.21, '2024-07-24 03:09:39', 0, 1),
	(4, 2, '{"productos": [{"id": 6, "nombre": "Tornillo No 10 combo p50", "cantidad": 4, "precio": 5.2}]}', 'Contado', 'Efectivo', 0, 20.80, '2024-07-24 03:36:05', 0, 1),
	(5, 1, '{"productos": [{"id": 6, "nombre": "Tornillo No 10 combo p50", "cantidad": 1, "precio": 5.2}]}', 'Contado', 'Efectivo', 1, 191.05, '2024-07-24 03:40:23', 0, 1),
	(6, 1, '{"productos": [{"id": 5, "nombre": "Tornillos Drywall 6x1 p25", "cantidad": 2, "precio": 2.5}]}', 'Contado', 'Transferencia', 1, 183.70, '2024-07-24 22:56:37', 0, 1),
	(7, 2, '{"productos": [{"id": 14, "nombre": "Grifo Lavamanos 30cm", "cantidad": 1, "precio": 15.6}]}', 'Credito', 'Otro', 1, 573.14, '2024-07-24 23:02:40', 1, 1),
	(8, 1, '{"productos": [{"id": 5, "nombre": "Tornillos Drywall 6x1 p25", "cantidad": 3, "precio": 2.5}, {"id": 9, "nombre": "Martillo Hoteche", "cantidad": 1, "precio": 9.1}, {"id": 11, "nombre": "Martillo de Bola Madera", "cantidad": 1, "precio": 6.5}, {"id": 2, "nombre": "Alicate de Electricista", "cantidad": 1, "precio": 5.54}, {"id": 3, "nombre": "Alicate de presion recto", "cantidad": 1, "precio": 8.05}, {"id": 8, "nombre": "Mazo de goma", "cantidad": 1, "precio": 9.1}]}', 'Contado', 'Efectivo', 1, 1682.32, '2024-07-28 20:47:02', 0, 1),
	(9, 3, '{"productos": [{"id": 10, "nombre": "Martillo Madera 16", "cantidad": 1, "precio": 9.1}]}', 'Contado', 'Efectivo', 1, 343.71, '2024-08-04 01:20:58', 0, 1);

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
