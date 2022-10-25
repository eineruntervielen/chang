-- SQLite
CREATE TABLE IF NOT EXISTS task (
    task_id INTEGER PRIMARY KEY,
    label TEXT
);

INSERT INTO task (task_id,label)
VALUES (1,"Erster Task");
INSERT INTO task (task_id,label)
VALUES (2,"Zweiter Task");

select * from task;


