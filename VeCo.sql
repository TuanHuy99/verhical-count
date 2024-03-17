-- MySQL dump 10.13  Distrib 8.0.33, for Win64 (x86_64)
--
-- Host: localhost    Database: veco
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
-- Table structure for table `downloaded`
--

DROP TABLE IF EXISTS `downloaded`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `downloaded` (
  `link` text NOT NULL,
  `type` varchar(45) DEFAULT NULL,
  `project_id` varchar(45) DEFAULT NULL,
  `time_downloaded` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `downloaded`
--

LOCK TABLES `downloaded` WRITE;
/*!40000 ALTER TABLE `downloaded` DISABLE KEYS */;
INSERT INTO `downloaded` VALUES ('C:/Users/vutua/Workspace/TL-tech/Verhical_count/yolo8_json/video_path/video_path.zip','zip','prsx7','2023-06-27 14:34:20'),('C:/Users/vutua/Workspace/TL-tech/Verhical_count/yolo8_json/video_path/video_path.zip','zip','xd64f','2023-06-27 14:36:18'),('C:/Users/vutua/Workspace/TL-tech/Verhical_count/yolo8_json/video_path/video_path.zip','zip','my1dq','2023-06-27 14:37:21'),('C:/Users/vutua/Workspace/TL-tech/Verhical_count/yolo8_json/video_path/video_path.zip','zip','xiz5y','2023-06-27 14:39:34'),('C:/Users/vutua/Workspace/TL-tech/Verhical_count/yolo8_json/video_path/video_path.zip','zip','o3xzb','2023-06-27 14:39:56'),('C:/Users/vutua/Workspace/TL-tech/Verhical_count/yolo8_json/video_path/video_path.zip','zip','g8oxz','2023-06-27 14:43:15'),('C:/Users/vutua/Workspace/TL-tech/Verhical_count/yolo8_json/video_path/video path.zip','zip','89sig','2023-06-27 16:19:27');
/*!40000 ALTER TABLE `downloaded` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `error_link`
--

DROP TABLE IF EXISTS `error_link`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `error_link` (
  `link` text NOT NULL,
  `name` text,
  `id` varchar(45) DEFAULT NULL,
  `user` varchar(45) DEFAULT NULL,
  `upload_time` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `error_link`
--

LOCK TABLES `error_link` WRITE;
/*!40000 ALTER TABLE `error_link` DISABLE KEYS */;
INSERT INTO `error_link` VALUES ('ewrwerwer','err 1','jw029','test1','2023-06-26 15:16:51'),('asdasdasd','err 2','1enuo','test1','2023-06-26 15:17:23'),('123456','err 3','f9q3t','test1','2023-06-26 15:21:40'),('hgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhgdsvfgrdsvhsdgfekhrvdvvvvvvvhsdgfekhrvdvvvvvvv','er 5','w2zpk','test1','2023-06-26 17:20:12'),('None','zip 1','a83ri','test1','2023-06-27 14:30:16'),('None','zip 1','io9oj','test1','2023-06-27 14:32:15'),('None','zip 1','t1roq','test1','2023-06-27 14:32:48'),('C:UsersvutuaWorkspaceTL-techVerhical_countyolo8_jsonvideo_pathvideo_path.zip','zip 1','6kzje','test1','2023-06-27 14:33:30'),('C:/Users/vutua/Workspace/TL-tech/Verhical_count/yolo8_json/video_path/video_path.zip','zip 1','xiz5y','test1','2023-06-27 14:39:34'),('C:/Users/vutua/Workspace/TL-tech/Verhical_count/yolo8_json/video_path/video_path.zip','zip 1','o3xzb','test1','2023-06-27 14:39:56');
/*!40000 ALTER TABLE `error_link` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `login`
--

DROP TABLE IF EXISTS `login`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `login` (
  `userName` varchar(100) NOT NULL,
  `passWord` varchar(45) DEFAULT NULL,
  `Role` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`userName`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `login`
--

LOCK TABLES `login` WRITE;
/*!40000 ALTER TABLE `login` DISABLE KEYS */;
INSERT INTO `login` VALUES ('huy.vt','12345','Admin'),('huy.vt3','c20ad4d76fe97759aa27a0c99bff6710','user'),('test1','12','user'),('test2','123','user'),('test3','1234','user');
/*!40000 ALTER TABLE `login` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `need_download`
--

DROP TABLE IF EXISTS `need_download`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `need_download` (
  `link` text NOT NULL,
  `type` varchar(45) DEFAULT NULL,
  `name` text,
  `num_class` int DEFAULT NULL,
  `day_upload` datetime DEFAULT NULL,
  `user` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `need_download`
--

LOCK TABLES `need_download` WRITE;
/*!40000 ALTER TABLE `need_download` DISABLE KEYS */;
/*!40000 ALTER TABLE `need_download` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `processed`
--

DROP TABLE IF EXISTS `processed`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `processed` (
  `userName` varchar(100) DEFAULT NULL,
  `projectID` varchar(100) DEFAULT NULL,
  `dateUse` datetime DEFAULT NULL,
  `result` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `processed`
--

LOCK TABLES `processed` WRITE;
/*!40000 ALTER TABLE `processed` DISABLE KEYS */;
INSERT INTO `processed` VALUES ('test2','1s_test_name_p4eiq','2023-05-11 00:35:27','3 0 0 0 0'),('test2','1s_test_name_p4eiq','2023-05-11 00:35:54','2 0 0 0 0');
/*!40000 ALTER TABLE `processed` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `processing`
--

DROP TABLE IF EXISTS `processing`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `processing` (
  `project_id` varchar(10) NOT NULL,
  `num_class` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `processing`
--

LOCK TABLES `processing` WRITE;
/*!40000 ALTER TABLE `processing` DISABLE KEYS */;
/*!40000 ALTER TABLE `processing` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `projects`
--

DROP TABLE IF EXISTS `projects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `projects` (
  `projectID` varchar(45) NOT NULL,
  `uploadDay` datetime DEFAULT NULL,
  `numVideo` int DEFAULT NULL,
  `size` float DEFAULT NULL,
  `owner` varchar(100) DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`projectID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `projects`
--

LOCK TABLES `projects` WRITE;
/*!40000 ALTER TABLE `projects` DISABLE KEYS */;
INSERT INTO `projects` VALUES ('0hrj6','2023-06-11 15:32:01',0,25,'test2','Thư mục 1'),('1cs33','2023-06-07 14:34:23',1,0.109,'test3','Test Drop Box 3'),('2eav8','2023-06-07 14:20:12',0,0,'test3','Test Upload File'),('2jz35','2023-06-17 11:23:18',2,0.002,'test1','Drive 9'),('3lwpd','2023-06-16 15:49:00',2,0.002,'test1','Drive 1'),('3v1oa','2023-06-07 14:21:49',0,0,'test3','Test Upload File'),('4bhef','2023-06-07 09:01:36',1,0.009,'test3','Test Drop Box 5s'),('5nm8m','2023-06-16 15:29:46',2,0.002,'test1','Drive 1'),('5xgyi','2023-06-07 15:04:48',1,0.001,'test3','Huy test upload file'),('6nnj2','2023-06-13 22:40:58',1,0.001,'test3','Tessst'),('6zue7','2023-06-16 15:40:03',2,0.002,'test1','Drive 1'),('7wxmf','2023-06-16 16:44:24',1,0.429,'test1','hello'),('89sig','2023-06-27 16:19:27',2,0.002,'test1','zip 2'),('8rdxw','2023-05-11 15:07:23',2,0.002,'test3','Thư mục 1'),('8vpih','2023-06-16 15:25:46',2,0.002,'test1','Drive 1'),('9rqf8','2023-06-07 14:22:27',0,0,'test3','Test Upload File'),('abpzh','2023-06-12 14:49:52',1,0.009,'test2','Thư mục 1'),('b3y1b','2023-06-11 14:49:17',1,0.009,'test3','Test 5 Class'),('cfrd2','2023-06-19 17:15:25',2,0.002,'test3','Hello'),('dr6iv','2023-06-16 15:43:15',2,0.002,'test1','Drive 1'),('f4a8m','2023-05-12 15:41:34',1,0.001,'test1','Thư mục 1'),('flqlw','2023-06-16 15:56:06',2,0.002,'test1','Drive 1'),('g8omy','2023-06-17 11:19:16',2,0.002,'test1','Drive 1'),('g8oxz','2023-06-27 14:43:15',2,0.002,'test1','zip 1'),('gphdu','2023-05-10 23:54:32',2,0.002,'test3','Thư mục 2'),('grtni','2023-06-11 14:54:06',1,0.009,'test3','Test 5 Class'),('gzday','2023-06-07 14:26:30',1,0.001,'test3','Thư mục 2'),('hvt9b','2023-05-12 15:52:48',1,0.001,'test2','hek'),('imsbt','2023-06-07 10:31:44',1,0.109,'test3','Thư mục 2'),('j2ht7','2023-06-06 22:05:20',1,0.109,'test3','Test Drop Box'),('j9gb8','2023-05-12 15:50:42',1,0.001,'test2','skdjngkjsnd.sdglijsdk0349865039890'),('jc0so','2023-06-17 11:15:27',2,0.002,'test1','Drive 1'),('jnh7q','2023-06-11 15:30:44',0,0,'test2','Thầy Thiện 2'),('ljwkn','2023-05-12 15:57:28',1,0.001,'test1','asfasfhbjakshfiuashfkiuahsifu'),('m62i7','2023-06-20 08:29:51',2,0.002,'test3','Hello'),('mgj5t','2023-06-17 11:20:20',2,0.002,'test1','Drive 3'),('mruet','2023-05-12 15:59:00',1,0.001,'test1','s51dgsdjg'),('nfse9','2023-06-17 11:28:42',1,0.009,'test1','Dropbox 1'),('nkaj8','2023-06-09 11:22:40',1,0.001,'test3','Thư mục 1'),('npwl0','2023-06-17 11:21:27',2,0.002,'test1','Drive 5'),('o0dop','2023-06-07 14:25:36',0,0,'test3','Thư mục 1'),('ob285','2023-06-12 16:43:21',2,0.002,'test2','GG Drive 1'),('pw54i','2023-06-11 15:33:06',0,0,'test2','Test 5 Class'),('q7u6g','2023-06-11 14:53:00',1,0.109,'test3','Test 5 Class'),('qxlaa','2023-06-11 15:35:47',0,0,'test2','Thư mục 6'),('r0b8r','2023-06-17 11:22:23',2,0.002,'test1','Drive 7'),('rkimy','2023-06-17 11:32:08',1,0.009,'test1','Dropbox 2'),('rtrvi','2023-06-06 22:57:00',1,0.109,'test3','Test Drop Box'),('ry8ia','2023-06-12 14:46:50',1,0.009,'test2','Thư mục 2'),('s10g0','2023-06-16 15:33:51',2,0.002,'test1','Drive 1'),('sff7m','2023-06-11 15:33:46',0,0,'test2','Thư mục 5'),('sfzyo','2023-06-07 08:56:11',1,0.109,'test3','Test Drop Box'),('szndn','2023-05-11 10:30:45',3,0.011,'test3','Thư mục 2'),('t0l8r','2023-06-16 16:37:02',1,0.429,'test1','hello'),('t2zch','2023-05-12 15:54:39',1,0.001,'test1','mcdgbksdjn'),('tvir1','2023-06-11 14:48:12',1,0.009,'test3','Test 5 Class'),('ugfqt','2023-06-11 15:39:08',3,1.246,'test2','Thư mục 7'),('ur95m','2023-06-16 16:42:26',2,0.002,'test1','short'),('us40m','2023-06-07 15:05:06',1,0.001,'test3','Huy test upload file'),('vfh21','2023-06-11 15:13:22',1,0.009,'test3','Test 5 Class 1'),('vmbbm','2023-06-11 15:25:37',1,0.001,'test3','Thư mục 2'),('vqvwo','2023-06-11 15:27:51',0,0,'test2','Thầy Thiện 1'),('xg3lo','2023-06-07 08:55:42',1,0.109,'test3','Test Drop Box'),('xqvl1','2023-05-12 15:55:59',1,0.001,'test1','asfasfhbjakshfiuashfkiuahsifu'),('z5h1h','2023-05-11 10:30:08',3,0.011,'test3','Thư mục 2'),('zhgr5','2023-06-16 15:51:36',2,0.002,'test1','Drive 2');
/*!40000 ALTER TABLE `projects` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `videos`
--

DROP TABLE IF EXISTS `videos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `videos` (
  `projectID` varchar(45) NOT NULL,
  `videoname` varchar(45) DEFAULT NULL,
  `size` float DEFAULT NULL,
  `frames` int DEFAULT NULL,
  `fps` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `videos`
--

LOCK TABLES `videos` WRITE;
/*!40000 ALTER TABLE `videos` DISABLE KEYS */;
INSERT INTO `videos` VALUES ('gphdu','1s.mp4',0.001,30,31.0345),('gphdu','1s13f.mp4',0.001,13,32.5),('z5h1h','1s.mp4',0.001,30,31.0345),('z5h1h','1s13f.mp4',0.001,13,32.5),('z5h1h','test 5s.mp4',0.009,151,30.2),('szndn','1s.mp4',0.001,30,31.0345),('szndn','1s13f.mp4',0.001,13,32.5),('szndn','test 5s.mp4',0.009,151,30.2),('8rdxw','1s.mp4',0.001,30,31.0345),('8rdxw','1s13f.mp4',0.001,13,32.5),('f4a8m','1s13f.mp4',0.001,13,32.5),('j9gb8','1s13f.mp4',0.001,13,32.5),('hvt9b','1s13f.mp4',0.001,13,32.5),('t2zch','1s.mp4',0.001,30,31.0345),('xqvl1','1s13f.mp4',0.001,13,32.5),('ljwkn','1s13f.mp4',0.001,13,32.5),('mruet','1s13f.mp4',0.001,13,32.5),('j2ht7','sence1_1p.mp4',0.109,1804,30.0166),('rtrvi','sence1_1p.mp4',0.109,1804,30.0166),('xg3lo','sence1_1p.mp4',0.109,1804,30.0166),('sfzyo','sence1_1p.mp4',0.109,1804,30.0166),('4bhef','test 5s.mp4',0.009,151,30.2),('imsbt','sence1_1p.mp4',0.109,1804,30.0166),('gzday','1s13f.mp4',0.001,13,32.5),('1cs33','sence1_1p.mp4',0.109,1804,30.0166),('5xgyi','1s.mp4',0.001,30,31.0345),('us40m','1s.mp4',0.001,30,31.0345),('nkaj8','1s13f.mp4',0.001,13,32.5),('tvir1','test 5s.mp4',0.009,151,30.2),('b3y1b','test 5s.mp4',0.009,151,30.2),('q7u6g','sence1_1p.mp4',0.109,1804,30.0166),('grtni','test 5s.mp4',0.009,151,30.2),('vfh21','test 5s.mp4',0.009,151,30.2),('vmbbm','1s13f.mp4',0.001,13,32.5),('ugfqt','20230405_093751_048.MP4',0.416,18000,30),('ugfqt','20230405_094751_049.MP4',0.415,18000,30),('ugfqt','20230405_095751_050.MP4',0.415,18000,30),('ry8ia','test 5s.mp4',0.009,151,30.2),('abpzh','test 5s.mp4',0.009,151,30.2),('ob285','1s.mp4',0.001,30,31.0345),('ob285','1s13f.mp4',0.001,13,32.5),('6nnj2','1s13f.mp4',0.001,13,32.5),('8vpih','1s.mp4',0.001,30,31.0345),('8vpih','1s13f.mp4',0.001,13,32.5),('5nm8m','1s.mp4',0.001,30,31.0345),('5nm8m','1s13f.mp4',0.001,13,32.5),('s10g0','1s.mp4',0.001,30,31.0345),('s10g0','1s13f.mp4',0.001,13,32.5),('6zue7','1s.mp4',0.001,30,31.0345),('6zue7','1s13f.mp4',0.001,13,32.5),('dr6iv','1s.mp4',0.001,30,31.0345),('dr6iv','1s13f.mp4',0.001,13,32.5),('3lwpd','1s.mp4',0.001,30,31.0345),('3lwpd','1s13f.mp4',0.001,13,32.5),('zhgr5','1s.mp4',0.001,30,31.0345),('zhgr5','1s13f.mp4',0.001,13,32.5),('flqlw','1s.mp4',0.001,30,31.0345),('flqlw','1s13f.mp4',0.001,13,32.5),('t0l8r','videotest3.mp4',0.429,7201,30.0042),('ur95m','1s.mp4',0.001,30,31.0345),('ur95m','1s13f.mp4',0.001,13,32.5),('7wxmf','videotest3.mp4',0.429,7201,30.0042),('jc0so','1s.mp4',0.001,30,31.0345),('jc0so','1s13f.mp4',0.001,13,32.5),('g8omy','1s.mp4',0.001,30,31.0345),('g8omy','1s13f.mp4',0.001,13,32.5),('mgj5t','1s.mp4',0.001,30,31.0345),('mgj5t','1s13f.mp4',0.001,13,32.5),('npwl0','1s.mp4',0.001,30,31.0345),('npwl0','1s13f.mp4',0.001,13,32.5),('r0b8r','1s.mp4',0.001,30,31.0345),('r0b8r','1s13f.mp4',0.001,13,32.5),('2jz35','1s.mp4',0.001,30,31.0345),('2jz35','1s13f.mp4',0.001,13,32.5),('nfse9','test 5s.mp4',0.009,151,30.2),('rkimy','test 5s.mp4',0.009,151,30.2),('m62i7','1s.mp4',0.001,30,31.0345),('m62i7','1s13f.mp4',0.001,13,32.5),('cfrd2','1s.mp4',0.001,30,31.0345),('cfrd2','1s13f.mp4',0.001,13,32.5),('7gp3k','videotest3.mp4',0.429,7201,30.0042),('7gp3k','raw_img.jpg',0.001,1,25),('7gp3k','track',0,0,0),('7gp3k','videotest3.mp4',0.429,7201,30.0042),('m62i7','1s.mp4',0.001,30,31.0345),('m62i7','1s13f.mp4',0.001,13,32.5),('m62i7','data_point_5.json',0,0,0),('m62i7','line_road_5.jpg',0,1,25),('m62i7','raw_img.jpg',0,1,25),('m62i7','track',0,0,0),('m62i7','track2',0,0,0),('m62i7','1s.mp4',0.001,30,31.0345),('m62i7','1s13f.mp4',0.001,13,32.5),('m62i7','data_point_5.json',0,0,0),('m62i7','data_point_9.json',0,0,0),('m62i7','line_road_5.jpg',0,1,25),('m62i7','line_road_9.jpg',0,1,25),('m62i7','raw_img.jpg',0,1,25),('m62i7','track',0,0,0),('m62i7','track2',0,0,0),('m62i7','track3',0,0,0),('m62i7','track4',0,0,0),('m62i7','1s.mp4',0.001,30,31.0345),('m62i7','1s13f.mp4',0.001,13,32.5),('m62i7','data_point_5.json',0,0,0),('m62i7','data_point_9.json',0,0,0),('m62i7','line_road_5.jpg',0,1,25),('m62i7','line_road_9.jpg',0,1,25),('m62i7','raw_img.jpg',0,1,25),('m62i7','track',0,0,0),('m62i7','track2',0,0,0),('m62i7','track3',0,0,0),('m62i7','track4',0,0,0),('m62i7','track5',0,0,0),('m62i7','track6',0,0,0),('m62i7','1s.mp4',0.001,30,31.0345),('m62i7','1s13f.mp4',0.001,13,32.5),('m62i7','data_point_5.json',0,0,0),('m62i7','data_point_9.json',0,0,0),('m62i7','line_road_5.jpg',0,1,25),('m62i7','line_road_9.jpg',0,1,25),('m62i7','raw_img.jpg',0,1,25),('m62i7','track',0,0,0),('m62i7','track2',0,0,0),('m62i7','track3',0,0,0),('m62i7','track4',0,0,0),('m62i7','track5',0,0,0),('m62i7','track6',0,0,0),('m62i7','track7',0,0,0),('m62i7','track8',0,0,0),('7gp3k','raw_img.jpg',0.001,1,25),('7gp3k','track',0,0,0),('7gp3k','track2',0,0,0),('7gp3k','videotest3.mp4',0.429,7201,30.0042),('prsx7','1s.mp4',0.001,30,31.0345),('prsx7','1s13f.mp4',0.001,13,32.5),('my1dq','1s.mp4',0.001,30,31.0345),('my1dq','1s13f.mp4',0.001,13,32.5),('xiz5y','1s.mp4',0.001,30,31.0345),('xiz5y','1s13f.mp4',0.001,13,32.5),('o3xzb','1s.mp4',0.001,30,31.0345),('o3xzb','1s13f.mp4',0.001,13,32.5),('g8oxz','1s.mp4',0.001,30,31.0345),('g8oxz','1s13f.mp4',0.001,13,32.5),('89sig','1s.mp4',0.001,30,31.0345),('89sig','1s13f.mp4',0.001,13,32.5);
/*!40000 ALTER TABLE `videos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wait_list`
--

DROP TABLE IF EXISTS `wait_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `wait_list` (
  `project_id` varchar(45) NOT NULL,
  `num_class` int DEFAULT NULL,
  `time_create` datetime DEFAULT NULL,
  `user` varchar(45) DEFAULT NULL,
  `name` text CHARACTER SET armscii8 COLLATE armscii8_general_ci
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wait_list`
--

LOCK TABLES `wait_list` WRITE;
/*!40000 ALTER TABLE `wait_list` DISABLE KEYS */;
/*!40000 ALTER TABLE `wait_list` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-06-29 15:09:41
