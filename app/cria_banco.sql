SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

CREATE DATABASE `jogoteca` /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_bin */;
USE `jogoteca`;

CREATE TABLE `jogo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(50) COLLATE utf8_bin NOT NULL,
  `categoria` varchar(40) COLLATE utf8_bin NOT NULL,
  `console` varchar(20) NOT NULL,
  `usuario_id` varchar(8) COLLATE utf8_bin,
  PRIMARY KEY (`id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `jogo_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;


CREATE TABLE `usuario` (
  `id` varchar(8) COLLATE utf8_bin NOT NULL,
  `nome` varchar(20) COLLATE utf8_bin NOT NULL,
  `senha` varchar(8) COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;