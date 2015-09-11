CREATE DATABASE IF NOT EXISTS `flask_restless`
    DEFAULT CHARACTER SET utf8
    DEFAULT COLLATE utf8_general_ci;

USE flask_restless;

CREATE TABLE IF NOT EXISTS `person`(
    `id` INT NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(32) NOT NULL,
    `birth_date` DATE,
    `computers` INT,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `computer`(
    `id` INT NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(32) NOT NULL DEFAULT '',
    `vendor` VARCHAR(32),
    `purchase_time` DATETIME,
    `owner_id` INT,
    PRIMARY KEY (`id`),
    CONSTRAINT `owner_id_` FOREIGN KEY(`owner_id`) REFERENCES `person`(`id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

ALTER TABLE `person` ADD CONSTRAINT `computers_`
FOREIGN KEY(`computers`) REFERENCES `computer`(`id`);