CREATE TABLE `users` (
  `user_id` bigint(20) NOT NULL,
  `balance` decimal(10,2) NOT NULL DEFAULT '0.00',
  `work` datetime DEFAULT NULL,
  PRIMARY KEY (`user_id`)
)