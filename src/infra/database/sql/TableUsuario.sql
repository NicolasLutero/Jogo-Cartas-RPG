CREATE TABLE IF NOT EXISTS usuario (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    nome TEXT UNIQUE,
    senha TEXT NOT NULL,
    fator_n NUMERIC(38, 36),
    data_reforjar DATE,
    data_cartas_diarias DATE,
    data_fundir DATE
);
