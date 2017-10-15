# Plan and Process
> Author: 李大祥
StartTime : 2017-02-25
ModifyTime :  2017-07-20

## 1. Preparation Phrase Plan
+ [x] ~~1. Test how to use git server software.~~
+ [x] ~~2. Make sure that whether it can to use python to control linux commands.~~
+ [x] ~~3. Search for maximum user number by logging via SSH.~~
+ [x] ~~4. Learn python and django framework.~~
+ [x] ~~5. Design the system.~~
+ [x] ~~6. Write the ideas and design textbook, named 'ideas-and-design.md'.~~
+ [x] ~~7. Create a github repository.(It is named 'WeArt.md' meaning that our arts and we create arts together.)~~
+ [x] ~~8. Write the plan and process textbook.~~
+ [x] ~~9. Organize the all commands and test excuted by python.(2017-0701)~~
+ [x] ~~10. Write a demo that it can show control novel's version.(2017-0706)~~
+ [x] ~~11. Deploy server using two computer in teacher's lab.(2017-0714)~~

## 2. Development Phrase Plan
+ [x] ~~1. Design and Build Database.(2017-07-20)~~
+ [x] ~~2. Design Use case diagram and Class diagram.(2017-07-22)~~
+ [x] ~~3. Reader can login and register.(2017-07-26)~~
+ [x] ~~4. Author can be enabled.(2017-07-30)~~
+ [x] ~~5. Add html pages, create books function of author apps.(2017-08-12)~~
+ [x] ~~6. Author can create a novel and chapters.(2017-09-16)~~
+ [x] ~~7. Author can update the novel content.(2017-09-17)~~
+ [x] ~~8. Reader can read book,chapters list and content.(2017-09-21)~~
+ [x] ~~9. Differnt Readers can write different version chapters according by the same story outline.(2017-09-28)~~
+ [x] ~~10. Reader can read different version content.(2017-10-09)~~
+ [x] ~~11. Reader modify userName and password.(2017-10-10)~~
+ [x] ~~12. Reader can collect their favorite books and delete collections.(2017-10-11)~~
+ [x] ~~13. Author and Administrator manages books.(2017-10-11)~~
+ [x] ~~14. Delete foreign keys of database.(2017-10-11)~~                
+ [x] ~~15. Readers vote for a chapter of one version.(2017-10-14)~~                
+ [x] ~~16. Register a administrator account, login and modify password.(2017-10-15)~~          
+ [x] ~~17. Administrator manages books, readers and authors.(2017-10-15)~~   
+ [ ] 18. Recommand app, add,modify and get.(2017-10-28)

+ [ ] 19. Fix bugs knowed.(2017-10-28)
+ Modify the database struct (column name,data type) and use django commands to update database changes not using sql commands.(2017-10-28)
+ Change using extra bash file to using inner command string, when making the book's classied directory.(2017-10-28)
+ The error that joining in writing other reader's chapter when not logined.(2017-10-28)
+ Reader index page for showing data.(2017-10-28)

+ [ ] 20. Replace some pages with new html files.(2017-10-28)

## 3. Optional Development Phrase Plan
+ [ ] 21. [Optional] Use task queue(Celery in django) to serialize the operations operating the same file from different users, and these operations requests occuring at the same time.(2017-12-28)
+ [ ] 23. [Optional] Redis cache function.(2017-12-28)
+ [ ] 24. [Optional] Files writing error.(2017-12-28)
+ [ ] 25. [Optional] Database roolback.(2017-12-28)

## 4. Test Phrase Plan And Editing Files
+ [ ] 1. Unit test & Fix bugs.(2017-11-01)

+ [ ] 2. Using Apache ab test tool for Performance Test & Optimize server.(2017-11-10)
+ Performance Test for using different value  of Concurrency Level parameter and the number of requests parameter.And analysis the result using table or graph. (2017-11-10)
+ Load Test.Test the program in overload environment and analysis the conditions when program is not working using table or graph.(2017-11-10)
+ Optimize server is mainly to optimize the conf of nginx.(2017-11-10)

+ [ ] 3. Write the documents in github and others needed by this study.(2017-11-25)     
** This documents includes: **  
+ architecture model
+ er model
+ sql files
+ class diagrams
+ front_end_design files
+ --
+ introduction of functions
+ statusNumber list
+ introduction of used frameworks and librarys
+ server enviroment building shell
+ test result analysis documents
+ --
+ gantt chart file
+ progress of project file
