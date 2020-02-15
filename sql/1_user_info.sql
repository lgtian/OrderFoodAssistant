SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS  `user_info`;
CREATE TABLE `user_info` (
  `employeeId` varchar(32) DEFAULT NULL,
  `name` varchar(32) DEFAULT NULL,
  `password` varchar(32) DEFAULT NULL,
  `group` varchar(32) DEFAULT NULL,
  `role` varchar(32) DEFAULT NULL,
  `createdAt` datetime DEFAULT NULL,
  `updatedAt` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='user info';

SET FOREIGN_KEY_CHECKS = 1;

