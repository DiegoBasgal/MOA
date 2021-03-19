-- MySQL dump 10.13  Distrib 8.0.23, for Linux (x86_64)
--
-- Host: localhost    Database: django_db
-- ------------------------------------------------------
-- Server version	8.0.23-0ubuntu0.20.04.1

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
-- Table structure for table `agendamentos_agendamento`
--

DROP TABLE IF EXISTS `agendamentos_agendamento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `agendamentos_agendamento` (
  `id` int NOT NULL AUTO_INCREMENT,
  `data` datetime(6) NOT NULL,
  `observacao` longtext NOT NULL,
  `comando_id` int NOT NULL,
  `executado` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `agendamentos_agendamento_comando_id_673bc6c2` (`comando_id`),
  CONSTRAINT `agendamentos_agendamento_comando_id_673bc6c2_fk` FOREIGN KEY (`comando_id`) REFERENCES `parametros_moa_comando` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=68 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `agendamentos_agendamento`
--

LOCK TABLES `agendamentos_agendamento` WRITE;
/*!40000 ALTER TABLE `agendamentos_agendamento` DISABLE KEYS */;
INSERT INTO `agendamentos_agendamento` VALUES (46,'2021-02-22 19:36:00.000000','',10,1),(47,'2021-02-22 19:37:00.000000','',10,1),(48,'2021-02-22 19:38:00.000000','',10,1),(49,'2021-02-22 19:36:00.000000','',20,1),(51,'2021-02-22 19:38:00.000000','',10,1),(53,'2021-02-22 19:41:00.000000','',10,1),(55,'2021-02-22 19:44:00.000000','',10,1),(56,'2021-02-22 19:44:00.000000','',20,1),(57,'2021-02-22 19:50:00.000000','',20,1),(58,'2021-02-22 19:50:00.000000','',10,1),(59,'2021-02-22 19:52:00.000000','',10,1),(60,'2021-02-22 19:52:00.000000','',20,1),(61,'2021-02-22 19:53:00.000000','',20,1),(63,'2021-02-22 19:56:00.000000','',10,1),(64,'2021-02-22 19:56:00.000000','',20,1),(65,'2021-02-22 19:56:00.000000','',3,1),(66,'2021-02-22 19:57:00.000000','',3,1),(67,'2021-02-22 20:10:00.000000','',10,1);
/*!40000 ALTER TABLE `agendamentos_agendamento` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add parametros usina',7,'add_parametrosusina'),(26,'Can change parametros usina',7,'change_parametrosusina'),(27,'Can delete parametros usina',7,'delete_parametrosusina'),(28,'Can view parametros usina',7,'view_parametrosusina'),(29,'Can add contato',8,'add_contato'),(30,'Can change contato',8,'change_contato'),(31,'Can delete contato',8,'delete_contato'),(32,'Can view contato',8,'view_contato'),(33,'Can add agendamento',9,'add_agendamento'),(34,'Can change agendamento',9,'change_agendamento'),(35,'Can delete agendamento',9,'delete_agendamento'),(36,'Can view agendamento',9,'view_agendamento'),(37,'Can add comando',10,'add_comando'),(38,'Can change comando',10,'change_comando'),(39,'Can delete comando',10,'delete_comando'),(40,'Can view comando',10,'view_comando');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$216000$gsuWv6kGz7B3$SLkL6FXIWZ+JQlCd8AXd/p8UC5I4nEt+OYbGSRw+aFQ=','2021-03-18 20:14:28.176348',1,'super_lucas','','','lucas@ritmoenergia.com.br',1,1,'2021-01-27 19:20:05.881890'),(2,'pbkdf2_sha256$216000$Y9Q0wr3CQUUV$4OSLZf+6HZOyJXF4/KeXq29PRYNT646KYZU5fFY3JHc=','2021-03-03 18:53:10.429786',0,'lucas','','','',0,1,'2021-01-27 19:21:24.333354'),(3,'pbkdf2_sha256$216000$5zHh3dA6BpAN$aHL77p1WGNnjylcXC2mRzKVmsCLwCmZ9pfGX0xrnM4A=',NULL,0,'henrique','','','',0,1,'2021-02-08 19:05:04.563275');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=134 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2021-01-27 19:21:24.448107','2','lucas',1,'[{\"added\": {}}]',4,1),(2,'2021-02-01 18:55:48.989029','1','ParametrosUsina object (1)',1,'[{\"added\": {}}]',7,1),(3,'2021-02-01 19:02:16.683314','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Aguardando reservatorio\", \"Clp online\", \"Ug1 sinc\", \"Ug2 sinc\"]}}]',7,1),(4,'2021-02-02 18:16:03.182471','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Kp\"]}}]',7,1),(5,'2021-02-02 18:17:20.998528','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Kp\", \"Ki\", \"Kd\", \"Ug1 pot\", \"Ug1 setpot\"]}}]',7,1),(6,'2021-02-02 18:18:07.842292','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Kie\"]}}]',7,1),(7,'2021-02-02 18:20:21.101854','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Nv montante\", \"Ug1 setpot\", \"Valor ie inicial\"]}}]',7,1),(8,'2021-02-02 18:25:54.175931','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Ki\", \"Kd\", \"Kie\", \"N movel L\", \"Nv montante\", \"Ug1 pot\", \"Ug1 setpot\"]}}]',7,1),(9,'2021-02-02 18:26:09.567318','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Ki\"]}}]',7,1),(10,'2021-02-02 18:26:14.519183','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Nv montante\"]}}]',7,1),(11,'2021-02-02 19:10:20.988221','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Kie\", \"Nv montante\", \"Ug1 setpot\"]}}]',7,1),(12,'2021-02-02 19:12:48.243267','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Kie\", \"Nv montante\", \"Ug1 pot\", \"Ug1 setpot\"]}}]',7,1),(13,'2021-02-02 19:16:02.284739','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Kd\", \"Nv montante\", \"Ug1 pot\", \"Ug1 setpot\"]}}]',7,1),(14,'2021-02-02 19:16:17.735460','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Kie\", \"Nv montante\", \"Ug1 setpot\"]}}]',7,1),(15,'2021-02-02 19:16:49.768650','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Kd\", \"Nv montante\", \"Ug1 setpot\"]}}]',7,1),(16,'2021-02-03 18:21:00.405775','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Emergencia MOA\", \"Timestamp\", \"Nv montante\", \"Ug1 pot\", \"Ug1 setpot\", \"Ug1 sinc\"]}}]',7,1),(17,'2021-02-03 18:36:24.058731','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Emergencia MOA\", \"Timestamp\"]}}]',7,1),(18,'2021-02-03 18:58:36.480428','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Emergencia MOA\", \"Timestamp\"]}}]',7,1),(19,'2021-02-03 18:59:06.351551','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Emergencia MOA\", \"Timestamp\"]}}]',7,1),(20,'2021-02-03 19:06:47.429437','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Emergencia MOA\", \"Timestamp\", \"Nv montante\"]}}]',7,1),(21,'2021-02-03 19:14:14.853220','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Modo autonomo\", \"Timestamp\", \"Ug1 pot\", \"Ug1 setpot\"]}}]',7,1),(22,'2021-02-03 19:14:24.101159','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Modo autonomo\"]}}]',7,1),(23,'2021-02-03 19:14:34.311045','1','ParametrosUsina object (1)',2,'[]',7,1),(24,'2021-02-03 19:14:44.729226','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Modo autonomo\"]}}]',7,1),(25,'2021-02-03 19:14:50.883231','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Modo autonomo\", \"Emergencia MOA\"]}}]',7,1),(26,'2021-02-03 19:14:55.354071','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Emergencia MOA\"]}}]',7,1),(27,'2021-02-03 19:24:50.777918','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Emergencia MOA\", \"Timestamp\", \"Nv montante\", \"Ug1 pot\", \"Ug1 setpot\", \"Ug2 pot\", \"Ug2 setpot\"]}}]',7,1),(28,'2021-02-03 19:26:43.231397','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Modo autonomo\", \"Timestamp\"]}}]',7,1),(29,'2021-02-03 19:26:47.011609','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Emergencia MOA\"]}}]',7,1),(30,'2021-02-03 19:26:51.755747','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Emergencia MOA\"]}}]',7,1),(31,'2021-02-03 19:26:57.141999','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Emergencia MOA\"]}}]',7,1),(32,'2021-02-03 19:27:00.822085','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Modo autonomo\"]}}]',7,1),(33,'2021-02-03 19:54:07.904669','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Timestamp\", \"Nv alvo\", \"Nv montante\", \"Ug1 pot\", \"Ug1 setpot\"]}}]',7,1),(34,'2021-02-03 19:54:48.844786','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Nv alvo\"]}}]',7,1),(35,'2021-02-08 18:59:07.258061','1','Contato object (1)',1,'[{\"added\": {}}]',8,1),(36,'2021-02-08 18:59:42.876889','2','Contato object (2)',1,'[{\"added\": {}}]',8,1),(37,'2021-02-08 19:04:08.370588','3','Contato object (3)',1,'[{\"added\": {}}]',8,1),(38,'2021-02-08 19:05:04.674591','3','henrique',1,'[{\"added\": {}}]',4,1),(39,'2021-02-08 19:19:00.898629','1','Contato object (1)',2,'[{\"changed\": {\"fields\": [\"Nome\"]}}]',8,1),(40,'2021-02-08 19:19:04.013227','2','Contato object (2)',2,'[]',8,1),(41,'2021-02-08 19:19:35.040540','3','Contato object (3)',2,'[{\"changed\": {\"fields\": [\"Nome\"]}}]',8,1),(42,'2021-02-08 19:28:20.258813','3','Contato object (3)',2,'[{\"changed\": {\"fields\": [\"Nome\"]}}]',8,1),(43,'2021-02-08 21:01:08.890799','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Timestamp\", \"Aguardando reservatorio\", \"Nv montante\", \"Nv religamento\", \"Ug1 pot\", \"Ug1 setpot\", \"Ug1 sinc\", \"Ug2 pot\", \"Ug2 setpot\", \"Ug2 sinc\"]}}]',7,1),(44,'2021-02-08 21:48:41.809359','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Timestamp\", \"Nv alvo\", \"Ug2 sinc\"]}}]',7,1),(45,'2021-02-08 21:50:01.721649','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Timestamp\", \"Nv alvo\", \"Nv montante\", \"Ug2 sinc\"]}}]',7,1),(46,'2021-02-09 00:04:27.782183','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Timestamp\", \"Kp\", \"Ug2 pot\", \"Ug2 setpot\", \"Ug2 tempo\"]}}]',7,1),(47,'2021-02-09 00:05:03.215353','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Timestamp\", \"Kie\", \"Nv montante\", \"Ug2 tempo\"]}}]',7,1),(48,'2021-02-09 00:07:21.877173','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Timestamp\", \"Kd\", \"Ug2 tempo\"]}}]',7,1),(49,'2021-02-09 00:08:22.640178','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Timestamp\", \"Kd\", \"Kie\", \"Ug2 tempo\"]}}]',7,1),(50,'2021-02-09 00:15:25.293876','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Timestamp\", \"Nv montante\", \"Ug2 tempo\", \"Valor ie inicial\"]}}]',7,1),(51,'2021-02-09 00:24:27.780310','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Timestamp\", \"Kp\", \"Nv montante\", \"Ug1 pot\", \"Ug1 setpot\", \"Ug1 sinc\", \"Ug1 tempo\", \"Ug2 pot\", \"Ug2 setpot\", \"Ug2 sinc\", \"Ug2 tempo\"]}}]',7,1),(52,'2021-02-09 00:31:27.016367','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Timestamp\", \"Kd\", \"Nv montante\", \"Ug1 pot\", \"Ug1 setpot\", \"Ug1 tempo\"]}}]',7,1),(53,'2021-02-09 01:04:36.211819','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Timestamp\", \"Ug2 disp\"]}}]',7,1),(54,'2021-02-16 19:18:13.421547','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Timestamp\", \"Ug2 prioridade\"]}}]',7,1),(55,'2021-02-16 19:18:24.872375','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Timestamp\", \"Ug2 tempo\"]}}]',7,1),(56,'2021-02-16 19:19:02.594031','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Status moa\", \"Emergencia acionada\", \"Timestamp\", \"Pot disp\", \"Ug1 disp\", \"Ug2 disp\", \"Ug2 setpot\", \"Ug2 tempo\"]}}]',7,1),(57,'2021-02-16 19:19:22.123450','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Timestamp\", \"Ug2 prioridade\"]}}]',7,1),(58,'2021-02-16 19:19:36.240177','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Timestamp\", \"Ug1 prioridade\"]}}]',7,1),(59,'2021-02-16 19:22:09.430760','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Status moa\", \"Emergencia acionada\", \"Timestamp\", \"Nv montante\", \"Pot disp\", \"Ug1 disp\", \"Ug1 pot\", \"Ug1 sinc\", \"Ug1 tempo\", \"Ug2 disp\", \"Ug2 setpot\", \"Ug2 tempo\"]}}]',7,1),(60,'2021-02-17 17:38:43.518380','1','Agendamento object (1)',1,'[{\"added\": {}}]',9,1),(61,'2021-02-17 17:38:59.075851','2','Agendamento object (2)',1,'[{\"added\": {}}]',9,1),(62,'2021-02-17 17:39:12.884248','3','Agendamento object (3)',1,'[{\"added\": {}}]',9,1),(63,'2021-02-17 17:39:34.301781','1','Agendamento object (1)',2,'[]',9,1),(64,'2021-02-18 18:56:21.425797','9','Agendamento object (9)',3,'',9,1),(65,'2021-02-18 18:56:21.516822','8','Agendamento object (8)',3,'',9,1),(66,'2021-02-18 18:56:21.526762','7','Agendamento object (7)',3,'',9,1),(67,'2021-02-18 18:56:21.529276','6','Agendamento object (6)',3,'',9,1),(68,'2021-02-18 18:56:21.534708','5','Agendamento object (5)',3,'',9,1),(69,'2021-02-18 18:56:21.537057','4','Agendamento object (4)',3,'',9,1),(70,'2021-02-18 18:56:21.539324','3','Agendamento object (3)',3,'',9,1),(71,'2021-02-18 18:56:21.544117','2','Agendamento object (2)',3,'',9,1),(72,'2021-02-18 18:56:21.565674','1','Agendamento object (1)',3,'',9,1),(73,'2021-02-18 18:58:17.623413','1','Comando object (1)',1,'[{\"added\": {}}]',10,1),(74,'2021-02-18 18:59:01.947909','2','Comando object (2)',1,'[{\"added\": {}}]',10,1),(75,'2021-02-18 18:59:06.002992','2','Comando object (2)',2,'[]',10,1),(76,'2021-02-19 19:28:50.206472','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Timestamp\", \"Nv montante\", \"Ug2 disp\"]}}]',7,1),(77,'2021-02-19 21:12:14.986978','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Timestamp\", \"Kp\", \"Ki\", \"Nv montante\", \"Ug1 pot\", \"Ug1 setpot\", \"Ug1 sinc\", \"Ug2 pot\", \"Ug2 setpot\"]}}]',7,1),(78,'2021-02-19 21:12:32.274175','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Timestamp\", \"Kp\", \"Nv montante\", \"Ug2 pot\"]}}]',7,1),(79,'2021-02-19 21:12:57.434693','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Timestamp\", \"Nv alvo\", \"Nv maximo\", \"Nv montante\", \"Nv religamento\"]}}]',7,1),(80,'2021-02-22 19:03:32.059713','1','Comando object (1)',2,'[{\"changed\": {\"fields\": [\"Nome\"]}}]',10,1),(81,'2021-02-22 19:11:26.340465','3','Comando object (3)',1,'[{\"added\": {}}]',10,1),(82,'2021-02-22 19:11:53.893171','2','Comando object (2)',2,'[{\"changed\": {\"fields\": [\"Nome\"]}}]',10,1),(83,'2021-02-22 19:12:10.427073','10','Comando object (10)',1,'[{\"added\": {}}]',10,1),(84,'2021-02-22 19:12:26.323247','20','Comando object (20)',1,'[{\"added\": {}}]',10,1),(85,'2021-02-22 19:12:47.350719','11','Comando object (11)',1,'[{\"added\": {}}]',10,1),(86,'2021-02-22 19:13:02.866245','21','Comando object (21)',1,'[{\"added\": {}}]',10,1),(87,'2021-03-03 18:54:47.457467','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Timestamp\", \"Nv comporta pos 0 prox\", \"Nv comporta pos 1 prox\", \"Nv comporta pos 2 prox\", \"Nv comporta pos 3 prox\", \"Nv comporta pos 4 prox\", \"Nv comporta pos 1 ant\", \"Nv comporta pos 2 ant\", \"Nv comporta pos 3 ant\", \"Nv comporta pos 4 ant\", \"Nv comporta pos 5 ant\"]}}]',7,1),(88,'2021-03-03 19:13:30.427307','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Timestamp\", \"Nv montante\", \"Ug1 pot\", \"Ug1 setpot\", \"Ug1 tempo\", \"Ug2 setpot\", \"Ug2 tempo\", \"Nv comporta pos 5 prox\"]}}]',7,1),(89,'2021-03-03 19:16:57.487036','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Timestamp\", \"Nv montante\", \"Ug1 pot\", \"Ug1 tempo\", \"Ug2 tempo\", \"Nv comporta pos 1 prox\", \"Nv comporta pos 2 prox\", \"Nv comporta pos 3 prox\", \"Nv comporta pos 4 prox\", \"Nv comporta pos 3 ant\", \"Nv comporta pos 4 ant\", \"Nv comporta pos 5 ant\"]}}]',7,1),(90,'2021-03-03 19:47:02.878103','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Timestamp\", \"Aguardando reservatorio\", \"Nv montante\", \"Ug1 pot\", \"Ug1 setpot\", \"Ug1 tempo\", \"Ug2 setpot\", \"Ug2 tempo\", \"Nv comporta pos 0 ant\", \"Nv comporta pos 1 ant\", \"Nv comporta pos 2 ant\", \"Nv comporta pos 3 ant\", \"Nv comporta pos 4 ant\", \"Nv comporta pos 5 ant\", \"Nv comporta pos 0 prox\", \"Nv comporta pos 1 prox\", \"Nv comporta pos 2 prox\", \"Nv comporta pos 3 prox\", \"Nv comporta pos 4 prox\", \"Nv comporta pos 5 prox\"]}}]',7,1),(91,'2021-03-03 19:48:31.953845','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Nv comporta pos 0 ant\", \"Nv comporta pos 1 ant\", \"Nv comporta pos 2 ant\", \"Nv comporta pos 3 ant\", \"Nv comporta pos 4 ant\", \"Nv comporta pos 5 ant\", \"Nv comporta pos 0 prox\", \"Nv comporta pos 1 prox\", \"Nv comporta pos 2 prox\", \"Nv comporta pos 3 prox\", \"Nv comporta pos 4 prox\", \"Nv comporta pos 5 prox\"]}}]',7,1),(92,'2021-03-03 19:53:01.064801','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Timestamp\", \"Nv montante\", \"Pos comporta\", \"Nv comporta pos 0 ant\", \"Nv comporta pos 1 ant\", \"Nv comporta pos 2 ant\", \"Nv comporta pos 3 ant\", \"Nv comporta pos 4 ant\", \"Nv comporta pos 5 ant\", \"Nv comporta pos 0 prox\", \"Nv comporta pos 1 prox\", \"Nv comporta pos 2 prox\", \"Nv comporta pos 3 prox\", \"Nv comporta pos 4 prox\", \"Nv comporta pos 5 prox\"]}}]',7,1),(93,'2021-03-03 20:23:18.381696','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Timestamp\", \"Nv montante\", \"Ug1 tempo\", \"Ug2 tempo\", \"Pos comporta\", \"Nv comporta pos 1 ant\", \"Nv comporta pos 2 ant\", \"Nv comporta pos 4 ant\", \"Nv comporta pos 5 ant\", \"Nv comporta pos 0 prox\", \"Nv comporta pos 2 prox\", \"Nv comporta pos 3 prox\", \"Nv comporta pos 4 prox\", \"Nv comporta pos 5 prox\"]}}]',7,1),(94,'2021-03-04 19:04:29.868332','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Timestamp\", \"Nv montante\", \"Ug1 pot\", \"Tolerancia pot maxima\"]}}]',7,1),(95,'2021-03-08 19:18:17.687781','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Timestamp\", \"Kp\", \"Nv montante\", \"Ug1 pot\", \"Ug2 temp mancal\", \"Ug2 perda grade\"]}}]',7,1),(96,'2021-03-08 19:29:26.275078','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Timestamp\", \"Kp\", \"Nv montante\", \"Pot disp\", \"Ug1 pot\", \"Ug1 tempo\", \"Ug2 disp\", \"Ug2 tempo\", \"Pos comporta\", \"Ug1 temp mancal\", \"Ug2 temp mancal\", \"Ug1 perda grade\", \"Ug2 perda grade\"]}}]',7,1),(97,'2021-03-08 19:35:06.162696','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Timestamp\", \"Kp\", \"Ug1 pot\", \"Ug1 tempo\", \"Ug1 temp mancal\", \"Ug2 temp mancal\", \"Ug1 perda grade\", \"Ug2 perda grade\"]}}]',7,1),(98,'2021-03-08 19:40:13.078503','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Timestamp\", \"Kp\", \"Ug1 pot\", \"Ug1 setpot\", \"Ug1 temp mancal\", \"Ug2 temp mancal\", \"Ug2 perda grade\"]}}]',7,1),(99,'2021-03-08 19:40:17.566459','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Timestamp\", \"Kd\", \"Ug1 pot\", \"Ug1 setpot\", \"Ug1 tempo\", \"Ug1 temp mancal\", \"Ug2 temp mancal\", \"Ug1 perda grade\", \"Ug2 perda grade\"]}}]',7,1),(100,'2021-03-08 19:42:07.468327','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Timestamp\", \"Ki\", \"Kd\", \"Nv montante\", \"Ug1 pot\", \"Ug1 setpot\", \"Ug1 tempo\", \"Ug2 temp mancal\", \"Ug1 perda grade\", \"Ug2 perda grade\"]}}]',7,1),(101,'2021-03-08 19:43:57.515881','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Timestamp\", \"Kd\", \"Nv montante\", \"Ug1 pot\", \"Ug1 setpot\", \"Ug1 tempo\", \"Ug1 temp mancal\", \"Ug2 temp mancal\", \"Ug1 perda grade\"]}}]',7,1),(102,'2021-03-08 19:49:39.032721','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Timestamp\", \"Kp\", \"Ki\", \"Kd\", \"Nv montante\", \"Ug1 pot\", \"Ug1 setpot\", \"Ug1 tempo\", \"Ug1 temp mancal\", \"Ug2 temp mancal\", \"Ug1 perda grade\", \"Ug2 perda grade\"]}}]',7,1),(103,'2021-03-08 19:52:11.219595','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Timestamp\", \"Ki\", \"Nv montante\", \"Ug1 pot\", \"Ug1 setpot\", \"Ug1 tempo\", \"Ug1 temp mancal\", \"Ug2 temp mancal\", \"Ug1 perda grade\", \"Ug2 perda grade\"]}}]',7,1),(104,'2021-03-08 19:53:35.006953','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Timestamp\", \"Kp\", \"Nv montante\", \"Ug1 pot\", \"Ug1 setpot\", \"Ug1 tempo\", \"Ug1 temp mancal\", \"Ug2 temp mancal\", \"Ug1 perda grade\"]}}]',7,1),(105,'2021-03-08 20:02:18.331681','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Timestamp\", \"Kp\", \"Ki\", \"Nv montante\", \"Ug1 pot\", \"Ug1 setpot\", \"Ug1 temp mancal\", \"Ug2 temp mancal\", \"Ug1 perda grade\", \"Ug2 perda grade\"]}}]',7,1),(106,'2021-03-08 20:03:33.865873','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Timestamp\", \"N movel L\", \"N movel R\", \"Nv montante\", \"Ug1 pot\", \"Ug1 setpot\", \"Ug1 tempo\", \"Ug1 temp mancal\", \"Ug2 temp mancal\", \"Ug1 perda grade\", \"Ug2 perda grade\"]}}]',7,1),(107,'2021-03-08 20:08:02.129277','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Timestamp\", \"Kp\", \"Nv montante\", \"Ug1 pot\", \"Ug1 setpot\", \"Ug1 tempo\", \"Ug2 setpot\", \"Pos comporta\", \"Ug1 temp mancal\", \"Ug2 temp mancal\", \"Ug2 perda grade\"]}}]',7,1),(108,'2021-03-08 20:17:47.066236','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Timestamp\", \"Kp\", \"Ug1 pot\", \"Ug2 temp mancal\", \"Ug1 perda grade\", \"Ug2 perda grade\"]}}]',7,1),(109,'2021-03-08 20:19:40.724449','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Timestamp\", \"N movel L\", \"N movel R\", \"Nv montante\", \"Pot disp\", \"Ug1 pot\", \"Ug1 setpot\", \"Ug1 tempo\", \"Ug2 disp\", \"Ug1 temp mancal\", \"Ug2 temp mancal\", \"Ug1 perda grade\", \"Ug2 perda grade\"]}}]',7,1),(110,'2021-03-08 20:21:52.705650','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Timestamp\", \"Kp\", \"N movel L\", \"N movel R\", \"Nv montante\", \"Ug1 pot\", \"Ug1 setpot\", \"Ug1 tempo\", \"Pos comporta\", \"Ug1 temp mancal\", \"Ug2 temp mancal\", \"Ug1 perda grade\"]}}]',7,1),(111,'2021-03-08 20:23:18.653787','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Timestamp\", \"Kie\", \"Nv montante\", \"Ug1 pot\", \"Ug1 tempo\", \"Ug1 temp mancal\", \"Ug2 temp mancal\", \"Ug1 perda grade\", \"Ug2 perda grade\"]}}]',7,1),(112,'2021-03-08 20:26:30.701616','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Timestamp\", \"Kp\", \"Ki\", \"Kd\", \"Nv montante\", \"Pot disp\", \"Ug1 pot\", \"Ug1 setpot\", \"Ug1 tempo\", \"Ug2 disp\", \"Ug1 temp mancal\", \"Ug2 temp mancal\", \"Ug1 perda grade\", \"Ug2 perda grade\"]}}]',7,1),(113,'2021-03-08 20:28:13.063442','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Timestamp\", \"Kp\", \"Ki\", \"Kd\", \"Ug1 pot\", \"Ug1 setpot\", \"Ug1 tempo\", \"Ug2 temp mancal\", \"Ug1 perda grade\"]}}]',7,1),(114,'2021-03-08 20:29:40.032434','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Timestamp\", \"Kp\", \"Nv montante\", \"Ug1 pot\", \"Ug1 setpot\", \"Ug1 tempo\", \"Ug1 temp mancal\", \"Ug2 temp mancal\", \"Ug1 perda grade\", \"Ug2 perda grade\"]}}]',7,1),(115,'2021-03-08 20:32:34.697127','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Timestamp\", \"Ki\", \"Nv montante\", \"Ug1 tempo\", \"Ug1 temp mancal\", \"Ug2 temp mancal\", \"Ug1 perda grade\", \"Ug2 perda grade\"]}}]',7,1),(116,'2021-03-08 20:33:49.428074','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Timestamp\", \"Kp\", \"Nv montante\", \"Ug1 pot\", \"Ug1 tempo\", \"Ug1 temp mancal\", \"Ug2 temp mancal\", \"Ug1 perda grade\", \"Ug2 perda grade\"]}}]',7,1),(117,'2021-03-08 20:38:32.031078','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Timestamp\", \"Kp\", \"Ki\", \"Kd\", \"N movel L\", \"N movel R\", \"Nv montante\", \"Ug1 pot\", \"Ug1 setpot\", \"Ug1 tempo\", \"Ug1 temp mancal\", \"Ug2 temp mancal\", \"Ug1 perda grade\", \"Ug2 perda grade\"]}}]',7,1),(118,'2021-03-08 20:48:19.856701','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Timestamp\", \"Kd\", \"Nv montante\", \"Ug1 pot\", \"Ug1 setpot\", \"Ug1 tempo\", \"Ug2 setpot\", \"Pos comporta\", \"Ug1 temp mancal\", \"Ug2 temp mancal\", \"Ug1 perda grade\", \"Ug2 perda grade\"]}}]',7,1),(119,'2021-03-08 20:49:56.321523','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Timestamp\", \"Kd\", \"Nv montante\", \"Ug1 pot\", \"Ug1 setpot\", \"Ug1 tempo\", \"Ug1 temp mancal\", \"Ug2 temp mancal\", \"Ug1 perda grade\", \"Ug2 perda grade\"]}}]',7,1),(120,'2021-03-08 20:50:40.361714','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Timestamp\", \"Ki\", \"Nv montante\", \"Ug1 pot\", \"Ug1 setpot\", \"Ug1 tempo\", \"Ug1 temp mancal\", \"Ug2 temp mancal\", \"Ug1 perda grade\", \"Ug2 perda grade\"]}}]',7,1),(121,'2021-03-09 18:14:41.614075','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Timestamp\", \"Kie\", \"Nv montante\", \"Ug1 pot\", \"Ug1 setpot\", \"Ug2 tempo\", \"Ug1 temp mancal\", \"Ug2 temp mancal\", \"Ug1 perda grade\", \"Ug2 perda grade\"]}}]',7,1),(122,'2021-03-09 18:23:52.713374','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Timestamp\", \"Ki\", \"Kie\", \"Nv montante\", \"Ug1 pot\", \"Ug1 tempo\", \"Ug1 temp mancal\", \"Ug2 temp mancal\", \"Ug1 perda grade\"]}}]',7,1),(123,'2021-03-09 18:31:54.670744','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Timestamp\", \"Kd\", \"Nv montante\", \"Ug1 pot\", \"Ug1 temp mancal\", \"Ug2 temp mancal\", \"Ug1 perda grade\", \"Ug2 perda grade\"]}}]',7,1),(124,'2021-03-09 18:35:58.020531','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Timestamp\", \"Kp\", \"Ki\", \"Kd\", \"Kie\", \"Ug1 pot\", \"Ug1 setpot\", \"Ug1 temp mancal\", \"Ug2 temp mancal\", \"Ug1 perda grade\", \"Ug2 perda grade\"]}}]',7,1),(125,'2021-03-09 18:43:31.867123','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Timestamp\", \"Kp\", \"Ki\", \"Kd\", \"Nv montante\", \"Ug1 pot\", \"Ug1 setpot\", \"Ug1 tempo\", \"Ug2 tempo\", \"Ug1 temp mancal\", \"Ug2 temp mancal\", \"Ug1 perda grade\", \"Ug2 perda grade\"]}}]',7,1),(126,'2021-03-09 18:48:33.903585','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Timestamp\", \"Kp\", \"Ki\", \"Kie\", \"Ug1 pot\", \"Ug1 setpot\", \"Ug1 temp mancal\", \"Ug2 temp mancal\", \"Ug1 perda grade\", \"Ug2 perda grade\"]}}]',7,1),(127,'2021-03-09 18:54:55.632143','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Timestamp\", \"Ki\", \"Kie\", \"Nv montante\", \"Ug1 pot\", \"Ug1 setpot\", \"Ug1 tempo\", \"Ug2 setpot\", \"Ug1 temp mancal\", \"Ug2 temp mancal\", \"Ug1 perda grade\", \"Ug2 perda grade\"]}}]',7,1),(128,'2021-03-09 19:02:59.093231','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Timestamp\", \"N movel L\", \"N movel R\", \"Ug1 pot\", \"Ug1 setpot\", \"Ug1 tempo\", \"Ug1 temp mancal\", \"Ug2 temp mancal\", \"Ug1 perda grade\", \"Ug2 perda grade\"]}}]',7,1),(129,'2021-03-09 19:15:47.927592','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Timestamp\", \"Kie\", \"Nv montante\", \"Ug1 pot\", \"Ug1 tempo\", \"Ug2 tempo\", \"Ug1 temp mancal\", \"Ug2 temp mancal\", \"Ug1 perda grade\", \"Ug2 perda grade\"]}}]',7,1),(130,'2021-03-09 19:25:20.201600','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Timestamp\", \"Margem pot critica\", \"Nv montante\", \"Ug1 pot\", \"Ug1 setpot\", \"Ug1 tempo\", \"Ug2 setpot\", \"Ug2 tempo\", \"Ug1 temp mancal\", \"Ug2 temp mancal\", \"Ug1 perda grade\", \"Ug2 perda grade\"]}}]',7,1),(131,'2021-03-09 19:25:40.278722','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Timestamp\", \"Ug1 pot\", \"Ug1 tempo\", \"Ug2 setpot\", \"Ug2 tempo\", \"Valor ie inicial\", \"Ug1 temp mancal\", \"Ug2 temp mancal\", \"Ug1 perda grade\", \"Ug2 perda grade\"]}}]',7,1),(132,'2021-03-09 19:46:07.790652','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Timestamp\", \"Kp\", \"Ki\", \"Kie\", \"Nv montante\", \"Ug1 pot\", \"Ug1 setpot\", \"Ug1 sinc\", \"Ug1 tempo\", \"Ug2 pot\", \"Ug2 setpot\", \"Ug2 sinc\", \"Ug2 tempo\", \"Ug1 temp mancal\", \"Ug2 temp mancal\", \"Ug1 perda grade\", \"Ug2 perda grade\"]}}]',7,1),(133,'2021-03-17 18:19:04.368567','1','ParametrosUsina object (1)',2,'[{\"changed\": {\"fields\": [\"Ug1 temp alerta\", \"Ug2 temp alerta\", \"Ug1 perda grade alerta\", \"Ug2 perda grade alerta\", \"Ug1 perda grade maxima\", \"Ug2 perda grade maxima\"]}}]',7,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(9,'agendamentos','agendamento'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(10,'parametros_moa','comando'),(8,'parametros_moa','contato'),(7,'parametros_moa','parametrosusina'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2021-01-27 19:18:57.895149'),(2,'auth','0001_initial','2021-01-27 19:18:58.027539'),(3,'admin','0001_initial','2021-01-27 19:18:58.365404'),(4,'admin','0002_logentry_remove_auto_add','2021-01-27 19:18:58.471575'),(5,'admin','0003_logentry_add_action_flag_choices','2021-01-27 19:18:58.491892'),(6,'contenttypes','0002_remove_content_type_name','2021-01-27 19:18:58.570510'),(7,'auth','0002_alter_permission_name_max_length','2021-01-27 19:18:58.622941'),(8,'auth','0003_alter_user_email_max_length','2021-01-27 19:18:58.657142'),(9,'auth','0004_alter_user_username_opts','2021-01-27 19:18:58.666750'),(10,'auth','0005_alter_user_last_login_null','2021-01-27 19:18:58.694168'),(11,'auth','0006_require_contenttypes_0002','2021-01-27 19:18:58.698201'),(12,'auth','0007_alter_validators_add_error_messages','2021-01-27 19:18:58.709387'),(13,'auth','0008_alter_user_username_max_length','2021-01-27 19:18:58.752190'),(14,'auth','0009_alter_user_last_name_max_length','2021-01-27 19:18:58.785470'),(15,'auth','0010_alter_group_name_max_length','2021-01-27 19:18:58.800993'),(16,'auth','0011_update_proxy_permissions','2021-01-27 19:18:58.808584'),(17,'auth','0012_alter_user_first_name_max_length','2021-01-27 19:18:58.847209'),(18,'sessions','0001_initial','2021-01-27 19:18:58.868899'),(19,'parametros_moa','0001_initial','2021-02-01 18:28:20.521642'),(20,'parametros_moa','0002_auto_20210201_1600','2021-02-01 19:00:59.923439'),(21,'parametros_moa','0003_parametrosusina_timestamp','2021-02-03 17:31:24.538232'),(22,'parametros_moa','0004_parametrosusina_emergencia_moa','2021-02-03 17:53:55.661094'),(23,'parametros_moa','0005_parametrosusina_modo_autonomo','2021-02-03 19:13:26.204607'),(24,'parametros_moa','0006_contato','2021-02-08 18:58:05.267544'),(25,'parametros_moa','0007_auto_20210208_1802','2021-02-08 21:02:22.328348'),(26,'parametros_moa','0008_auto_20210209_0110','2021-02-09 04:10:27.247157'),(27,'parametros_moa','0009_parametrosusina_status_moa','2021-02-09 04:27:10.015193'),(28,'parametros_moa','0010_auto_20210216_1511','2021-02-16 18:11:35.415593'),(29,'parametros_moa','0011_auto_20210216_1536','2021-02-16 18:37:02.073889'),(30,'parametros_moa','0012_parametrosusina_modo_de_escolha_das_ugs','2021-02-16 18:38:50.606034'),(31,'agendamentos','0001_initial','2021-02-17 17:38:00.131976'),(32,'parametros_moa','0013_comando','2021-02-18 18:45:10.984254'),(33,'agendamentos','0002_auto_20210218_1641','2021-02-18 19:41:44.839477'),(34,'agendamentos','0003_agendamento_executado','2021-02-19 18:13:53.331684'),(35,'parametros_moa','0002_auto_20210222_1605','2021-02-22 19:05:42.095654'),(36,'parametros_moa','0003_auto_20210222_1610','2021-02-22 19:10:23.368869'),(37,'parametros_moa','0004_auto_20210303_1459','2021-03-03 18:00:08.751978'),(38,'parametros_moa','0005_auto_20210303_1517','2021-03-03 18:17:18.351292'),(39,'parametros_moa','0006_auto_20210304_1514','2021-03-04 18:14:49.221733'),(40,'parametros_moa','0007_parametrosusina_tolerancia_pot_maxima','2021-03-04 18:50:01.518883'),(41,'parametros_moa','0008_auto_20210305_1459','2021-03-05 17:59:59.249922'),(42,'parametros_moa','0009_auto_20210305_1508','2021-03-05 18:08:59.066951'),(43,'parametros_moa','0010_parametrosusina_pot_maxima_alvo','2021-03-08 19:07:42.808612'),(44,'parametros_moa','0011_auto_20210317_1516','2021-03-17 18:16:37.263510');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('ch5682nlucjv64eosd5lugk58k3fyjlk','.eJxVjEEOwiAQRe_C2hAY2gFcuu8ZyMCgVA0kpV0Z765NutDtf-_9lwi0rSVsPS9hZnEWWpx-t0jpkesO-E711mRqdV3mKHdFHrTLqXF-Xg7376BQL9-aBuMN2jHq0ahkHBMA2wwA0TjNiFlbf3U4qKTQeA2Kox_AKWTKhFa8P7JENqo:1lHWcd:XjqsMuZLjXLYXyrmkJX6swIfRG39ysUgAg55oidQztY','2021-03-17 18:53:23.987716'),('g4xvr2xlnuijteadgfz823ib0d7mv3yl','.eJxVjEEOwiAQRe_C2hAY2gFcuu8ZyMCgVA0kpV0Z765NutDtf-_9lwi0rSVsPS9hZnEWWpx-t0jpkesO-E711mRqdV3mKHdFHrTLqXF-Xg7376BQL9-aBuMN2jHq0ahkHBMA2wwA0TjNiFlbf3U4qKTQeA2Kox_AKWTKhFa8P7JENqo:1l9tPs:3kknlMsgEFKoLNe08SDd4mYwlXw24arVne12tCZOL-Q','2021-02-24 17:36:40.781465'),('m2vkha4puuvkeep8t72r2ymqagutqybt','.eJxVjEEOwiAQRe_C2hAY2gFcuu8ZyMCgVA0kpV0Z765NutDtf-_9lwi0rSVsPS9hZnEWWpx-t0jpkesO-E711mRqdV3mKHdFHrTLqXF-Xg7376BQL9-aBuMN2jHq0ahkHBMA2wwA0TjNiFlbf3U4qKTQeA2Kox_AKWTKhFa8P7JENqo:1lMypW:gvJE2vIHikh_eAGjnNq0mMRRyjbPZaB5gX7XnZDp_y4','2021-04-01 20:01:14.697933'),('naiuff3c4whoc6jmqfke3oo31tk264yt','.eJxVjEEOwiAQRe_C2hAY2gFcuu8ZyMCgVA0kpV0Z765NutDtf-_9lwi0rSVsPS9hZnEWWpx-t0jpkesO-E711mRqdV3mKHdFHrTLqXF-Xg7376BQL9-aBuMN2jHq0ahkHBMA2wwA0TjNiFlbf3U4qKTQeA2Kox_AKWTKhFa8P7JENqo:1lMz2K:7_M2-xXYaBgUJ7Uokq4CWABGb_Ks7F-ct51GlOlAjjo','2021-04-01 20:14:28.178783'),('pbdrqckqyzyk79p52ktxf6dks0rff384','.eJxVjEEOwiAQRe_C2hAY2gFcuu8ZyMCgVA0kpV0Z765NutDtf-_9lwi0rSVsPS9hZnEWWpx-t0jpkesO-E711mRqdV3mKHdFHrTLqXF-Xg7376BQL9-aBuMN2jHq0ahkHBMA2wwA0TjNiFlbf3U4qKTQeA2Kox_AKWTKhFa8P7JENqo:1l7k3U:szPUNwH3ey9LmbG4LXRMJjwcQyhYIyRdPdeZzH87jcs','2021-02-18 19:12:40.446858'),('wj78kio75m6gltu6mcrdi99c9aev113y','.eJxVjEEOwiAQRe_C2hAY2gFcuu8ZyMCgVA0kpV0Z765NutDtf-_9lwi0rSVsPS9hZnEWWpx-t0jpkesO-E711mRqdV3mKHdFHrTLqXF-Xg7376BQL9-aBuMN2jHq0ahkHBMA2wwA0TjNiFlbf3U4qKTQeA2Kox_AKWTKhFa8P7JENqo:1l9BmP:k27tFclIJFObLl_BMNAL2H1AlDa0Jwql7sRisnCNl_Y','2021-02-22 19:01:01.396443');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `parametros_moa_comando`
--

DROP TABLE IF EXISTS `parametros_moa_comando`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `parametros_moa_comando` (
  `id` int NOT NULL,
  `nome` varchar(255) NOT NULL,
  `descricao` longtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `parametros_moa_comando`
--

LOCK TABLES `parametros_moa_comando` WRITE;
/*!40000 ALTER TABLE `parametros_moa_comando` DISABLE KEYS */;
INSERT INTO `parametros_moa_comando` VALUES (1,'Resetar parâmetors','Reseta os parâmetors para os valores padrões'),(2,'Indisponibilizar Usina','Indisponibiliza a usina enviando um comando de emergência para a CLP'),(3,'Normalizar Usina','Manda o comando para a CLP normalizar a usina (Todas as UGs, et.)'),(10,'Indisponibilizar UG 1','Indisponibiliza a UG1 enviando um comando para a CLP'),(11,'Normalizar UG 1','Normaliza a UG1 enviando um comando para a CLP'),(20,'Indisponibilizar UG 2','Indisponibiliza a UG2 enviando um comando para a CLP'),(21,'Normalizar UG 2','Normaliza a UG2 enviando um comando para a CLP');
/*!40000 ALTER TABLE `parametros_moa_comando` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `parametros_moa_contato`
--

DROP TABLE IF EXISTS `parametros_moa_contato`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `parametros_moa_contato` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(250) NOT NULL,
  `numero` varchar(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `parametros_moa_contato`
--

LOCK TABLES `parametros_moa_contato` WRITE;
/*!40000 ALTER TABLE `parametros_moa_contato` DISABLE KEYS */;
INSERT INTO `parametros_moa_contato` VALUES (1,'Lucas Lavratti','41988591567'),(2,'DEBUG MOA','0'),(3,'Henrique TESTE Helmuth Kreutz Pfeifer','41999610053');
/*!40000 ALTER TABLE `parametros_moa_contato` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `parametros_moa_parametrosusina`
--

DROP TABLE IF EXISTS `parametros_moa_parametrosusina`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `parametros_moa_parametrosusina` (
  `id` int NOT NULL AUTO_INCREMENT,
  `clp_ip` varchar(15) NOT NULL,
  `clp_porta` int NOT NULL,
  `modbus_server_ip` varchar(15) NOT NULL,
  `modbus_server_porta` int NOT NULL,
  `kp` decimal(15,10) NOT NULL,
  `ki` decimal(15,10) NOT NULL,
  `kd` decimal(15,10) NOT NULL,
  `kie` decimal(15,10) NOT NULL,
  `margem_pot_critica` decimal(10,5) NOT NULL,
  `n_movel_L` int NOT NULL,
  `n_movel_R` int NOT NULL,
  `nv_alvo` decimal(10,3) NOT NULL,
  `nv_maximo` decimal(10,3) NOT NULL,
  `nv_minimo` decimal(10,3) NOT NULL,
  `nv_montante` decimal(10,3) NOT NULL,
  `nv_religamento` decimal(10,3) NOT NULL,
  `pot_minima` decimal(10,5) NOT NULL,
  `pot_nominal` decimal(10,5) NOT NULL,
  `pot_nominal_ug` decimal(10,5) NOT NULL,
  `pot_disp` decimal(10,5) NOT NULL,
  `timer_erro` int NOT NULL,
  `ug1_disp` decimal(10,5) NOT NULL,
  `ug1_pot` decimal(10,5) NOT NULL,
  `ug1_setpot` decimal(10,5) NOT NULL,
  `ug2_disp` decimal(10,5) NOT NULL,
  `ug2_pot` decimal(10,5) NOT NULL,
  `ug2_setpot` decimal(10,5) NOT NULL,
  `valor_ie_inicial` decimal(10,5) NOT NULL,
  `aguardando_reservatorio` int NOT NULL,
  `clp_online` int NOT NULL,
  `ug1_sinc` int NOT NULL,
  `ug2_sinc` int NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `emergencia_acionada` int NOT NULL,
  `modo_autonomo` int NOT NULL,
  `ug1_tempo` int NOT NULL,
  `ug2_tempo` int NOT NULL,
  `status_moa` int NOT NULL,
  `ug1_prioridade` int NOT NULL,
  `ug2_prioridade` int NOT NULL,
  `modo_de_escolha_das_ugs` int NOT NULL,
  `pos_comporta` int NOT NULL,
  `nv_comporta_pos_0_ant` decimal(10,2) NOT NULL,
  `nv_comporta_pos_0_prox` decimal(10,2) NOT NULL,
  `nv_comporta_pos_1_ant` decimal(10,2) NOT NULL,
  `nv_comporta_pos_1_prox` decimal(10,2) NOT NULL,
  `nv_comporta_pos_2_ant` decimal(10,2) NOT NULL,
  `nv_comporta_pos_2_prox` decimal(10,2) NOT NULL,
  `nv_comporta_pos_3_ant` decimal(10,2) NOT NULL,
  `nv_comporta_pos_3_prox` decimal(10,2) NOT NULL,
  `nv_comporta_pos_4_ant` decimal(10,2) NOT NULL,
  `nv_comporta_pos_4_prox` decimal(10,2) NOT NULL,
  `nv_comporta_pos_5_ant` decimal(10,2) NOT NULL,
  `nv_comporta_pos_5_prox` decimal(10,2) NOT NULL,
  `tolerancia_pot_maxima` decimal(10,5) NOT NULL,
  `ug1_perda_grade` decimal(10,3) NOT NULL,
  `ug1_perda_grade_maxima` decimal(10,3) NOT NULL,
  `ug1_temp_mancal` decimal(10,2) NOT NULL,
  `ug1_temp_maxima` decimal(10,2) NOT NULL,
  `ug2_perda_grade` decimal(10,3) NOT NULL,
  `ug2_perda_grade_maxima` decimal(10,3) NOT NULL,
  `ug2_temp_mancal` decimal(10,2) NOT NULL,
  `ug2_temp_maxima` decimal(10,2) NOT NULL,
  `pot_maxima_alvo` decimal(10,5) NOT NULL,
  `ug1_perda_grade_alerta` decimal(10,3) NOT NULL,
  `ug1_temp_alerta` decimal(10,2) NOT NULL,
  `ug2_perda_grade_alerta` decimal(10,3) NOT NULL,
  `ug2_temp_alerta` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `parametros_moa_parametrosusina`
--

LOCK TABLES `parametros_moa_parametrosusina` WRITE;
/*!40000 ALTER TABLE `parametros_moa_parametrosusina` DISABLE KEYS */;
INSERT INTO `parametros_moa_parametrosusina` VALUES (1,'172.21.15.13',502,'172.21.15.12',5002,-40.0000000000,-0.0150000000,-100.0000000000,0.0800000000,1.00000,60,6,643.250,643.500,643.000,643.550,643.250,1.00000,5.00000,2.50000,5.20000,30,1.00000,1.45500,1.45600,1.00000,2.60000,2.60000,0.30000,0,1,1,1,'2021-03-19 16:37:57.000000',0,1,23,23,5,0,0,1,1,0.00,643.55,643.50,643.60,643.55,643.65,643.60,643.70,643.65,643.75,643.70,1000.00,1.04000,0.390,10.000,83.20,100.00,0.470,10.000,79.30,95.00,5.00000,3.000,70.00,3.000,85.00);
/*!40000 ALTER TABLE `parametros_moa_parametrosusina` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-03-19 16:37:59
