# BDT, Praktikumsbericht 4

Gruppe 21: Maximilian Neudert, Kai Pehns

---

## Aufgabe 1

[Hadoop](https://wiki.h-da.de/fbi/bigdata/index.php/Installierte_Software#Hadoop)

## Aufgabe 2

Zuerst verbinden wir uns auf den Cluster

```bash
ssh <istuser>@lannisport.fbi.h-da.de
```

anschließend erstellen wir neue Ordner für das Hadoop Filesystem

```bash
hadoop fs -mkdir /user/<istuser>
hadoop fs -mkdir /user/<istuser>/praktikum4
```

und schließlich kopieren wir die aufgearbeiteten Daten dort hin

```bash
cd /mnt/datasets/Grouplens/JSON
hadoop fs -put movies_* /user/<istuser>/praktikum4
```
