insert into users values (97, '123', 'Connor McDavid','cm@nhl.com','Edmonton',-7);
insert into users values (29, '456', 'Leon Draisaitl','ld@nhl.com','Edmonton',-7);
insert into users values (5, '789', 'Davood Rafiei','dr@ualberta.ca','Edmonton',-7);
insert into users values (3, 'abc', 'John Doeee','jd@ualberta.ca','Edmonton',-7);
insert into users values (6, 'def', 'john doe',null,'Edmonton',-7);
insert into users values (7, 'ghi', 'John doee','jd@ualberta.ca','Edmonton',-7);
insert into users values (8, 'jkl', 'Jery Joe','jer@ualberta.ca','Edmonton',-7);
insert into users values (9, 'mno', 'Alex','a@ualberta.ca','John',-7);
insert into users values (10, 'pqr', 'Eubank','eu@ualberta.ca','Johnny',-7);
insert into users values (11, 'stu', 'Andrew','and@ualberta.ca','Johni',-7);
insert into users values (12, 'def', 'john',null,'Edmonton',-7);
insert into users values (13, 'ghi', 'John d','jd@ualberta.ca','Edmonton',-7);
insert into users values (14, 'jkl', 'Johnnie','jer@ualberta.ca','Edmonton',-7);
insert into users values (15, 'mno', 'Alex1','a@ualberta.ca','John',-7);
insert into users values (16, 'pqr', 'Eubank1','eu@ualberta.ca','Johnny',-7);
insert into users values (17, 'stu', 'Andrew1','and@ualberta.ca','Johni',-7);

insert into follows values (29,97,'2021-01-10');
insert into follows values (97,29,'2021-09-01');
insert into follows values (5,97,'2022-11-15');
insert into follows values (3,97,'2023-09-14');
insert into follows values (6,97,'2023-09-16');
insert into follows values (7,97,'2023-09-17');
insert into follows values (3,6,'2023-09-16');
insert into follows values (5,6,'2023-09-16');
insert into follows values (7,6,'2023-09-16');
insert into follows values (8,6,'2023-09-16');

insert into tweets values (1, 5,'2023-06-01','Looking for a good book to read. Just finished lone #survivor', null);
insert into tweets values (2, 97,'2023-02-12','#Edmonton #Oilers had a good game last night.',null);
insert into tweets values (3, 5,'2023-03-01','Go oliers!',4);
insert into tweets values (4, 3,'2023-01-12','#Edmonton #Oilers had a good game last night.',null);
insert into tweets values (5, 3,'2023-02-12','#Edmonton #Oilers',null);
insert into tweets values (6, 3,'2023-03-12','#Edmonton is a great city!',null);
insert into tweets values (7, 7,'2023-04-12','#Edmonton is a great city!',null);
insert into tweets values (8, 7,'2022-04-12','#Edmonton is a great city!',null);
insert into tweets values (9, 29,'2022-05-12','ooga',null);
insert into tweets values (10, 29,'2022-12-28','booga',null);
insert into tweets values (11, 29,'2023-03-15','chub',null);
insert into tweets values (12, 29,'2022-08-19','flowers',null);
insert into tweets values (13, 29,'2022-10-21','town hall',null);
insert into tweets values (14, 29,'2022-04-24','hello world',null);
insert into tweets values (15, 29,'2022-06-10','super',null);
insert into tweets values (16, 29,'2022-16-28','zoms',null);
insert into tweets values (17, 29,'2023-02-15','cgsdfg',null);
insert into tweets values (18, 29,'2022-04-19','plane',null);
insert into tweets values (19, 29,'2022-02-21','h2o',null);
insert into tweets values (20, 29,'2022-05-24','asdw',null);
insert into tweets values (21, 29,'2022-07-11','gem',null);
insert into tweets values (22, 3,'2023-05-12','edmonton          oilers',null);


insert into hashtags values ('survivor');
insert into hashtags values ('oilers');
insert into hashtags values ('edmonton');

insert into mentions values (1, 'survivor');
insert into mentions values (2, 'edmonton');
insert into mentions values (3, 'oilers');

insert into retweets values (29,1,'2023-02-13');
insert into retweets values (3,2,'2023-03-13');
insert into retweets values (5,1,'2023-04-13');
insert into retweets values (5,3,'2023-05-13');
insert into retweets values (29,3,'2023-07-13');
insert into retweets values (7,4,'2023-02-11');
insert into retweets values (3,5,'2023-01-13');
insert into retweets values (3,7,'2023-03-15');

insert into lists values ('oilers players',5);
insert into lists values ('pc',5);
insert into lists values ('liberal',5);
insert into lists values ('ndp',5);

insert into includes values ('oilers players',97);
insert into includes values ('oilers players',29);
insert into includes values ('oilers players',3);
insert into includes values ('oilers players',5);
insert into includes values ('oilers players',7);
insert into includes values ('oilers players',6);
insert into includes values ('oilers players',8);
