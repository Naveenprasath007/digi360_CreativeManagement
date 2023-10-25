----convert all to varchar----

CREATE TABLE CampaignQuestionResponse (
    CampaignQuestionID   varchar(255),
    UserID varchar(255),
    Response varchar(2000)  NOT NULL
);

-- Table: CampaignVideo
CREATE TABLE CampaignVideo (
    CampaignVideoID varchar(255),
    VideoID varchar(255),
    CampaignID varchar(255),
    PreviousVideoID varchar(255),
    CONSTRAINT CampaignVideo_pk PRIMARY KEY  (CampaignVideoID)
);


-- Table: tb_CampaignQuestion
CREATE TABLE tb_CampaignQuestion (
    CampaignQuestionID varchar(255),
    CampaignVideoID varchar(255),
    UserRoleID varchar(255),
    QuestionID varchar(255),
    CONSTRAINT tb_CampaignQuestion_pk PRIMARY KEY  (CampaignQuestionID)
);

-- Table: tb_Question
CREATE TABLE tb_Question (
    QuestionID varchar(255),
    QuestionText varchar(2000)  NOT NULL,
    QuestionResponse varchar(4000)  NOT NULL,
    CONSTRAINT tb_Question_pk PRIMARY KEY  (QuestionID)
);

-- Table: tb_User
CREATE TABLE tb_User (
    UserID varchar(255),
    UserName varchar(250)  NOT NULL,
    UserRoleID varchar(255),
    CONSTRAINT tb_User_pk PRIMARY KEY  (UserID)
);

-- Table: tb_UserRole
CREATE TABLE tb_UserRole (
    UserRoleID varchar(255),
    UserRoleName varchar(250)  NOT NULL,
    CONSTRAINT tb_UserRole_pk PRIMARY KEY  (UserRoleID)
);

-- Table: tb_Video
CREATE TABLE tb_Video (
    VideoID varchar(255),
    PreviousVideoID varchar(255),
    VideoName varchar(2000)  NOT NULL,
    VideoPath varchar(2000)  NOT NULL,
    VideoTranscription varchar(30000)  NOT NULL,
    CONSTRAINT tb_Video_pk PRIMARY KEY  (VideoID)
);



CREATE TABLE tb_Status (
    UserID varchar(255),
    VideoID varchar(250)  NOT NULL,
    Reason varchar(255),
	videoName varchar(255),
	Approver varchar(255)
);


CREATE TABLE tb_Approve (
    UserID varchar(255),
    VideoID varchar(250)  NOT NULL,
    VideoTitle varchar(255),
	VideoPath varchar(255)
);




----my editz-----

-- foreign keys
-- Reference: CampaignQuestionResponse_tb_CampaignQuestion (table: CampaignQuestionResponse)
ALTER TABLE CampaignQuestionResponse ADD CONSTRAINT CampaignQuestionResponse_tb_CampaignQuestion
    FOREIGN KEY (CampaignQuestionID)
    REFERENCES tb_CampaignQuestion (CampaignQuestionID);

-- Reference: CampaignQuestionResponse_tb_User (table: CampaignQuestionResponse)
ALTER TABLE CampaignQuestionResponse ADD CONSTRAINT CampaignQuestionResponse_tb_User
    FOREIGN KEY (UserID)
    REFERENCES tb_User (UserID);


-- Reference: CampaignVideo_tb_Video (table: CampaignVideo)
ALTER TABLE CampaignVideo ADD CONSTRAINT CampaignVideo_tb_Video
    FOREIGN KEY (VideoID)
    REFERENCES tb_Video (VideoID);

-- Reference: tb_CampaignQuestion_CampaignVideo (table: tb_CampaignQuestion)
ALTER TABLE tb_CampaignQuestion ADD CONSTRAINT tb_CampaignQuestion_CampaignVideo
    FOREIGN KEY (CampaignVideoID)
    REFERENCES CampaignVideo (CampaignVideoID);

-- Reference: tb_CampaignQuestion_tb_Question (table: tb_CampaignQuestion)
ALTER TABLE tb_CampaignQuestion ADD CONSTRAINT tb_CampaignQuestion_tb_Question
    FOREIGN KEY (QuestionID)
    REFERENCES tb_Question (QuestionID);

-- Reference: tb_CampaignQuestion_tb_UserRole (table: tb_CampaignQuestion)
ALTER TABLE tb_CampaignQuestion ADD CONSTRAINT tb_CampaignQuestion_tb_UserRole
    FOREIGN KEY (UserRoleID)
    REFERENCES tb_UserRole (UserRoleID);



-- Reference: tb_User_tb_UserRole (table: tb_User)
ALTER TABLE tb_User ADD CONSTRAINT tb_User_tb_UserRole
    FOREIGN KEY (UserRoleID)
    REFERENCES tb_UserRole (UserRoleID);

-- End of file.



ALTER TABLE tb_Status ADD CONSTRAINT tb_Status_tb_User
    FOREIGN KEY (UserID)
    REFERENCES tb_User (UserID);



ALTER TABLE tb_Approve ADD CONSTRAINT tb_Approve_tb_User
    FOREIGN KEY (UserID)
    REFERENCES tb_User (UserID);

ALTER TABLE tb_User
ADD Password varchar(256) not null;


ALTER TABLE tb_Approve
ADD ApprovedDate timestamp;

alter table tb_Approve
add UploaderName varchar(255);


ALTER TABLE tb_Status
ADD CreatedDate timestamp;

alter table tb_Status
add Status varchar(255);

alter table tb_Status
add UploaderName varchar(255);

alter table tb_Status
add Platform varchar(255);


alter table tb_Video
add Vendor varchar(255);

alter table tb_Video
add LOB varchar(255);

alter table tb_Video
add Creative varchar(255);

alter table tb_Video
add Platform varchar(255); 

alter table tb_Video
add VideoPath1 varchar(255); 

alter table tb_Video
add VideoTranscribeOne varchar(30000)  NOT NULL;

--here below new querys---


CREATE TABLE videodetails (
    UserID varchar(255),
    videopath varchar(2000)  NOT NULL
);

alter table tb_User
add Vendor varchar(255);

alter table tb_Video
add Creater varchar(255);


---- NEW---
alter table tb_Video
add imgurl varchar(255);

alter table tb_Video
add gifurl varchar(255);


alter table tb_Status
add imgurl varchar(255);

alter table tb_Status
add gifurl varchar(255);

alter table tb_Status
add videopath1 varchar(255);

alter table tb_Status
add videopath varchar(255);

alter table tb_Status
add Creative varchar(255);

alter table tb_Status
add mainReason varchar(255);



CREATE TABLE tb_ApproverQuestion (
    QuestionID varchar(255),
    QuestionText varchar(2000)  NOT NULL,
    CONSTRAINT tb_ApproverQuestion_pk PRIMARY KEY  (QuestionID)
);


alter table campaignquestionresponse
add auto_increment_id SERIAL;


alter table tb_approve
add downloadaccess varchar(255);

alter table tb_approve
add downloader varchar(255);



alter table tb_Status
add downloadaccess varchar(255);

alter table tb_Status
add downloader varchar(255);




alter table tb_Video
add imgurl1 varchar(255); 

alter table tb_Video
add gifurl1 varchar(255); 

alter table videodetails
add videoname varchar(255); 

alter table videodetails
add creative varchar(255); 


alter table tb_Status
add downloadaccesslist varchar(255);

ALTER TABLE tb_video
RENAME COLUMN imgurl1 TO videopath2;

ALTER TABLE tb_video 
DROP COLUMN gifurl1;

ALTER TABLE tb_video 
DROP COLUMN videotranscribeone;


alter table tb_Status
add videopath2 varchar(255);

alter table tb_Status
add aspect_ratio varchar(255);

ALTER TABLE tb_video 
add aspect_ratio varchar(255);
