SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS  `activity_detail`;
CREATE TABLE `activity_detail` (
  `activityDetailId` INT NOT NULL AUTO_INCREMENT,
  `activityId` NVARCHAR(32) NOT NULL,
  `employeeId` NVARCHAR(45) NOT NULL,
  `quantity` INT NULL,
  `createdBy` NVARCHAR(45) NULL,
  `createdAt` DATETIME NULL,
  `updatedBy` NVARCHAR(45) NULL,
  `updatedAt` DATETIME NULL,
  PRIMARY KEY (`activityDetailId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='活动明细表';

SET FOREIGN_KEY_CHECKS = 1;

