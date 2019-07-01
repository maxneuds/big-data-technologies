# BDT, Praktikumsbericht 4

Gruppe 21: Maximilian Neudert, Kai Pehns

---

## Aufgabe 1

Zuerst verbinden wir uns auf den Cluster

```bash
ssh <istuser>@lannisport.fbi.h-da.de
```

anschließend erstellen wir neue Ordner für das Hadoop Filesystem

```bash
hdfs dfs -mkdir /user/<istuser>
hdfs dfs -mkdir /user/<istuser>/praktikum6
```

und schließlich kopieren wir die aufgearbeiteten Daten dort hin

```bash
cd /mnt/datasets/Grouplens/JSON
hdfs dfs -put movies_* /user/<istuser>/praktikum4
```

und überprüfen diese im [Hadoop Explorer](http://lannisport.fbi.h-da.de:50070/explorer.html#/).
