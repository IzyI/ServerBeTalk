CREATE TABLE IF NOT EXISTS protokol
(
    id      SERIAL PRIMARY KEY,
    name    CHARACTER VARYING(200),
    accaunt CHARACTER VARYING(200)
);



CREATE TABLE IF NOT EXISTS users
(
    id              SERIAL PRIMARY KEY,
    id_user_accaunt INTEGER,
    nickname        CHARACTER VARYING(200),
    id_protokol     INTEGER REFERENCES protokol (id),
    info            jsonb
);

CREATE TABLE IF NOT EXISTS talk_user
(
    id      SERIAL PRIMARY KEY,
    id_user INTEGER REFERENCES users (id),
    info    jsonb
);
