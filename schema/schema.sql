CREATE TABLE `policy_published` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `domain` text,
  `aspf` tinytext,
  `adkim` tinytext,
  `p` text,
  `pct` int(3) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11243 DEFAULT CHARSET=latin1;

CREATE TABLE `report_metadata` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `organization` text,
  `email` text,
  `extra_contact_information` text,
  `report_id` text,
  `date_range_begin` int(11) DEFAULT NULL,
  `date_range_end` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11263 DEFAULT CHARSET=latin1;

CREATE TABLE `records` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `source_ip` char(15) DEFAULT NULL,
  `count` int(11) DEFAULT NULL,
  `disposition` char(11) DEFAULT NULL,
  `dkim` char(11) DEFAULT NULL,
  `spf` char(11) DEFAULT NULL,
  `type` char(20) DEFAULT NULL,
  `comment` text,
  `header_from` char(255) DEFAULT NULL,
  `dkim_domain` char(255) DEFAULT NULL,
  `dkim_result` char(11) DEFAULT NULL,
  `dkim_hresult` char(255) DEFAULT NULL,
  `spf_domain` char(255) DEFAULT NULL,
  `spf_result` char(11) DEFAULT NULL,
  `metadata_fk` int(11) unsigned NOT NULL,
  `published_fk` int(11) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `report_metadata_fk` (`metadata_fk`),
  KEY `policy_published_fk` (`published_fk`),
  CONSTRAINT `policy_published_fk` FOREIGN KEY (`published_fk`) REFERENCES `policy_published` (`id`),
  CONSTRAINT `report_metadata_fk` FOREIGN KEY (`metadata_fk`) REFERENCES `report_metadata` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6575763 DEFAULT CHARSET=latin1;