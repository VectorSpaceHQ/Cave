-- MySQL dump 10.13  Distrib 5.5.40, for debian-linux-gnu (i686)
--
-- Host: localhost    Database: RaspberryParade
-- ------------------------------------------------------
-- Server version	5.5.40-0ubuntu0.14.04.1

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
-- Table structure for table `ModuleInfo`
--

DROP TABLE IF EXISTS `ModuleInfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ModuleInfo` (
  `moduleID` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `strDescription` varchar(45) DEFAULT NULL,
  `firmwareVer` char(11) DEFAULT NULL,
  `tempSense` tinyint(1) NOT NULL DEFAULT '0',
  `humiditySense` tinyint(1) NOT NULL DEFAULT '0',
  `lightSense` tinyint(1) NOT NULL DEFAULT '0',
  `motionSense` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`moduleID`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `SensorData`
--

DROP TABLE IF EXISTS `SensorData`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `SensorData` (
  `readingID` int(11) NOT NULL AUTO_INCREMENT,
  `timeStamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `moduleID` int(11) unsigned NOT NULL,
  `location` varchar(25) NOT NULL,
  `temperature` decimal(4,1) NOT NULL,
  `humidity` decimal(3,2) DEFAULT NULL,
  `light` decimal(3,2) DEFAULT NULL,
  `motion` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`readingID`),
  KEY `moduleID` (`moduleID`),
  CONSTRAINT `SensorData_ibfk_1` FOREIGN KEY (`moduleID`) REFERENCES `ModuleInfo` (`moduleID`)
) ENGINE=InnoDB AUTO_INCREMENT=174025 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `ThermostatLog`
--

DROP TABLE IF EXISTS `ThermostatLog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ThermostatLog` (
  `timeStamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `moduleID` int(11) unsigned NOT NULL,
  `targetTemp` int(11) DEFAULT NULL,
  `actualTemp` float DEFAULT NULL,
  `coolOn` tinyint(1) NOT NULL,
  `heatOn` tinyint(1) NOT NULL,
  `fanOn` tinyint(1) NOT NULL,
  `auxOn` tinyint(1) NOT NULL,
  PRIMARY KEY (`timeStamp`),
  KEY `moduleID` (`moduleID`),
  CONSTRAINT `ThermostatLog_ibfk_1` FOREIGN KEY (`moduleID`) REFERENCES `ModuleInfo` (`moduleID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ThermostatSet`
--

DROP TABLE IF EXISTS `ThermostatSet`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ThermostatSet` (
  `timeStamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `moduleID` int(11) unsigned NOT NULL,
  `targetTemp` int(11) NOT NULL,
  `targetMode` varchar(45) NOT NULL,
  `expiryTime` datetime NOT NULL,
  `entryNo` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`entryNo`),
  KEY `moduleID` (`moduleID`),
  CONSTRAINT `ThermostatSet_ibfk_1` FOREIGN KEY (`moduleID`) REFERENCES `ModuleInfo` (`moduleID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

INSERT INTO `hvac`.`ModuleInfo` (`moduleID`, `strDescription`, `firmwareVer`, `tempSense`, `humiditySense`, `lightSense`, `motionSense`) VALUES ('1', 'RPI thermostat 1', '1', '1', '0', '1', '1');

-- Dump completed on 2015-01-05 22:14:07
