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
-- Table structure for table `penaltylog`
--

DROP TABLE IF EXISTS `penaltylog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `penaltylog` (
  `id` int NOT NULL AUTO_INCREMENT,
  `timestamp` datetime NOT NULL,
  `penalty` int NOT NULL,
  `door_id_penaltylog` int NOT NULL,
  `userInstance_id_penaltylog` int NOT NULL,
  `penaltyType_id_penaltylog` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `fk_doorid_penaltylog` (`door_id_penaltylog`),
  KEY `fk_userInstanceid_penaltylog` (`userInstance_id_penaltylog`),
  KEY `fk_penaltyTypeid_penaltylog` (`penaltyType_id_penaltylog`),
  CONSTRAINT `fk_doorid_penaltylog` FOREIGN KEY (`door_id_penaltylog`) REFERENCES `door` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_penaltyTypeid_penaltylog` FOREIGN KEY (`penaltyType_id_penaltylog`) REFERENCES `penaltytype` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_userInstanceid_penaltylog` FOREIGN KEY (`userInstance_id_penaltylog`) REFERENCES `userinstance` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `penaltylog`
--

LOCK TABLES `penaltylog` WRITE;
/*!40000 ALTER TABLE `penaltylog` DISABLE KEYS */;
/*!40000 ALTER TABLE `penaltylog` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-12-01  3:27:47
