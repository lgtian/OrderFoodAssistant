USE `orderfoodassistant`;
DROP procedure IF EXISTS `hahaha`;

DELIMITER $$
USE `orderfoodassistant`$$
CREATE PROCEDURE `sp_batch_create_actiity`(in startD date, in endD date, in groupN nvarchar(50))
BEGIN
    declare i int default 1;
	declare start_date date ;
	declare end_date date ;
	declare group_name nvarchar(50);
    declare expired_at datetime;

	select startD into start_date;
	select endD into end_date;
    select groupN into group_name;

    while start_date < end_date
    do
        select date_add(start_date, interval 15 hour) into expired_at;
        insert into activity_info(
		`activityType`,
		`activitySubType`,
		`group`,
		`date` ,
		`expiredAt`,
		`createdBy`,
		`createdAt`,
		`updatedAt`) values (
        'lunch',
        '11',
        group_name,
        start_date,
        expired_at,
        'admin',
        '2020-02-01',
        '2020-02-01'
        );

        insert into activity_info(
		`activityType`,
		`activitySubType`,
		`group`,
		`date` ,
		`expiredAt`,
		`createdBy`,
		`createdAt`,
		`updatedAt`) values (
        'lunch',
        '16',
        group_name,
        start_date,
        expired_at,
        'admin',
        '2020-02-01',
        '2020-02-01'
        );

        insert into activity_info(
		`activityType`,
		`activitySubType`,
		`group`,
		`date` ,
		`expiredAt`,
		`createdBy`,
		`createdAt`,
		`updatedAt`) values (
        'dinner',
        '11',
        group_name,
        start_date,
        expired_at,
        'admin',
        '2020-02-01',
        '2020-02-01'
        );

        insert into activity_info(
		`activityType`,
		`activitySubType`,
		`group`,
		`date` ,
		`expiredAt`,
		`createdBy`,
		`createdAt`,
		`updatedAt`) values (
        'dinner',
        '16',
        group_name,
        start_date,
        expired_at,
        'admin',
        '2020-02-01',
        '2020-02-01'
        );
        set start_date = date_add(start_date,interval 1 day);
    end while;
    commit;
END$$

DELIMITER ;

