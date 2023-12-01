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
-- Table structure for table `openlog`
--

DROP TABLE IF EXISTS `openlog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `openlog` (
  `id` int NOT NULL AUTO_INCREMENT,
  `timestamp` datetime NOT NULL,
  `door_id_openlog` int NOT NULL,
  `photo_id_openlog` int NOT NULL,
  `userInstance_id_openlog` int NOT NULL,
  `openType_id_openlog` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  UNIQUE KEY `photo_id_openlog` (`photo_id_openlog`),
  KEY `fk_doorid_openlog` (`door_id_openlog`),
  KEY `fk_photoid_openlog` (`photo_id_openlog`),
  KEY `fk_userInstanceid_openlog` (`userInstance_id_openlog`),
  KEY `fk_openTypeid_openlog` (`openType_id_openlog`),
  CONSTRAINT `fk_doorid_openlog` FOREIGN KEY (`door_id_openlog`) REFERENCES `door` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_openTypeid_openlog` FOREIGN KEY (`openType_id_openlog`) REFERENCES `opentype` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_photoid_openlog` FOREIGN KEY (`photo_id_openlog`) REFERENCES `entryphoto` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_userInstanceid_openlog` FOREIGN KEY (`userInstance_id_openlog`) REFERENCES `userinstance` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `openlog`
--

LOCK TABLES `openlog` WRITE;
/*!40000 ALTER TABLE `openlog` DISABLE KEYS */;
/*!40000 ALTER TABLE `openlog` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-12-01  3:27:50
