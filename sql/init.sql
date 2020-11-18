CREATE SCHEMA nonogram ;

CREATE TABLE nonogram.nonograms (
  `id` INT NOT NULL AUTO_INCREMENT,
  `json` VARCHAR(1024) NOT NULL DEFAULT '',
  `name` VARCHAR(45) NOT NULL DEFAULT '',
  `user_id` INT NOT NULL DEFAULT 1,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE);

ALTER TABLE nonogram.nonograms 
ADD COLUMN `width` INT NOT NULL AFTER `user_id`,
ADD COLUMN `height` INT NOT NULL AFTER `width`;
