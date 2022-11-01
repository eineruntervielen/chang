CREATE TABLE IF NOT EXISTS task(
    task_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    summary TEXT,
    label TEXT,
    state TEXT
);

INSERT INTO task (title, summary, label, state)
VALUES ("Erste Aufgabe", "Blablabla eine Aufgabe nervt und kostet nur Zeit", "Privat", "Offen");
INSERT INTO task (title, summary, label, state)
VALUES ("Zweite Aufgabe", "eMails von den Studenten beantworten", "OTH", "Offen");
INSERT INTO task (title, summary, label, state)
VALUES ("Dritte Aufgabe", "Vorlesung für Donnerstag vorbereiten", "OTH", "Offen");
INSERT INTO task (title, summary, label, state)
VALUES ("Vierte Aufgabe", "Lasagne fertig machen", "Privat", "Aktiv");
INSERT INTO task (title, summary, label, state)
VALUES ("Fünfte Aufgabe", "Gemüse schneiden!!!", "Privat", "Geschlossen");


