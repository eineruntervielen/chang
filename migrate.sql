-- SQLite
-- DROP TABLE task;
CREATE TABLE IF NOT EXISTS task(
    task_id INTEGER PRIMARY KEY,
    label TEXT,
    summary TEXT
);

INSERT INTO task (label,summary)
VALUES ("Erster Task", "hier sollte etwas längerer text stehen");
INSERT INTO task (label,summary)
VALUES ("Zweiter Task", "bei einem andeeren task steht hier vielleicht noch mehr");


