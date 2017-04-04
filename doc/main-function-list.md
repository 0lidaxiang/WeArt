# Main-function List
> Author: 李大祥
StartTime :   2017-3-28
ModifyTime :  2017-4-2

## 1. Reader (From Reader View)
+ [ ] 1. Reader can see different kinds of novels collections from main website page.
+ [ ] 2. Reader can search novels by keywords.
+ [ ] 3. Show the outline of novel for readers.
+ [ ] 4. In every chapter page, we will first show the version most people liked. And this page must include author information
+ [ ] 5. Reader can set his/her preference about which version he/she like and then we should show this branch to him/her firstly.
+ [ ] 6. Collect novels that he likes.
+ [ ] 7. Reader can select register or not using password to login and then they can look at their history and collection. And they can select to or not become authors.
+ [ ] 8. Reader can vote and like a novel or a chapter.
+ [ ] 9. If people register, he/she could change it primary email and add an spare email.

## 2. Author (From Author View)
+ [ ] 1. Create a novel, including title(tens words), outline(Thousands words,maybe tens thousand), writing plan(delay time, task, is_finish).
+ [ ] 2. Claim one task and update this task to claimed at the same time.
+ [ ] 3. Commit the chapter and update this task to claimed at the same time.
+ [ ] 4. Close his/her novel created by him/her.
+ [ ] 5. If the author asks to Delete his/her novel, we will mark this novel deleted and this novel must be found by searching.This means it will not be show in any sorting views.
+ [ ] 6. Collect novels created by Author.
+ [ ] 7. Collect novels liked by Author.
+ [ ] 8. Show these detail of novels created by Author. These details include that the number of people like it, the number of people dislike it, the number of people read it, the link that shows the detail of every chapter. We will select five branches of all branches. And these main branches of this novel and main branch's details like above.
+ [ ] 9. Show these detail of every chapter in this novel. These detail include
that the number of people like every chapter, the number of people dislike every chapter, the number of people read every chapter, the version of every chapter, the branch of every chapter.
+ [ ] 10. Author and contributors can delete their novel's chapter but also can submit to recover. Submitter can complaint about them to administrator but needing reasonable reasons.

## 3. Administrator (From Administrator View)
+ [ ] 1. Manage novels.These info includes but not limiting that the number of likes, the number of views, the author,the number of contributors, the number of words, the branches, the name, the creating time, the chapter finished, the finished percentage, the status(finished or interrupted or writing or other) and so on. **Administors can ban or delete novels and chapters.**
+ [ ] 2. Manage authors and users. These info includes but not limiting that people's primary email and spare email for accounts, nickname, contribution, his/her arts links and so on. **Administors can caveat or ban or delete authors and users.**
+ [ ] 3. Manage temporary accounts.**Administors can ban or delete temporary accounts.**
+ [ ] 4. An button for sending some info to some users by emails.

## 4. The Model and Architecture

[Newest Model and Architecture Diagram from draw.io](https://www.draw.io/?lightbox=1&highlight=0000ff&edit=_blank&layers=1&nav=1&page=1&title=WeArt#R%3Cmxfile%3E%3Cdiagram%20name%3D%22Core%20Logic%20Model%22%3E7VtNc6M4EP01XF2AQEhHSOzZy1ZN7Rx290iA2NTYJoXJ1%2F767dYHBiFiTOxMZnZzSECAkPq1Xr9uFIfc7F6%2B1OnD5vcqL7aO7%2BYvDrl1fJ9FPvzGhlfZEASebFjXZS6bOg3fyn8K1eiq1scyLw69G5uq2jblQ78xq%2Fb7Imt6bWldV8%2F92%2B6rbf%2BtD%2Bm6GDR8y9LtsPXPMm82qtWj%2FHjht6Jcb9SrmU%2Flhbs0%2B76uq8e9ep%2Fjk3vxIy%2FvUt2Xmuhhk%2BbVc6eJLB1yU1dVI492LzfFFk2rzSafW41cbcddF%2FtmygOBGsdTun1Uc3eWocNCJ6HOMnCSxOFwEDmMO4w5S%2BrwGye%2BUYNvXrXBNs1uC0eeQ5J2Si6c5OlhU%2BTqJN2W6z0cZzC4ooaGp6JuSrB6rC7syjzHHrGPB%2Bx597JG%2F1pITH35F7t91f2jx3l4tK%2BabKNa78vt9qbaVrUYHCCQ5T6DdugsL%2BHlvWtp6OIzddWkTVnhMLwIGw5NXX0vOrfmEb8Ttw6NrOyO8yleOk3K6F%2BKalc09Svcoq5y7QBqgXg8kufPHXfT4Gw6nqafS5WHr9uujyjDgQJ6BHTvf9AHoJOrY07Bll3MgU8%2BDnPC%2F0uYn7GY33KPSyx011joGohToHvkAqBbMAeobxHbJXOYi%2FiDF8RLJ%2FYQ89h1EnBSuoVBJHc1HK2b1g4dL4DXQChGAJ83ZVN8e0gzvPIMGEJbx0cGAN37WWbFg97RkI7hkXNKL7QI%2B3BA5B7C4VvgYBdYg3QIhzJ1Xj4dbS2bDg%2Fpvm1D1G4cznCBxhECd8QxdDhxmKefg0H0Hj02915iACoki1i%2F3gxQ1ar7YYuslTFabnoTUaUXQNWzRFMrhsyJVw4LBO3C4qOKZJNYtQARj2H4yyw%2FE6kwIB%2B3%2FrRXnEQKlhRQ41LgsnISd5wjf12kAiNw%2BfQDmdILLUiZpt3nsVQJt9k2PRzKrG9RmHr9%2BhcKhUWoT%2F%2FW117KpnMJzv5WimLUcofqsc50eqhz0rReF5pKZFOR9zLLoXk75gst1tNtdbEFBfPUz0dtJlVv%2BFqVMOAWPRJG%2FXWmLaq7kNNRT3UTRKOjwOgocI2OpA0GHQE06Wvntge84TDwgdYw09zCFkHnu4Ub%2BF3HgIaw4xtexzPaB78WdQkDRlE73V3Ip%2FcWz1jr3J%2FnLYOOfKOjD%2FWW6KLewmn0hre4F%2FMWHaU%2Br7sE%2FATKU90lpMSIMdGPcxd%2Fmo77o0hzANR3lToATSfT5zhEdY55ND%2BhxU%2BqfSqUouwYVGOcQZbctC%2BFxcluzpT7017s03SHumR%2FdxB%2FqidR1rVJ1xUmJCeHMUhiRMpyjaF301lpIGhJAqHZIjwF%2Fdbec86gGQr0OFEgwwSuMnronDt8ddbItPudCYHw1PMsYIJPhB39M00xKo11ESjbVo%2F5aal8AXFLjDIAJRZxSy0Myg2CmiNuNVueHZcOQIfN2%2BHKol068lfJHiOOBe8LVxYtrO%2F7LPEqMsQwnSmGQyMnCs1cZyRezYlGltrd2IqGBRroytCtvc6AVV0ZsW4xgX13fOK3DiPOEnqV75T1qVjnx1y88xZJ90pkD1OUAZcDx4t6NVZQIsvsz6TU5elnZg5aFhNk2T3Wg3axdIdBxhUGBcuGGLZ%2BWmb1jCVCAwuz2urdF2HW4HrMeuRPxvr86bf8ahKoLTmQdDyfWsmnolbaZ1YazWRWYjJrRK%2FGrLba0lty9SxpiZRI8MGJ8myKMpS5RYidKWZdYYESL8WK%2BoF6FefR4zed5FQiMl%2BsTtDxA%2FKLRKmbog1x0BypWwYlOGVyGu6voS8Neem5E2unLXu%2BiwXnVsnOYsFeTbVHdouwV1RdcH06S1%2Fq5dolwc%2FFgZ7xTQP05jwS9Iy6imfGxAuSoK02NvVTiFn1YIJsTkm9k7QSYZrNhLyEF6I%2BYqghkelAVYpvZT8%2FM5gVUs8fbvzhNnl0CWJgQ9AnAWzjbL4UgjUUnzCX46Fn0i6Cj8ch1N8xNA6WT8bXwoFYNt1dgaD7DK1o%2BBoy1VKw1l79SSi6%2Ffz13g8cbemg5Xqjo8tRNLHVoy9bJgKncFkPdH8kVHf8yiN9v4qiMb%2Ba7z3sU3kPZX3OJv5M74mIoRSi63nPhFT4g%2Fby4RvLQ6E9Ve3pW0Toa2Jbn88XHE%2F0zj7fXQi3vC%2FSZiO9SRQph%2FuOMs6FsqiLTG33ey4OQlmY2yYIJZzkl4kdgbF517bdyBo8zOx4VvCwpK%2ByCJgIDQU5VrKyaa5jAinyRgz5wwyXdCpSYxlue88wER1%2BYDmRX6onxBBicdx%2BWRpOSimTWG2cYlzIj0BrFfn4cAfr5LF00miYTBzpN%2FtH3Wkxoig4Jt0vUONzmj6W4eQp7v%2BLV7byobAL7g4M8SVyH6%2BaioAYc2rbx0qwXeKdBZY5VVFWZrIoAb3yzpuHUn1araErGN%2F9aOcmbzG6BQ8h4ph9yB2WagIiH4nF108wOPM7uzDFxmkmDsCAXBgzFh4xdcj%2BQqhpphxG2VXW01fKA7Ge%2FjGjIYuOJSh6UCIPEqSBY0vXrXS9H%2BewVAfJssMKHA3MTzjAiVTt59hu%2Ftb21vFNsd2wBQoCI8clohMzSqnWAnw4DE50RmoDp8f%2FVZIq5fj%2FYGT5Lw%3D%3D%3C%2Fdiagram%3E%3Cdiagram%20name%3D%22Tech%20Model%22%3E7Vldb5swFP01eUUYA8GPbdp1L5MmRVOfDTZg1cSRcZtkv342mAaC2%2FWDoaxtkCL7XH%2BeY1%2BbywKuqv2NxNvyhyCULwKf7BfwahEEYaz%2FTP5g8yFogUIy0kI9YM1%2BUwv6Fr1nhNaDgkoIrth2CGZis6GZGmBYSrEbFssFH%2Fa6xQUdAesM8zF6y4gqWzQJ4iP%2BnbKi7HoGMWotKc7uCinuN7a%2FRQDz5teaK9y1ZSdal5iIXQ%2BC1wu4kkKoNlXtV5QbZjva2nrfnrA%2BjlvSjXpJhaCt8ID5vZ36DVNrKh%2BotANUh44UPdatSWYHzjZEF4CXu5Iput7izOA7vRI0VqqK6xzQyZxxvhJcyKYBmEfm0XitpLijPUvc%2FLRlPH47JT0gRfc9yM7nhoqKKnnQRTpr6Fty7eILIpvfHaWMLVT2VAwthu3iKR6bPhKoE5ZDN5%2FhiM9ftYPKZoVQYml6HYtZRiO9nhwswhgiSKZhEYEhidCfj8ToMyxKhGbjM%2F4EfMIZN3ky4tPzvA%2FDZDjjTgdjf7kIYq57uCTsQScL1cyyheot3pxiqTxFdJ%2Bughp2NPmJermlabfnn23cOYqXdfdV9avqnFXf7XEJk%2Fr1gYmNzlNcqzc54UJiwrQD7tnS5pnIQYPk7%2FdZAJZjDw3QBC4ajTz0z4MqNWNPsa8nizmnXGheqlcfetcXcAmgi%2B80iUI9cyffFMfpZAdi4CfDq0V3Ie0fiHBMdwDfzzZ863l4hRVOcU3f7dxn2FME0yTPnHsqS2iauzVeapGpP5XGAAw1RsmLLj3BcoJLj0vkE9p7fD6GCMzcCa7L5r3RZDBnhWE500Q0yhgCWIb5hTVUjBDT4mWnYrUvTLjGa2Mkgad24hYfLkzONG7I8L0oMGnDFACeb%2FaiFApbRZHv8JF5RvSl2KEnWaLUf2LP5jmO%2FMn0DE5eB%2BKxnqFDTzDFJXbsIs9Kz7iTE0bnqB06Od4gcBxvyLUXJ9Cua%2BNctQtRJ14QeQieo34Anr6KOwREjvMSRBPoB0b6fZCA25xRS0cY%2BIOwOGdYyHF5c8WF%2Fj8S%2F2FESGePHzsaW%2B97Erz%2BAw%3D%3D%3C%2Fdiagram%3E%3C%2Fmxfile%3E)
