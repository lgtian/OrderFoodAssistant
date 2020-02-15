SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS  `product_info`;
CREATE TABLE `product_info` (
  `productId` BIGINT(20) NOT NULL,
  `productType` NVARCHAR(20) NULL,
  `productSubType` NVARCHAR(20) NULL,
  `productPrice` NVARCHAR(50) NULL,
  `beginTime` NVARCHAR(45) NULL,
  `expireTime` NVARCHAR(45) NULL,
  `createdAt` DATETIME NULL,
  `updatedAt` DATETIME NULL,
  PRIMARY KEY (`productId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='商品信息表';

SET FOREIGN_KEY_CHECKS = 1;