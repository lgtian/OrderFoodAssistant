CREATE TABLE `orderassistant`.`activity_info` (
  `activityId` INT NOT NULL AUTO_INCREMENT,
  `activityType` NVARCHAR(45) NULL,
  `activitySubType` NVARCHAR(45) NULL,
  `group` NVARCHAR(45) NULL,
  `date` date NULL,
  `expiredAt` DATETIME NULL,
  `createdBy` NVARCHAR(45) NULL,
  `createdAt` DATETIME NULL,
  `updatedAt` DATETIME NULL,

  PRIMARY KEY (`activityId`),
  UNIQUE INDEX uni_idx_group_date(`group`,`date`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8 COMMENT='活动表';
