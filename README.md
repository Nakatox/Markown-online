Template BDD
(Go to line 9 of "app.py". Change login to your database)

Members :
    Fabian Zuo
    Rinoshan Vijayakumar
    Vincent Loron

Table data :
    id : INT/primary key
    content : TEXT
    url : VARCHAR(255)

Packeage used
    - shortuuid
    - markown
    - mysql / connector
    - flask

Pages
    - create article (path :"/")
    - read article (path :"/articles/<article_url>")
    - admin page (path :"/articles/admin")
    - edit article (path :"/articles/admin/update/<article_id>")