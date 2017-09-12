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
-- Table structure for table `candidate_committees`
--

DROP TABLE IF EXISTS `candidate_committees`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `candidate_committees` (
  `candidate_id` int(11) NOT NULL,
  `committee_id` int(11) NOT NULL,
  PRIMARY KEY (`candidate_id`,`committee_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `candidate_filing`
--

DROP TABLE IF EXISTS `candidate_filing`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `candidate_filing` (
  `id` mediumint(4) unsigned NOT NULL AUTO_INCREMENT,
  `in_general` tinyint(1) unsigned NOT NULL DEFAULT '0',
  `candidate_id` mediumint(4) unsigned NOT NULL,
  `full_name` varchar(255) NOT NULL,
  `office` varchar(128) NOT NULL,
  `office_district` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `county` char(2) NOT NULL,
  `party` varchar(32) NOT NULL,
  `address` varchar(255) NOT NULL,
  `mail_address` varchar(128) NOT NULL,
  `email` varchar(128) NOT NULL,
  `url` varchar(128) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `date_filed` datetime NOT NULL,
  `date_found` datetime NOT NULL,
  `page_found` varchar(16) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cicero_district`
--

DROP TABLE IF EXISTS `cicero_district`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cicero_district` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `cicero_id` int(10) unsigned NOT NULL,
  `sk` int(10) unsigned NOT NULL,
  `district_type` varchar(64) NOT NULL,
  `valid_from` varchar(32) NOT NULL,
  `valid_to` varchar(32) NOT NULL,
  `country` varchar(64) NOT NULL,
  `state` varchar(8) NOT NULL,
  `city` varchar(64) NOT NULL,
  `subtype` varchar(64) NOT NULL,
  `district_id` varchar(64) NOT NULL,
  `num_officials` smallint(5) unsigned NOT NULL DEFAULT '0',
  `label` varchar(64) NOT NULL,
  `ocd_id` varchar(128) NOT NULL DEFAULT '',
  `data` text NOT NULL,
  `last_update_date` varchar(32) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=68 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `committee`
--

DROP TABLE IF EXISTS `committee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `committee` (
  `id` int(4) unsigned NOT NULL AUTO_INCREMENT,
  `candidate_id` int(4) unsigned NOT NULL DEFAULT '0',
  `is_candidates` int(10) unsigned NOT NULL DEFAULT '0',
  `committee_name` varchar(128) NOT NULL,
  `committee_slug` varchar(128) DEFAULT NULL,
  `committee_description` text,
  `donations_2015` decimal(10,2) DEFAULT '0.00',
  `donations_2016` decimal(10,2) DEFAULT '0.00',
  PRIMARY KEY (`id`),
  UNIQUE KEY `committee_name` (`committee_name`),
  KEY `committee_slug` (`committee_slug`)
) ENGINE=MyISAM AUTO_INCREMENT=1127 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `contributor`
--

DROP TABLE IF EXISTS `contributor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `contributor` (
  `id` int(4) unsigned NOT NULL AUTO_INCREMENT,
  `address_id` int(4) NOT NULL DEFAULT '0',
  `name_prefix` varchar(64) NOT NULL DEFAULT '',
  `name_first` varchar(64) NOT NULL DEFAULT '',
  `name_middle` varchar(64) NOT NULL DEFAULT '',
  `name_last` varchar(64) NOT NULL DEFAULT '',
  `name_suffix` varchar(64) NOT NULL DEFAULT '',
  `name_business` varchar(255) NOT NULL DEFAULT '',
  `slug` varchar(64) DEFAULT NULL,
  `is_person` smallint(1) NOT NULL DEFAULT '0',
  `is_business` smallint(1) NOT NULL DEFAULT '0',
  `num_contributions` mediumint(8) unsigned NOT NULL DEFAULT '0',
  `num_committees_contrib_to` mediumint(8) unsigned NOT NULL DEFAULT '0',
  `total_contributed_2015` decimal(12,2) DEFAULT NULL,
  `total_contributed_2016` decimal(12,2) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `slug` (`slug`),
  KEY `name_first` (`name_first`),
  KEY `name_last` (`name_last`),
  KEY `name_prefix` (`name_prefix`),
  KEY `name_suffix` (`name_suffix`),
  KEY `address_id` (`address_id`)
) ENGINE=MyISAM AUTO_INCREMENT=82117 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `contributor_address`
--

DROP TABLE IF EXISTS `contributor_address`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `contributor_address` (
  `id` int(4) unsigned NOT NULL AUTO_INCREMENT,
  `address_type` varchar(64) NOT NULL DEFAULT '',
  `number` varchar(16) NOT NULL DEFAULT '',
  `street` varchar(64) NOT NULL DEFAULT '',
  `addr1` varchar(128) NOT NULL DEFAULT '',
  `addr2` varchar(128) NOT NULL DEFAULT '',
  `po_box` varchar(16) NOT NULL DEFAULT '',
  `city` varchar(64) NOT NULL DEFAULT '',
  `state` varchar(32) NOT NULL DEFAULT '',
  `zipcode` varchar(16) NOT NULL DEFAULT '',
  `slug` varchar(64) DEFAULT NULL,
  `num_individual_contribs` mediumint(8) unsigned NOT NULL DEFAULT '0',
  `num_non_individual_contribs` mediumint(8) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `slug` (`slug`),
  KEY `city` (`city`,`state`),
  KEY `zipcode` (`zipcode`),
  KEY `addr1` (`addr1`),
  KEY `address_type` (`address_type`),
  KEY `number` (`number`),
  KEY `street` (`street`)
) ENGINE=MyISAM AUTO_INCREMENT=52778 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `contributor_type`
--

DROP TABLE IF EXISTS `contributor_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `contributor_type` (
  `id` int(4) unsigned NOT NULL AUTO_INCREMENT,
  `type_name` varchar(64) NOT NULL,
  `type_slug` varchar(32) NOT NULL DEFAULT '',
  `type_description` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `type_name` (`type_name`),
  KEY `type_slug` (`type_slug`)
) ENGINE=MyISAM AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `fb_events`
--

DROP TABLE IF EXISTS `fb_events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fb_events` (
  `id` mediumint(8) unsigned NOT NULL AUTO_INCREMENT,
  `candidate_id` mediumint(8) unsigned NOT NULL,
  `fb_page_id` bigint(10) unsigned NOT NULL,
  `fb_event_id` bigint(10) unsigned NOT NULL,
  `event_type` varchar(16) NOT NULL,
  `event_name` varchar(255) NOT NULL,
  `category` varchar(32) NOT NULL,
  `description` text NOT NULL,
  `attending_count` mediumint(9) NOT NULL,
  `declined_count` mediumint(9) NOT NULL,
  `interested_count` mediumint(9) NOT NULL,
  `maybe_count` mediumint(9) NOT NULL,
  `start_time` datetime NOT NULL,
  `end_time` datetime NOT NULL,
  `is_cancelled` tinyint(1) NOT NULL,
  `place_id` bigint(10) unsigned NOT NULL,
  `place_name` varchar(255) NOT NULL,
  `place_location` text NOT NULL,
  `photos` text NOT NULL,
  `num_photos` mediumint(8) unsigned NOT NULL,
  `picture` text NOT NULL,
  `fb_created_at` datetime NOT NULL,
  `fb_updated_at` datetime NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `candidate_id` (`candidate_id`),
  KEY `type` (`event_type`),
  KEY `fb_post_id` (`fb_event_id`),
  KEY `fb_user_id` (`fb_page_id`),
  KEY `category` (`category`)
) ENGINE=MyISAM AUTO_INCREMENT=362 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `fb_posts`
--

DROP TABLE IF EXISTS `fb_posts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fb_posts` (
  `id` mediumint(8) unsigned NOT NULL AUTO_INCREMENT,
  `candidate_id` mediumint(8) unsigned NOT NULL,
  `fb_page_id` bigint(10) unsigned NOT NULL,
  `fb_post_id` bigint(10) unsigned NOT NULL,
  `post_type` varchar(16) NOT NULL,
  `message` text CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `story` text NOT NULL,
  `link` text NOT NULL,
  `caption` text NOT NULL,
  `description` text NOT NULL,
  `full_picture` text NOT NULL,
  `post_name` text NOT NULL,
  `picture` text NOT NULL,
  `permalink_url` text NOT NULL,
  `reactions` text NOT NULL,
  `num_reactions` mediumint(8) unsigned NOT NULL,
  `num_comments` mediumint(9) NOT NULL,
  `fb_created_at` datetime NOT NULL,
  `fb_updated_at` datetime NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `candidate_id` (`candidate_id`),
  KEY `type` (`post_type`),
  KEY `fb_page_id` (`fb_page_id`),
  KEY `fb_post_id` (`fb_post_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3234 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `open_address_to_donor_address`
--

DROP TABLE IF EXISTS `open_address_to_donor_address`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `open_address_to_donor_address` (
  `open_address_id` mediumint(8) unsigned NOT NULL,
  `donor_address_id` mediumint(8) unsigned NOT NULL,
  PRIMARY KEY (`open_address_id`,`donor_address_id`),
  KEY `donor_address_id` (`donor_address_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `open_addresses`
--

DROP TABLE IF EXISTS `open_addresses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `open_addresses` (
  `id` mediumint(8) unsigned NOT NULL AUTO_INCREMENT,
  `number` varchar(16) NOT NULL,
  `street` varchar(64) NOT NULL,
  `zipcode` smallint(5) unsigned NOT NULL,
  `longitude` decimal(12,8) NOT NULL,
  `latitude` decimal(12,8) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `zipcode5` (`zipcode`),
  KEY `number` (`number`),
  KEY `street` (`street`)
) ENGINE=MyISAM AUTO_INCREMENT=674237 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `party`
--

DROP TABLE IF EXISTS `party`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `party` (
  `id` int(1) unsigned NOT NULL AUTO_INCREMENT,
  `party_name` varchar(32) NOT NULL,
  `slug` varchar(32) NOT NULL,
  `party_order` tinyint(3) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `political_donation`
--

DROP TABLE IF EXISTS `political_donation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `political_donation` (
  `id` int(4) unsigned NOT NULL AUTO_INCREMENT,
  `is_annonymous` tinyint(1) unsigned NOT NULL DEFAULT '0',
  `contributor_id` int(4) unsigned NOT NULL,
  `contributor_type_id` int(4) unsigned NOT NULL,
  `contribution_type_id` int(4) unsigned NOT NULL,
  `committee_id` int(4) unsigned NOT NULL,
  `filing_period_id` int(4) unsigned NOT NULL,
  `employer_name_id` int(4) unsigned NOT NULL,
  `employer_occupation_id` int(4) unsigned NOT NULL,
  `donation_date` datetime NOT NULL,
  `donation_amount` decimal(10,2) NOT NULL,
  `provided_name` varchar(128) NOT NULL,
  `provided_address` varchar(128) NOT NULL,
  `is_fixed_asset` smallint(1) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `contributor_id` (`contributor_id`),
  KEY `contributor_type_id` (`contributor_type_id`),
  KEY `contribution_type_id` (`contribution_type_id`),
  KEY `committee_id` (`committee_id`),
  KEY `filing_period_id` (`filing_period_id`),
  KEY `donation_date` (`donation_date`),
  KEY `donation_amount` (`donation_amount`),
  KEY `employer_name_id` (`employer_name_id`,`employer_occupation_id`)
) ENGINE=MyISAM AUTO_INCREMENT=433215 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `political_donation_contribution_type`
--

DROP TABLE IF EXISTS `political_donation_contribution_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `political_donation_contribution_type` (
  `id` int(4) unsigned NOT NULL AUTO_INCREMENT,
  `is_donation` tinyint(4) NOT NULL DEFAULT '0',
  `type_name` varchar(128) NOT NULL,
  `type_name_short` varchar(32) NOT NULL DEFAULT '',
  `type_slug` varchar(32) NOT NULL DEFAULT '',
  `type_description` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `type_name` (`type_name`),
  KEY `type_slug` (`type_slug`)
) ENGINE=MyISAM AUTO_INCREMENT=29 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `political_donation_contributor_address_cicero_details`
--

DROP TABLE IF EXISTS `political_donation_contributor_address_cicero_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `political_donation_contributor_address_cicero_details` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `address_id` int(10) unsigned NOT NULL,
  `wkid` int(11) NOT NULL,
  `score` int(11) NOT NULL,
  `geo_x` decimal(12,8) NOT NULL,
  `geo_y` decimal(12,8) NOT NULL,
  `match_addr` varchar(192) NOT NULL,
  `match_postal` varchar(32) NOT NULL DEFAULT '',
  `match_country` varchar(32) NOT NULL DEFAULT '',
  `locator` varchar(64) NOT NULL,
  `match_region` varchar(32) NOT NULL DEFAULT '',
  `match_subregion` varchar(32) NOT NULL DEFAULT '',
  `match_city` varchar(64) NOT NULL DEFAULT '',
  `partial_match` tinyint(1) NOT NULL DEFAULT '0',
  `geoservice` varchar(32) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `political_donation_contributor_address_cicero_district_set`
--

DROP TABLE IF EXISTS `political_donation_contributor_address_cicero_district_set`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `political_donation_contributor_address_cicero_district_set` (
  `address_id` mediumint(8) unsigned NOT NULL,
  `cicero_district_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`address_id`,`cicero_district_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `political_donation_contributor_address_cicero_raw`
--

DROP TABLE IF EXISTS `political_donation_contributor_address_cicero_raw`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `political_donation_contributor_address_cicero_raw` (
  `id` mediumint(8) unsigned NOT NULL AUTO_INCREMENT,
  `address_id` int(11) NOT NULL DEFAULT '0',
  `addr1` varchar(128) NOT NULL,
  `zipcode5` smallint(5) unsigned NOT NULL,
  `district_ids` varchar(128) NOT NULL,
  `geo_x` decimal(12,8) NOT NULL,
  `geo_y` decimal(12,8) NOT NULL,
  `match_addr` varchar(192) NOT NULL,
  `raw_text` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=344 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `political_donation_contributor_address_cicero_raw_ward`
--

DROP TABLE IF EXISTS `political_donation_contributor_address_cicero_raw_ward`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `political_donation_contributor_address_cicero_raw_ward` (
  `id` int(11) NOT NULL,
  `contributor_address_id` int(11) NOT NULL DEFAULT '0',
  `geo_x` char(16) NOT NULL,
  `geo_y` char(16) NOT NULL,
  `ward` int(11) NOT NULL,
  UNIQUE KEY `contributor_address_id` (`contributor_address_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `political_donation_employer_name`
--

DROP TABLE IF EXISTS `political_donation_employer_name`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `political_donation_employer_name` (
  `id` int(4) unsigned NOT NULL AUTO_INCREMENT,
  `employer_name` varchar(128) NOT NULL,
  `employer_slug` varchar(32) NOT NULL DEFAULT '',
  `employer_description` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `employer_name` (`employer_name`),
  KEY `employer_slug` (`employer_slug`)
) ENGINE=MyISAM AUTO_INCREMENT=8444 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `political_donation_employer_occupation`
--

DROP TABLE IF EXISTS `political_donation_employer_occupation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `political_donation_employer_occupation` (
  `id` int(4) unsigned NOT NULL AUTO_INCREMENT,
  `occupation_name` varchar(64) NOT NULL,
  `occupation_slug` varchar(32) NOT NULL DEFAULT '',
  `occupation_description` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `occupation_name` (`occupation_name`),
  KEY `occupation_slug` (`occupation_slug`)
) ENGINE=MyISAM AUTO_INCREMENT=5620 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `political_donation_filing_period`
--

DROP TABLE IF EXISTS `political_donation_filing_period`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `political_donation_filing_period` (
  `id` int(4) unsigned NOT NULL AUTO_INCREMENT,
  `period_name` varchar(64) NOT NULL,
  `period_slug` varchar(32) NOT NULL DEFAULT '',
  `period_description` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `period_name` (`period_name`),
  KEY `period_slug` (`period_slug`)
) ENGINE=MyISAM AUTO_INCREMENT=105 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
-- Table structure for table `raw_donations`
--

DROP TABLE IF EXISTS `raw_donations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `raw_donations` (
  `id` mediumint(8) unsigned NOT NULL AUTO_INCREMENT,
  `FilerName` varchar(128) NOT NULL,
  `Year` varchar(32) NOT NULL,
  `Cycle` varchar(32) NOT NULL,
  `DocType` varchar(128) NOT NULL,
  `EntityName` varchar(128) NOT NULL,
  `EntityAddressLine1` varchar(64) NOT NULL,
  `EntityAddressLine2` varchar(64) NOT NULL,
  `EntityCity` varchar(64) NOT NULL,
  `EntityState` varchar(32) NOT NULL,
  `EntityZip` varchar(32) NOT NULL,
  `Occupation` varchar(64) NOT NULL,
  `EmployerName` varchar(128) NOT NULL,
  `EmployerAddressLine1` varchar(64) NOT NULL,
  `EmployerAddressLine2` varchar(64) NOT NULL,
  `EmployerCity` varchar(64) NOT NULL,
  `EmployerState` varchar(32) NOT NULL,
  `EmployerZip` varchar(32) NOT NULL,
  `Date` varchar(32) NOT NULL,
  `Amount` varchar(32) NOT NULL,
  `Description` varchar(255) NOT NULL,
  `Amended` varchar(64) NOT NULL,
  `SubDate` varchar(32) NOT NULL,
  `FiledBy` varchar(128) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Year` (`Year`),
  KEY `Year_2` (`Year`),
  KEY `Cycle` (`Cycle`),
  KEY `DocType` (`DocType`),
  KEY `FilerName` (`FilerName`),
  KEY `EntityCity` (`EntityCity`),
  KEY `EmployerName` (`EmployerName`),
  KEY `Amended` (`Amended`)
) ENGINE=MyISAM AUTO_INCREMENT=113039 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `social_media_accounts`
--

DROP TABLE IF EXISTS `social_media_accounts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `social_media_accounts` (
  `id` int(4) unsigned NOT NULL AUTO_INCREMENT,
  `social_media_site_id` int(2) unsigned NOT NULL,
  `candidate_id` int(4) unsigned NOT NULL,
  `account_url` varchar(128) NOT NULL,
  `account_id` varchar(64) NOT NULL DEFAULT '',
  `account_name` varchar(64) NOT NULL DEFAULT '',
  `last_checked` datetime NOT NULL DEFAULT '1980-01-01 00:00:00',
  `account_order` int(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `last_checked` (`last_checked`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `social_media_sites`
--

DROP TABLE IF EXISTS `social_media_sites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `social_media_sites` (
  `id` int(2) unsigned NOT NULL AUTO_INCREMENT,
  `social_name` varchar(32) NOT NULL,
  `base_url` varchar(64) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sqllite_campaign`
--

DROP TABLE IF EXISTS `sqllite_campaign`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sqllite_campaign` (
  `id` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  `year` smallint(5) unsigned NOT NULL,
  `cycle` varchar(32) NOT NULL,
  `candidate_id` smallint(5) unsigned NOT NULL,
  `position` varchar(64) NOT NULL,
  `party` varchar(64) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=102 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sqllite_candidate`
--

DROP TABLE IF EXISTS `sqllite_candidate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sqllite_candidate` (
  `id` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  `candidate_name` varchar(128) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=97 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sqllite_candidate_to_committee`
--

DROP TABLE IF EXISTS `sqllite_candidate_to_committee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sqllite_candidate_to_committee` (
  `id` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  `sqllite_candidate_id` smallint(5) unsigned NOT NULL,
  `candidate_name` varchar(128) NOT NULL,
  `committee_id` mediumint(8) unsigned NOT NULL,
  `committee_name` varchar(128) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=97 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `us_contributions_by_individuals_active`
--

DROP TABLE IF EXISTS `us_contributions_by_individuals_active`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `us_contributions_by_individuals_active` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `fec_committee_id` char(9) NOT NULL,
  `amendment_indicator` char(1) NOT NULL,
  `report_type` char(3) NOT NULL,
  `primary_general` char(5) NOT NULL,
  `image_number` char(18) NOT NULL,
  `transaction_type` char(3) NOT NULL,
  `entity_type` char(3) NOT NULL,
  `contributor_name` varchar(200) NOT NULL,
  `city` varchar(30) NOT NULL,
  `state` char(2) NOT NULL,
  `zipcode` char(9) NOT NULL,
  `employer` varchar(38) NOT NULL,
  `occupation` varchar(38) NOT NULL,
  `transaction_date` date NOT NULL,
  `amount` decimal(14,2) NOT NULL,
  `from_fec_id` char(9) NOT NULL,
  `transaction_id` varchar(32) NOT NULL,
  `file_num` bigint(20) NOT NULL,
  `memo_code` char(1) NOT NULL,
  `memo_text` char(100) NOT NULL,
  `fec_record_number` bigint(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-09-12 19:49:27
