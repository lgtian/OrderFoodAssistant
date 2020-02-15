CREATE TABLE `activity_info` (
  `activityId` INT NOT NULL AUTO_INCREMENT,
  `activityType` NVARCHAR(45) NULL,
  `activitySubType` NVARCHAR(45) NULL,
  `group` NVARCHAR(45) NULL,
  `date` date NULL,
  `expiredAt` DATETIME NULL,
  `createdBy` NVARCHAR(45) NULL,
  `createdAt` DATETIME NULL,
  `updatedAt` DATETIME NULL,

  PRIMARY KEY (`activityId`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8 COMMENT='活动表';

ALTER TABLE activity_info
ADD COLUMN mealDeliver nvarchar(20) null ;