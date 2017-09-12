-- MySQL dump 10.13  Distrib 5.7.19, for Linux (x86_64)
--
-- Host: localhost    Database: leverage_philly
-- ------------------------------------------------------
-- Server version	5.7.19-0ubuntu0.16.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `candidacy`
--

DROP TABLE IF EXISTS `candidacy`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `candidacy` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `candidate_id` int(11) NOT NULL,
  `race_id` int(11) NOT NULL,
  `candidacy_type` enum('incumbent','challenger') NOT NULL,
  `outcome` enum('won','lost') NOT NULL,
  PRIMARY KEY (`id`),
  KEY `candidate_id` (`candidate_id`),
  KEY `race_id` (`race_id`),
  KEY `candidacy_type` (`candidacy_type`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `candidacy`
--

LOCK TABLES `candidacy` WRITE;
/*!40000 ALTER TABLE `candidacy` DISABLE KEYS */;
INSERT INTO `candidacy` VALUES (1,90,27,'incumbent','lost'),(2,93,27,'incumbent','lost'),(3,94,28,'incumbent','lost'),(4,96,28,'incumbent','lost');
/*!40000 ALTER TABLE `candidacy` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `candidate`
--

DROP TABLE IF EXISTS `candidate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `candidate` (
  `id` int(4) unsigned NOT NULL AUTO_INCREMENT,
  `party_id` int(1) unsigned NOT NULL,
  `fec_id` char(9) DEFAULT NULL,
  `district` tinyint(3) unsigned NOT NULL,
  `name_first` varchar(128) NOT NULL,
  `name_middle` varchar(32) NOT NULL DEFAULT '',
  `name_last` varchar(32) NOT NULL,
  `name_suffix` varchar(8) NOT NULL DEFAULT '',
  `slug` varchar(64) NOT NULL,
  `website` varchar(128) NOT NULL DEFAULT '',
  `social_blob` text NOT NULL,
  `is_active` int(1) NOT NULL DEFAULT '1',
  `candidate_order` int(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `fec_id` (`fec_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=97 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `candidate`
--

LOCK TABLES `candidate` WRITE;
/*!40000 ALTER TABLE `candidate` DISABLE KEYS */;
INSERT INTO `candidate` VALUES (1,2,'',0,'Jim Kenney','','','','jim-kenney','','',1,0),(2,1,'',0,'Melissa Murray Bailey','','','','melissa-murray-bailey','','',1,0),(6,1,'',0,'Al Taubenberger','','','','al-taubenberger','','',1,0),(7,2,'',0,'Alan Domb','','','','alan-domb','','',1,0),(9,2,'',0,'Bill Greenlee','','','','bill-greenlee','','',1,0),(10,2,'',0,'Blondell Reynolds-Brown','','','','blondell-reynolds-brown','','',1,0),(11,1,'',0,'Dan Tinney','','','','dan-tinney','','',1,0),(12,2,'',0,'David Oh','','','','david-oh','','',1,0),(13,1,'',0,'Denny O\'Brien','','','','denny-o-brien','','',1,0),(14,2,'',0,'Derek Green','','','','derek-green','','',1,0),(15,2,'',0,'Helen Gym','','','','helen-gym','','',1,0),(17,5,'',0,'Kristin Combs','','','','kristin-combs','','',1,0),(19,1,'',0,'Terrence Tracy','','','','terrence-tracy','','',1,0),(20,2,'',1,'Mark Squilla','','','','mark-squilla','','',1,0),(21,2,'',2,'Kenyatta Johnson','','','','kenyatta-johnson','','',1,0),(22,2,'',3,'Jannie Blackwell','','','','jannie-blackwell','','',1,0),(23,2,'',4,'Curtis Jones','','','','curtis-jones','','',1,0),(24,2,'',5,'Darrell Clarke','','','','darrell-clarke','','',1,0),(25,2,'',6,'Bobby Henon','','','','bobby-henon','','',1,0),(26,2,'',7,'Maria Quinones-Sanchez','','','','maria-quinones-sanchez','','',1,0),(27,2,'',8,'Cindy Bass','','','','cindy-bass','','',1,0),(30,2,'',9,'Cherelle Parker','','','','cherelle-parker','','',1,0),(31,1,'',9,'Kevin Strickand','','','','kevin-strickand','','',1,0),(32,1,'',10,'Brian O\'Neill','','','','brian-o-neill','','',1,0),(33,2,'',0,'Dwayne Woodruff','','','','dwayne-woodruff','','',1,0),(34,1,'',0,'Sallie Mundy','','','','sallie-mundy','','',1,0),(35,2,'',0,'Carolyn H Nichols','','','','carolyn-h-nichols','','',1,0),(36,2,'',0,'Geoff Moulton','','','','geoff-moulton','','',1,0),(37,2,'',0,'Maria Mclaughlin','','','','maria-mclaughlin','','',1,0),(38,2,'',0,'Debbie Kunselman','','','','debbie-kunselman','','',1,0),(39,2,'',0,'Bill Caye','','','','bill-caye','','',1,0),(40,1,'',0,'Emil Giordano','','','','emil-giordano','','',1,0),(41,1,'',0,'Craig Stedman','','','','craig-stedman','','',1,0),(42,1,'',0,'Wade A Kagarise','','','','wade-a-kagarise','','',1,0),(43,1,'',0,'Mary Murray','','','','mary-murray','','',1,0),(44,1,'',0,'Paula A Patrick','','','','paula-a-patrick','','',1,0),(45,2,'',0,'Timothy Barry','','','','timothy-barry','','',1,0),(46,2,'',0,'Joe Cosgrove','','','','joe-cosgrove','','',1,0),(47,2,'',0,'Ellen Ceisler','','','','ellen-ceisler','','',1,0),(48,2,'',0,'Todd Eagen','','','','todd-eagen','','',1,0),(49,2,'',0,'Irene M Clark','','','','irene-m-clark','','',1,0),(50,2,'',0,'Bryan Barbin','','','','bryan-barbin','','',1,0),(51,1,'',0,'Paul Lalley','','','','paul-lalley','','',1,0),(52,1,'',0,'Christine Fizzano Cannon','','','','christine-fizzano-cannon','','',1,0),(53,2,'',0,'Stella Tsai','','','','stella-tsai','','',1,0),(54,2,'',0,'Vikki Kristiansson','','','','vikki-kristiansson','','',1,0),(55,2,'',0,'Deborah Cianfrani','','','','deborah-cianfrani','','',1,0),(56,2,'',0,'John Macoretta','','','','john-macoretta','','',1,0),(57,2,'',0,'Rania Major','','','','rania-major','','',1,0),(58,2,'',0,'Henry Mcgregor Sias','','','','henry-mcgregor-sias','','',1,0),(59,2,'',0,'Lawrence J Bozzelli','','','','lawrence-j-bozzelli','','',1,0),(61,2,'',0,'Brian Mclaughlin','','','','brian-mclaughlin','','',1,0),(62,2,'',0,'Shanese Johnson','','','','shanese-johnson','','',1,0),(63,2,'',0,'Mark B Cohen','','','','mark-b-cohen','','',1,0),(64,2,'',0,'Daniel R Sulman','','','','daniel-r-sulman','','',1,0),(65,2,'',0,'Leon Goodman','','','','leon-goodman','','',1,0),(66,2,'',0,'Deborah Canty','','','','deborah-canty','','',1,0),(67,2,'',0,'Wendi Barish','','','','wendi-barish','','',1,0),(68,2,'',0,'Leonard Deutchman','','','','leonard-deutchman','','',1,0),(69,2,'',0,'Zac Shaffer','','','','zac-shaffer','','',1,0),(70,2,'',0,'Jennifer Schultz','','','','jennifer-schultz','','',1,0),(71,2,'',0,'Vincent Melchiorre','','','','vincent-melchiorre','','',1,0),(74,2,'',0,'David Conroy','','','','david-conroy','','',1,0),(75,2,'',0,'Mark J Moore','','','','mark-j-moore','','',1,0),(76,2,'',0,'Danyl S Patterson','','','','danyl-s-patterson','','',1,0),(77,2,'',0,'Terri M Booker','','','','terri-m-booker','','',1,0),(78,2,'',0,'Lucretia C Clemons','','','','lucretia-c-clemons','','',1,0),(81,2,'',0,'Matt Wolf','','','','matt-wolf','','',1,0),(82,2,'',0,'Marissa Brumbach','','','','marissa-brumbach','','',1,0),(83,2,'',0,'George Twardy','','','','george-twardy','','',1,0),(84,2,'',0,'Sherman Toppin','','','','sherman-toppin','','',1,0),(85,2,'',0,'Crystal B Powell','','','','crystal-b-powell','','',1,0),(86,2,'',0,'Rich Negrin','','','','rich-negrin','','',1,0),(87,2,'',0,'Joe Khan','','','','joe-khan','','',1,0),(88,2,'',0,'Michael W Untermeyer','','','','michael-w-untermeyer','','',1,0),(89,2,'',0,'Tariq Karim El-Shabazz','','','','tariq-karim-el-shabazz','','',1,0),(90,2,'',0,'Lawrence S Krasner','','','','lawrence-s-krasner','','',1,0),(91,2,'',0,'Teresa Carr Deni','','','','teresa-carr-deni','','',1,0),(92,2,'',0,'John ONeill','','','','john-oneill','','',1,0),(93,1,'',0,'Beth Grossman','','','','beth-grossman','','',1,0),(94,2,'',0,'Rebecca Rhynhart','','','','rebecca-rhynhart','','',1,0),(95,2,'',0,'Alan L Butkovitz','','','','alan-l-butkovitz','','',1,0),(96,1,'',0,'Michael Tomlinson','','','','michael-tomlinson','','',1,0);
/*!40000 ALTER TABLE `candidate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `race`
--

DROP TABLE IF EXISTS `race`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `race` (
  `id` int(4) unsigned NOT NULL AUTO_INCREMENT,
  `election_type` enum('primary','general') NOT NULL,
  `election_year` year(4) NOT NULL,
  `election_date` int(11) NOT NULL,
  `seat_status` enum('filled','open seat','retired') NOT NULL,
  `race_order` mediumint(4) unsigned NOT NULL DEFAULT '0',
  `race_name` varchar(64) NOT NULL,
  `race_district` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `race_description` text,
  `num_candidates` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `parties_short_text` varchar(16) NOT NULL DEFAULT '',
  `slug` varchar(48) NOT NULL,
  `is_statewide` int(11) NOT NULL DEFAULT '0',
  `area` varchar(32) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `race_order` (`race_order`),
  KEY `race_name` (`race_name`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `race`
--

LOCK TABLES `race` WRITE;
/*!40000 ALTER TABLE `race` DISABLE KEYS */;
INSERT INTO `race` VALUES (10,'primary',2015,0,'filled',0,'Mayor',0,'',0,'','mayor',0,''),(11,'primary',2015,0,'filled',0,'Council-At-Large',0,'',0,'','council-at-large',0,''),(12,'primary',2015,0,'filled',0,'District 1',1,'',0,'','district-1',0,''),(13,'primary',2015,0,'filled',0,'District 2',2,'',0,'','district-2',0,''),(14,'primary',2015,0,'filled',0,'District 3',3,'',0,'','district-3',0,''),(15,'primary',2015,0,'filled',0,'District 4',4,'',0,'','district-4',0,''),(16,'primary',2015,0,'filled',0,'District 5',5,'',0,'','district-5',0,''),(17,'primary',2015,0,'filled',0,'District 6',6,'',0,'','district-6',0,''),(18,'primary',2015,0,'filled',0,'District 7',7,'',0,'','district-7',0,''),(19,'primary',2015,0,'filled',0,'District 8',8,'',0,'','district-8',0,''),(20,'primary',2015,0,'filled',0,'District 9',9,'',0,'','district-9',0,''),(21,'primary',2015,0,'filled',0,'District 10',10,'',0,'','district-10',0,''),(22,'general',2017,0,'filled',0,'Justice Of The Supreme Court',0,'',0,'','justice-of-the-supreme-court',0,''),(23,'general',2017,0,'filled',0,'Judge Of The Superior Court',0,'',0,'','judge-of-the-superior-court',0,''),(24,'general',2017,0,'filled',0,'Judge Of The Commonwealth Court',0,'',0,'','judge-of-the-commonwealth-court',0,''),(25,'general',2017,0,'filled',0,'Judge Of The Court Of Common Pleas',0,'',0,'','judge-of-the-court-of-common-pleas',0,''),(26,'general',2017,0,'filled',0,'Judge Of The Municipal Court',0,'',0,'','judge-of-the-municipal-court',0,''),(27,'general',2017,0,'open seat',0,'District Attorney',0,'',0,'','district-attorney',0,''),(28,'general',2017,0,'open seat',0,'City Controller',0,'',0,'','city-controller',0,'');
/*!40000 ALTER TABLE `race` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-09-12 19:50:29
