CREATE DATABASE tut_news;
-- DROP DATABASE tut_news;
-- Команда на переключение текущей базы данных -  \c tut_news

CREATE SEQUENCE rubric_id_seq;

CREATE TABLE rubrics (
	id INTEGER NOT NULL PRIMARY KEY DEFAULT nextval('rubric_id_seq'),
	name VARCHAR(50) NOT NULL
);

CREATE SEQUENCE news_id_seq;

CREATE TABLE news (
	id	INTEGER NOT NULL PRIMARY KEY DEFAULT nextval('news_id_seq'),
	head	VARCHAR(256) NOT NULL,
	text	TEXT NOT NULL,
	link	TEXT NOT NULL,
	date	DATE NOT NULL,
	rubric_id	INTEGER NOT NULL
);


ALTER TABLE news ADD FOREIGN KEY(rubric_id) REFERENCES public.rubrics(id) ON DELETE CASCADE;

INSERT INTO rubrics (name) VALUES ('Test rubric');

INSERT INTO news (head, text, link, date, rubric_id) VALUES
('News 1', 'Very big text', 'https://tut.by/', '2020-06-20', 1),
('News 2', 'Very hardtext', 'https://tut.by/', '2020-06-21', 1);

INSERT INTO news (head, text, link, date, rubric_id) VALUES
('News 3', 'ajsdf ajsdfh ', 'https://tut.by/', '2020-06-22',
(SELECT id FROM rubrics WHERE name = 'Test rubric')
);
