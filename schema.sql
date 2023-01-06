DROP TABLE IF EXISTS clientes;
CREATE TABLE clientes (
  id integer primary key autoincrement,
  nome string not null,
  email string not null,
  cpf string not null,
  tipo string  null,
  time_coracao string null
);
