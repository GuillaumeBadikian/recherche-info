# recherche-info

#### dependencies
 - numpy
 - pandas
 - PyYAML
 - rank_bm25
 - keras
 - keras_preprocessing
 - nltk
 - xmltodict
 - colorama
 - matplotlib
 - jinja2
 
 
 
 


#### configuration file
```yaml
run:
  b: 0.4 #bm25 b
  d: 1 #bm25 delta
data:
    file: data/data.json # filename for indexing
    overwrite: true # rewrite data.json if exist 
    path: data/coll # data folder
  granularity: articles # or element
  k: 0.8 #bm25 k1
  num: 44 #run number
  staff: #for report
  - Guillaume
  - Benoit
  - Gauthier
  - Theo
  step: 4 #for step
  weighting: bm25 #method to use
  compare: filename #file to compare in runs/
  limit: 1500 # limit of result per request
query:
    - id:
      - word1
      - words2
```

#### execute program
```shell script
cd recherche-info
python -m manage
```

#### Compare 2 runs:
```shell script
cd recherche-info/src/compare
python -m compare_run
``` 

#### show MAgP
```shell script
cd recherche-info/src/compare
python -m result
``` 

