# BDT, Praktikumsbericht 3

Gruppe 21: Maximilian Neudert, Kai Pehns

---

## Vorbereitung

### Postgres

Da war erstmal nichts zu machen. Dennoch zur Erinnerung die alten postgres Befehle, die man auf `postgres.fbi.h-da.de` abgesetzt hat.

```sql
insert into public.user values (generate_series(1,1000000));

\copy public.movie FROM '/pgpool/movielens/adjusted/1m/movies.dat' with (format csv, delimiter ';');

\copy public.genre FROM '/pgpool/movielens/adjusted/1m/genres.dat' with (format csv, delimiter ';');

\copy public.rating FROM '/pgpool/movielens/adjusted/1m/ratings.dat' with (format csv, delimiter ';');
```

### MongoDB

Wir loggen uns in [faircastle](faircastle.fbi.h-da.de) und öffnen die Mongo Shell.

```bash
mongo \
--username prak21 \
--password prak21 \
--authenticationDatabase prak21
```

Anschließend löschen wir die alte Collection

```javascript
use movies
db.movies.drop()
exit
```

und fügen die neuen Daten ein.

```bash
mongoimport \
-u prak21 -p prak21 \
--db prak21 \
--collection movies \
--file /mnt/datasets/Movielens/JSON/movies_20m.json
```

### Couchbase

Zuerst loggen wir uns in [silverhill-web](http://silverhill.fbi.h-da.de:8091/ui/index.html) ein und dann löschen wir die alten Dokumente über das web interface. Alternativ hätte auch folgendes Command funktioniert, wenn `enable-flush` gesetzt wäre.

```bash
couchbase-cli bucket-flush -c localhost:8091 -u prak21 -p prak21 --bucket=prak21
```

Danach loggen wir uns in [faircastle](faircastle.fbi.h-da.de) ein und importieren den `20m` Datensatz.

```bash
cbdocloader \
-u prak21 -p prak21 \
-b prak21 \
-c localhost:8091 \
-m 100 \
/mnt/datasets/Movielens/couchbase/movies_20m.zip
```

<div style="page-break-after: always;"></div>

## Aufgabe 1
