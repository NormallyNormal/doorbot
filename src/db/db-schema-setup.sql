USE doorbot;

CREATE TABLE usertype (
	id INT UNIQUE NOT NULL AUTO_INCREMENT,
    category VARCHAR(255) NOT NULL,
	startTime datetime NOT NULL,
    endTime datetime NOT NULL,
	PRIMARY KEY(id)
);

CREATE TABLE entryphoto (
	id INT UNIQUE NOT NULL AUTO_INCREMENT,
    fileName VARCHAR(255) NOT NULL,
	`timestamp` datetime NOT NULL,
	PRIMARY KEY(id)
);

CREATE TABLE doorinfo (
	id INT UNIQUE NOT NULL AUTO_INCREMENT,
    `status` VARCHAR(255) NOT NULL,
	ipAddress VARCHAR(255) NOT NULL,
	dns VARCHAR(255) NOT NULL,
	`port` VARCHAR(255) NOT NULL,
	PRIMARY KEY(id)
);

CREATE TABLE door (
	id INT UNIQUE NOT NULL AUTO_INCREMENT,
    displayName VARCHAR(255) NOT NULL,
	location VARCHAR(255) NOT NULL,
	PRIMARY KEY(id),
	doorInfo_id_door INT UNIQUE NOT NULL,
	KEY fk_doorInfo_id_door (doorInfo_id_door),
    CONSTRAINT fk_doorInfo_id_door FOREIGN KEY (doorInfo_id_door) REFERENCES doorinfo (id) ON DELETE NO ACTION ON UPDATE CASCADE
);

CREATE TABLE `user` (
	id INT UNIQUE NOT NULL AUTO_INCREMENT,
    discordUUID VARCHAR(255) NOT NULL,
	hashedPassword VARCHAR(255) NOT NULL,
    salt VARCHAR(255) NOT NULL,
    developer BIT NOT NULL,
	PRIMARY KEY(id),
	door_id_user INT UNIQUE,
	KEY fk_defaultDoor (door_id_user),
    CONSTRAINT fk_defaultDoor FOREIGN KEY (door_id_user) REFERENCES door (id) ON DELETE NO ACTION ON UPDATE CASCADE
);

CREATE TABLE opentype (
	id INT UNIQUE NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL,
	PRIMARY KEY(id)
);

CREATE TABLE penaltytype (
	id INT UNIQUE NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL,
	PRIMARY KEY(id)
);

CREATE TABLE userinstance (
	id INT UNIQUE NOT NULL AUTO_INCREMENT,
    score INT NOT NULL,
	PRIMARY KEY(id),
    
	door_id_userinstance INT UNIQUE NOT NULL,
	KEY fk_doorid_userinstance (door_id_userinstance),
    CONSTRAINT fk_doorid_userinstance FOREIGN KEY (door_id_userinstance) REFERENCES door (id) ON DELETE NO ACTION ON UPDATE CASCADE,
    
	user_id_userinstance INT UNIQUE NOT NULL,
	KEY fk_userid_userinstance (user_id_userinstance),
    CONSTRAINT fk_userid_userinstance FOREIGN KEY (user_id_userinstance) REFERENCES `user` (id) ON DELETE NO ACTION ON UPDATE CASCADE,
    
	userType_id_userinstance INT UNIQUE NOT NULL,
	KEY fk_userTypeid_userinstance (userType_id_userinstance),
    CONSTRAINT fk_userTypeid_userinstance FOREIGN KEY (userType_id_userinstance) REFERENCES usertype (id) ON DELETE NO ACTION ON UPDATE CASCADE
);

CREATE TABLE openlog (
	id INT UNIQUE NOT NULL AUTO_INCREMENT,
    `timestamp` datetime NOT NULL,
	PRIMARY KEY(id),
    
	door_id_openlog INT UNIQUE NOT NULL,
	KEY fk_doorid_openlog (door_id_openlog),
    CONSTRAINT fk_doorid_openlog FOREIGN KEY (door_id_openlog) REFERENCES door (id) ON DELETE NO ACTION ON UPDATE CASCADE,
    
    photo_id_openlog INT UNIQUE NOT NULL,
	KEY fk_photoid_openlog (photo_id_openlog),
    CONSTRAINT fk_photoid_openlog FOREIGN KEY (photo_id_openlog) REFERENCES entryphoto (id) ON DELETE CASCADE ON UPDATE CASCADE,
    
	userInstance_id_openlog INT UNIQUE NOT NULL,
	KEY fk_userInstanceid_openlog (userInstance_id_openlog),
    CONSTRAINT fk_userInstanceid_openlog FOREIGN KEY (userInstance_id_openlog) REFERENCES userinstance (id) ON DELETE NO ACTION ON UPDATE CASCADE,
    
	openType_id_openlog INT UNIQUE NOT NULL,
	KEY fk_openTypeid_openlog (openType_id_openlog),
    CONSTRAINT fk_openTypeid_openlog FOREIGN KEY (openType_id_openlog) REFERENCES opentype (id) ON DELETE NO ACTION ON UPDATE CASCADE
);

CREATE TABLE penaltylog (
	id INT UNIQUE NOT NULL AUTO_INCREMENT,
    `timestamp` datetime NOT NULL,
    penalty INT NOT NULL,
	PRIMARY KEY(id),
    
	door_id_penaltylog INT UNIQUE NOT NULL,
	KEY fk_doorid_penaltylog (door_id_penaltylog),
    CONSTRAINT fk_doorid_penaltylog FOREIGN KEY (door_id_penaltylog) REFERENCES door (id) ON DELETE NO ACTION ON UPDATE CASCADE,
    
	userInstance_id_penaltylog INT UNIQUE NOT NULL,
	KEY fk_userInstanceid_penaltylog (userInstance_id_penaltylog),
    CONSTRAINT fk_userInstanceid_penaltylog FOREIGN KEY (userInstance_id_penaltylog) REFERENCES userinstance (id) ON DELETE NO ACTION ON UPDATE CASCADE,
    
	penaltyType_id_penaltylog INT UNIQUE NOT NULL,
	KEY fk_penaltyTypeid_penaltylog (penaltyType_id_penaltylog),
    CONSTRAINT fk_penaltyTypeid_penaltylog FOREIGN KEY (penaltyType_id_penaltylog) REFERENCES penaltytype (id) ON DELETE NO ACTION ON UPDATE CASCADE
);

CREATE TABLE scheduledEvent (
	id INT UNIQUE NOT NULL AUTO_INCREMENT,
	timeStart datetime NOT NULL,
    timeEnd datetime NOT NULL,
	`name` VARCHAR(255) NOT NULL,
	PRIMARY KEY(id),
    
    door_id_scheduledEvent INT UNIQUE NOT NULL,
	KEY fk_doorid_scheduledEvent (door_id_scheduledEvent),
    CONSTRAINT fk_doorid_scheduledEvent FOREIGN KEY (door_id_scheduledEvent) REFERENCES door (id) ON DELETE NO ACTION ON UPDATE CASCADE
);

CREATE TABLE userToEvent (
	userInstance_id_userToEvent INT UNIQUE NOT NULL,
	KEY fk_userInstanceid_userToEvent (userInstance_id_userToEvent),
    CONSTRAINT fk_userInstanceid_userToEvent FOREIGN KEY (userInstance_id_userToEvent) REFERENCES userinstance (id) ON DELETE NO ACTION ON UPDATE CASCADE,
	
    event_id_userToEvent INT UNIQUE NOT NULL,
	KEY fk_eventid_userToEvent (event_id_userToEvent),
    CONSTRAINT fk_eventid_userToEvent FOREIGN KEY (event_id_userToEvent) REFERENCES scheduledEvent (id) ON DELETE NO ACTION ON UPDATE CASCADE,
    
	PRIMARY KEY(userInstance_id_userToEvent, event_id_userToEvent)
);