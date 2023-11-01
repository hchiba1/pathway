# pathway

## Original data

ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/docs/pathway.txt

## Processed data

```
$ cd ftp/
$ ls
pathlist.txt  pathway.txt
$ ../bin/pathway.py > ../tsv/pathway.tsv 2> ../tsv/pathway.err
$ cd ../tsv/
$ cut -f4 pathway.tsv | sort | uniq > pathway.sorted
```
