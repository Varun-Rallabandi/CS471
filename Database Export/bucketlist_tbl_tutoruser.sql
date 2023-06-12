-- MySQL dump 10.13  Distrib 8.0.33, for Win64 (x86_64)
--
-- Host: localhost    Database: bucketlist
-- ------------------------------------------------------
-- Server version	8.0.33

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
-- Table structure for table `tbl_tutoruser`
--

DROP TABLE IF EXISTS `tbl_tutoruser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tbl_tutoruser` (
  `user_id` bigint NOT NULL AUTO_INCREMENT,
  `user_name` varchar(100) DEFAULT NULL,
  `user_username` varchar(100) DEFAULT NULL,
  `user_password` varchar(1000) DEFAULT NULL,
  `time1` varchar(20) DEFAULT 'N',
  `time2` varchar(20) DEFAULT 'N',
  `time3` varchar(20) DEFAULT 'N',
  `class1` varchar(20) DEFAULT 'N',
  `class2` varchar(20) DEFAULT 'N',
  `class3` varchar(20) DEFAULT 'N',
  `qualifications` varchar(5000) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `user_id` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_tutoruser`
--

LOCK TABLES `tbl_tutoruser` WRITE;
/*!40000 ALTER TABLE `tbl_tutoruser` DISABLE KEYS */;
INSERT INTO `tbl_tutoruser` VALUES (12,'Aaron','aaron@gmail.com','pbkdf2:sha256:260000$0n73Cz8A3wTbgJLm$a575391ea1d10cdaef7dd3a78ff0073ad318dd0c2fcc73d45ecf32ccbd513c55','Y','Y','N','N','Y','Y','I am proficient in programing in C and Java! '),(13,'aaron','aaron1@gmail.com','pbkdf2:sha256:260000$pvSOI79q1vPgIV0N$76e4b4a3351d5d97761cd3565766545e4201f622a095b44cf529fdb3436c7e49','Y','N','Y','Y','N','Y','I am good with coding in java');
/*!40000 ALTER TABLE `tbl_tutoruser` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-06-12 19:01:37
