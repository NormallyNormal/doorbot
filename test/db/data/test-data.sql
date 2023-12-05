USE doorbot;
INSERT INTO `doorinfo` VALUES (1,'online','10.10.10.67','door403','22'),(2,'offline','10.10.15.10','door300','22');
INSERT INTO `door` VALUES (1,'Room 403 Door','password','salt','Lakeview',1),(2,'Room 300 Door','password2','salt2','Plaza',2);
INSERT INTO `opentype` VALUES (1,'manual'),(2,'bot'),(3,'scheduled');
INSERT INTO `scheduledEvent` VALUES (1,'2008-11-09 15:45:21','2008-11-11 13:23:44','Party B',1);
INSERT INTO `usertype` VALUES (1,'admin','00:00:00','23:59:59'),(2,'resident','00:00:00','23:59:59'),(3,'guest','9:00:00','15:00:00');
INSERT INTO `user` VALUES (1,'1234','ff7578b6e3a909d2646c9b8361af8f8f5afbb0e981ddc5231533b8f950b2edbf','8498b943341dbb35814ec6438c19b30c',1,0,1),(2,'12345','password','salt',0,1,1),('3', '10101', 'password2', 'salt2', 0, 0, NULL);
INSERT INTO `userinstance` VALUES (1,0,1,1,2);
INSERT INTO `userToEvent` VALUES (1,1);