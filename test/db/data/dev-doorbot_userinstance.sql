-- MySQL dump 10.13  Distrib 8.0.33, for Win64 (x86_64)
--
-- Host: csc440-chupacabra-proj.mysql.database.azure.com    Database: dev-doorbot
-- ------------------------------------------------------
-- Server version	8.0.34

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `userinstance`
--

DROP TABLE IF EXISTS `userinstance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `userinstance` (
  `id` int NOT NULL AUTO_INCREMENT,
  `score` int NOT NULL,
  `door_id_userinstance` int NOT NULL,
  `user_id_userinstance` int NOT NULL,
  `userType_id_userinstance` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `fk_doorid_userinstance` (`door_id_userinstance`),
  KEY `fk_userid_userinstance` (`user_id_userinstance`),
  KEY `fk_userTypeid_userinstance` (`userType_id_userinstance`),
  CONSTRAINT `fk_doorid_userinstance` FOREIGN KEY (`door_id_userinstance`) REFERENCES `door` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_userid_userinstance` FOREIGN KEY (`user_id_userinstance`) REFERENCES `user` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_userTypeid_userinstance` FOREIGN KEY (`userType_id_userinstance`) REFERENCES `usertype` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `userinstance`
--

LOCK TABLES `userinstance` WRITE;
/*!40000 ALTER TABLE `userinstance` DISABLE KEYS */;
INSERT INTO `userinstance` VALUES (1,0,1,1,2);
/*!40000 ALTER TABLE `userinstance` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-12-01  3:27:48
