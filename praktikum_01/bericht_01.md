# BDT, Praktikumsbericht 1

Gruppe 21: Maximilian Neudert, Kai Pehns

---

## Aufgabe 1

#### UML

_UML Bild hier_

Die Angaben wurden übernommen, wie gestellt. Es waren keine besonderen Anpassungen nötig.

#### SQL

_SQL Bild hier_

Fast direkte Übertragung des UML in das relationale Modell. Wichtig sind die Referenzen mit den Foreign Keys. Wir haben zur Modellierung die Entscheidung getroffen für die `Movie` Tabelle `Title` und `Year` in zwei Spalten zu trennen. Einfacherheitshalber wird aber erst eine `MovieYear` Spalte erstellt, damit der Datenimport einfacher ist und anschließend geteilt.

#### Document Store

_NOSQL Bild hier_

Hier hatten wir bei der Übertragung des UML die Entscheidung zu treffen, ob wir die Ratings an das `User` oder an der `Movie` Dokument anhängen. Wir haben uns dazu entschieden die Ratings in das `Movie` Dokument zu integrieren, da es intuitiv wahrscheinlicher ist, dass man zur Informationsgewinnung `Movie` iteriert. Dies hat zur Folge, dass das `User` Dokument sehr simpel ist.

## Aufgabe 2

Die Datei `movies.dat` enthält folgende Struktur

```bash
MovieID::Title::Genres
```

Zuerst haben wir festgestellt, dass `::` als Trennzeichen für die Spalten und `|` für Elemente in den Spalten genutzt wird. Dies ist später für den Import der Daten wichtig. Ansonsten gab es keine Unterschiede zur Modellierung.

Die Datei `ratings.dat` enthält die Bewertungen mit den gleichen Trennzeichen.

```bash
UserID::MovieID::Rating::Timestamp
```

Ein Unterschied zu der geplanten Modellierung ist, dass zusätzlich noch eine Spalte `Timestamp` existiert. Diese sollte dann noch für den Import in der SQL Datenbank erstellt werden.

## Aufgabe 3

#### PostgreSQL
