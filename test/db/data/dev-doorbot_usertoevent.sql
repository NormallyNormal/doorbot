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
-- Table structure for table `usertoevent`
--

DROP TABLE IF EXISTS `usertoevent`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usertoevent` (
  `userInstance_id_userToEvent` int NOT NULL,
  `event_id_userToEvent` int NOT NULL,
  PRIMARY KEY (`userInstance_id_userToEvent`,`event_id_userToEvent`),
  KEY `fk_userInstanceid_userToEvent` (`userInstance_id_userToEvent`),
  KEY `fk_eventid_userToEvent` (`event_id_userToEvent`),
  CONSTRAINT `fk_eventid_userToEvent` FOREIGN KEY (`event_id_userToEvent`) REFERENCES `scheduledevent` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_userInstanceid_userToEvent` FOREIGN KEY (`userInstance_id_userToEvent`) REFERENCES `userinstance` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usertoevent`
--

LOCK TABLES `usertoevent` WRITE;
/*!40000 ALTER TABLE `usertoevent` DISABLE KEYS */;
INSERT INTO `usertoevent` VALUES (1,1);
/*!40000 ALTER TABLE `usertoevent` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-12-01  3:27:52
