USE doorbot;
INSERT INTO `doorinfo` VALUES (1,'online','10.10.10.67','door403','22'),(2,'offline','10.10.15.10','door300','22');
INSERT INTO `door` VALUES (1,'Room 403 Door', 'password', 'salt', 'Lakeview',1),(2,'Room 300 Door', 'password2', 'salt2', 'Plaza',2);
INSERT INTO `opentype` VALUES (1,'manual'),(2,'bot'),(3,'scheduled');
INSERT INTO `scheduledEvent` VALUES (1,'2008-11-09 15:45:21','2008-11-11 13:23:44','Party B',1);
INSERT INTO `usertype` VALUES (1,'admin','15:45:21','13:23:44'),(2,'resident','15:45:21','13:23:44'),(3,'guest','15:45:21','13:23:44');
INSERT INTO `user` VALUES (1,'ccrollin','passwordTest','saltTest',true,1);
INSERT INTO `userinstance` VALUES (1,0,1,1,2);
INSERT INTO `userToEvent` VALUES (1,1);