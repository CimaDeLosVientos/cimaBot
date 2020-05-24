CREATE TABLE IF NOT EXISTS `Place` (
    `id`    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `name`  TEXT NOT NULL UNIQUE,
    `description` TEXT
);


CREATE TABLE IF NOT EXISTS `Tag` (
    `id`    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `name`  TEXT NOT NULL UNIQUE
);


CREATE TABLE IF NOT EXISTS `Adventurer` (
    `id`    INTEGER PRIMARY KEY AUTOINCREMENT,
    `name`  TEXT NOT NULL,
    `complete_name` TEXT NOT NULL,
    `birth_date_day`    INTEGER NOT NULL,
    `birth_date_month`    INTEGER NOT NULL,
    `birth_date_year`    INTEGER NOT NULL,
    `registrer_date_day`    INTEGER NOT NULL,
    `registrer_date_month`    INTEGER NOT NULL,
    `registrer_date_year`    INTEGER NOT NULL,
    `sex`   INTEGER NOT NULL,
    `race`   TEXT NOT NULL,
    `id_from`   INTEGER,
    `formation` TEXT,
    `especialiation`    TEXT,
    `work_experience`   TEXT,
    `testament` TEXT,
    `room`  INTEGER,
    `rank`  INTEGER,
    `on_service`    INTEGER,
    FOREIGN KEY(id_from) REFERENCES Place(id)
);


CREATE TABLE IF NOT EXISTS `Character` (
    `id`    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `name`  TEXT NOT NULL,
    `id_adventure` INTEGER,
    `player` TEXT,
    `experience_points`    INTEGER NOT NULL,
    `level` INTEGER NOT NULL,
    `money` INTEGER NOT NULL,
    FOREIGN KEY(id_adventure) REFERENCES Adventurer(id)
);


CREATE TABLE IF NOT EXISTS `Especialization` (
    `id_adventurer` INTEGER NOT NULL,
    `id_tag`    INTEGER NOT NULL,
    FOREIGN KEY(id_adventurer) REFERENCES Adventurer(id),
    FOREIGN KEY(id_tag) REFERENCES Tag(id)
);

CREATE TABLE IF NOT EXISTS `Quest` (
    `id`    INTEGER PRIMARY KEY AUTOINCREMENT,
    `day`    INTEGER NOT NULL,
    `month`    INTEGER NOT NULL,
    `year`    INTEGER NOT NULL,
    `summary`  TEXT NOT NULL,
    `id_place` INTEGER NOT NULL,
    `reward`    INTEGER NOT NULL,
    `rank`   INTEGER NOT NULL,
    `master`   TEXT NOT NULL,
    FOREIGN KEY(id_place) REFERENCES Place(id)
);

CREATE TABLE IF NOT EXISTS `Report` (
    `id`    INTEGER PRIMARY KEY AUTOINCREMENT,
    `id_quest`  INTEGER NOT NULL,
    `day`    INTEGER NOT NULL,
    `month`    INTEGER NOT NULL,
    `year`    INTEGER NOT NULL,
    `summary`  TEXT NOT NULL,
    `id_lead` INTEGER NOT NULL,
    FOREIGN KEY(id_quest) REFERENCES Quest(id),
    FOREIGN KEY(id_lead) REFERENCES Adventurer(id)
);

CREATE TABLE IF NOT EXISTS `Team` (
    `id_adventurer_1` INTEGER NOT NULL,
    `id_adventurer_2` INTEGER NOT NULL,
    `id_report`       INTEGER NOT NULL,
    FOREIGN KEY(id_adventurer_1) REFERENCES Adventurer(id),
    FOREIGN KEY(id_adventurer_2) REFERENCES Adventurer(id),
    FOREIGN KEY(id_report) REFERENCES Report(id)
);
