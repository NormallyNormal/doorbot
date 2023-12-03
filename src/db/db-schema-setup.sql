use doorbot;

CREATE TABLE IF NOT EXISTS usertype (
	id INT UNIQUE NOT NULL AUTO_INCREMENT,
  category VARCHAR(255) NOT NULL,
	startTime time NOT NULL,
  endTime time NOT NULL,
	PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS entryphoto (
	id INT UNIQUE NOT NULL AUTO_INCREMENT,
  fileName VARCHAR(255) UNIQUE NOT NULL,
	`timestamp` datetime NOT NULL,
	PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS doorinfo (
	id INT UNIQUE NOT NULL AUTO_INCREMENT,
  `status` VARCHAR(255) NOT NULL,
	ipAddress VARCHAR(255) UNIQUE NOT NULL,
	dns VARCHAR(255) UNIQUE NOT NULL,
	`port` VARCHAR(255) NOT NULL,
	PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS door (
	id INT UNIQUE NOT NULL AUTO_INCREMENT,
  displayName VARCHAR(255) UNIQUE NOT NULL,
  hashedPassword VARCHAR(255) UNIQUE NOT NULL,
  salt VARCHAR(255) UNIQUE NOT NULL,
	location VARCHAR(255) NOT NULL,
	PRIMARY KEY(id),
	doorInfo_id_door INT UNIQUE NOT NULL,
	KEY fk_doorInfo_id_door (doorInfo_id_door),
    CONSTRAINT fk_doorInfo_id_door FOREIGN KEY (doorInfo_id_door) REFERENCES doorinfo (id) ON DELETE NO ACTION ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS `user` (
	id INT UNIQUE NOT NULL AUTO_INCREMENT,
  discordUUID VARCHAR(255) UNIQUE NOT NULL,
	hashedPassword VARCHAR(255) UNIQUE NOT NULL,
  salt VARCHAR(255) UNIQUE NOT NULL,
  developer boolean NOT NULL,
  loggedIn boolean NOT NULL,
	PRIMARY KEY(id),
	door_id_user INT,
	KEY fk_defaultDoor (door_id_user),
    CONSTRAINT fk_defaultDoor FOREIGN KEY (door_id_user) REFERENCES door (id) ON DELETE NO ACTION ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS opentype (
	id INT UNIQUE NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
	PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS penaltytype (
	id INT UNIQUE NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
	PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS userinstance (
	id INT UNIQUE NOT NULL AUTO_INCREMENT,
  score INT NOT NULL,
	PRIMARY KEY(id),
    
	door_id_userinstance INT NOT NULL,
	KEY fk_doorid_userinstance (door_id_userinstance),
    CONSTRAINT fk_doorid_userinstance FOREIGN KEY (door_id_userinstance) REFERENCES door (id) ON DELETE NO ACTION ON UPDATE CASCADE,
    
	user_id_userinstance INT NOT NULL,
	KEY fk_userid_userinstance (user_id_userinstance),
    CONSTRAINT fk_userid_userinstance FOREIGN KEY (user_id_userinstance) REFERENCES `user` (id) ON DELETE NO ACTION ON UPDATE CASCADE,
    
	userType_id_userinstance INT NOT NULL,
	KEY fk_userTypeid_userinstance (userType_id_userinstance),
    CONSTRAINT fk_userTypeid_userinstance FOREIGN KEY (userType_id_userinstance) REFERENCES usertype (id) ON DELETE NO ACTION ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS openlog (
	id INT UNIQUE NOT NULL AUTO_INCREMENT,
  `timestamp` datetime NOT NULL,
	PRIMARY KEY(id),
    
	door_id_openlog INT NOT NULL,
	KEY fk_doorid_openlog (door_id_openlog),
    CONSTRAINT fk_doorid_openlog FOREIGN KEY (door_id_openlog) REFERENCES door (id) ON DELETE NO ACTION ON UPDATE CASCADE,
    
    photo_id_openlog INT UNIQUE NOT NULL,
	KEY fk_photoid_openlog (photo_id_openlog),
    CONSTRAINT fk_photoid_openlog FOREIGN KEY (photo_id_openlog) REFERENCES entryphoto (id) ON DELETE CASCADE ON UPDATE CASCADE,
    
	userInstance_id_openlog INT NOT NULL,
	KEY fk_userInstanceid_openlog (userInstance_id_openlog),
    CONSTRAINT fk_userInstanceid_openlog FOREIGN KEY (userInstance_id_openlog) REFERENCES userinstance (id) ON DELETE NO ACTION ON UPDATE CASCADE,
    
	openType_id_openlog INT NOT NULL,
	KEY fk_openTypeid_openlog (openType_id_openlog),
    CONSTRAINT fk_openTypeid_openlog FOREIGN KEY (openType_id_openlog) REFERENCES opentype (id) ON DELETE NO ACTION ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS penaltylog (
	id INT UNIQUE NOT NULL AUTO_INCREMENT,
  `timestamp` datetime NOT NULL,
  penalty INT NOT NULL,
	PRIMARY KEY(id),
    
	door_id_penaltylog INT NOT NULL,
	KEY fk_doorid_penaltylog (door_id_penaltylog),
    CONSTRAINT fk_doorid_penaltylog FOREIGN KEY (door_id_penaltylog) REFERENCES door (id) ON DELETE NO ACTION ON UPDATE CASCADE,
    
	userInstance_id_penaltylog INT NOT NULL,
	KEY fk_userInstanceid_penaltylog (userInstance_id_penaltylog),
    CONSTRAINT fk_userInstanceid_penaltylog FOREIGN KEY (userInstance_id_penaltylog) REFERENCES userinstance (id) ON DELETE NO ACTION ON UPDATE CASCADE,
    
	penaltyType_id_penaltylog INT NOT NULL,
	KEY fk_penaltyTypeid_penaltylog (penaltyType_id_penaltylog),
    CONSTRAINT fk_penaltyTypeid_penaltylog FOREIGN KEY (penaltyType_id_penaltylog) REFERENCES penaltytype (id) ON DELETE NO ACTION ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS scheduledEvent (
	id INT UNIQUE NOT NULL AUTO_INCREMENT,
	timeStart datetime NOT NULL,
  timeEnd datetime NOT NULL,
	`name` VARCHAR(255) UNIQUE NOT NULL,
	PRIMARY KEY(id),
    
  door_id_scheduledEvent INT NOT NULL,
	KEY fk_doorid_scheduledEvent (door_id_scheduledEvent),
    CONSTRAINT fk_doorid_scheduledEvent FOREIGN KEY (door_id_scheduledEvent) REFERENCES door (id) ON DELETE NO ACTION ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS userToEvent (
	userInstance_id_userToEvent INT NOT NULL,
	KEY fk_userInstanceid_userToEvent (userInstance_id_userToEvent),
    CONSTRAINT fk_userInstanceid_userToEvent FOREIGN KEY (userInstance_id_userToEvent) REFERENCES userinstance (id) ON DELETE NO ACTION ON UPDATE CASCADE,
	
  event_id_userToEvent INT NOT NULL,
	KEY fk_eventid_userToEvent (event_id_userToEvent),
    CONSTRAINT fk_eventid_userToEvent FOREIGN KEY (event_id_userToEvent) REFERENCES scheduledEvent (id) ON DELETE NO ACTION ON UPDATE CASCADE,
    
	PRIMARY KEY(userInstance_id_userToEvent, event_id_userToEvent)
);

-- DROP TRIGGER IF EXISTS add_penalty;
CREATE TRIGGER add_penalty
AFTER INSERT ON penaltylog
FOR EACH ROW
	UPDATE userinstance
	SET score = score - NEW.penalty
	WHERE id = NEW.userInstance_id_penaltylog;

-- DROP PROCEDURE IF EXISTS create_open_log;
-- DROP PROCEDURE IF EXISTS open_door;

DELIMITER //
CREATE PROCEDURE create_open_log(IN user_id VARCHAR(255), IN door_id INT, IN photo_filename VARCHAR(255), IN open_type_id INT, OUT success boolean)
BEGIN 
	DECLARE ui_id INT;
	DECLARE t time; -- timestamp
	DECLARE last_inserted INT;
	SELECT ui.id INTO ui_id FROM userinstance AS ui JOIN user AS u ON u.id = ui.user_id_userinstance JOIN door AS d ON d.id = ui.door_id_userinstance WHERE d.id = door_id AND u.id = user_id;
	IF ui_id IS NOT NULL THEN 
		SET t = CURRENT_TIME();
		INSERT INTO entryphoto(fileName, `timestamp`) VALUES (photo_filename, t);
		SET last_inserted = LAST_INSERT_ID();
		IF last_inserted <> 0 THEN
			INSERT INTO openlog(`timestamp`, door_id_openlog, photo_id_openlog, userInstance_id_openlog, openType_id_openlog) VALUES (t, door_id, last_inserted, ui_id, open_type_id);
            SET success = 1;
        ELSE 
			SET success = 0;
		END IF;
	ELSE
		SET success = 0;
	END IF;
END;
//

CREATE PROCEDURE open_door(IN door_id INT, IN user_id VARCHAR(255), OUT score INT, OUT msg VARCHAR(255))
BEGIN
	DECLARE ui_id INT;
	DECLARE start_time datetime;
	DECLARE end_time datetime; 
	-- Get the user instance ID for this door
	SELECT ui.id INTO ui_id FROM userinstance AS ui JOIN user AS u ON u.id = ui.user_id_userinstance JOIN door AS d ON d.id = ui.door_id_userinstance WHERE d.id = door_id AND u.id = user_id;
	IF ui_id IS NOT NULL THEN
		-- Get times the user can enter the door
		SELECT ut.startTime, ut.endTime INTO start_time, end_time FROM usertype AS ut JOIN userinstance AS ui ON ui.userType_id_userinstance = ut.id WHERE ui.id = ui_id;
		IF start_time < CURRENT_TIME() AND end_time > CURRENT_TIME() THEN
			SELECT ui.score INTO score FROM userinstance AS ui WHERE ui.id = ui_id;
		ELSE
			SET msg = "No permission to access that door right now";
		END IF;
	ELSE 
		SET msg = "No permission for that door";
	END IF;
END;
//
DELIMITER ;
