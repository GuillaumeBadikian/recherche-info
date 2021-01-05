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
  granularity: articles
  k: 0.8 #bm25 k1
  num: 44 #run number
  others: #for report : unused, just for information
  - k0.8 
  - b0.4
  staff: #for report
  - Guillaume
  - Benoit
  - Gauthier
  - Theo
  step: 4 #for step
  weighting: bm25 #method to use
  compare: filename #file to compare in runs/
```

#### execute program
```shell script
cd recherche-info
python -m manage
```


