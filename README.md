# retrofitting

- [ported Faruqui's implementation](https://github.com/mfaruqui/retrofitting) to Python 3


```
Usage: retrofit.py [OPTIONS]

Options:
  -i, --input TEXT          Input word vectors  [required]
  -l, --lexicon TEXT        Lexicon file name  [required]
  -o, --output TEXT         Output word vectors  [required]
  -n, --iterations INTEGER  Number of iterations  [default: 10; required]
  --help                    Show this message and exit.
```
### Requirements
* Python 3.6+
* [click](http://click.pocoo.org)
### Reference 
```
@InProceedings{faruqui:2014:NIPS-DLRLW,
  author    = {Faruqui, Manaal and Dodge, Jesse and Jauhar, Sujay K.  and  Dyer, Chris and Hovy, Eduard and Smith, Noah A.},
  title     = {Retrofitting Word Vectors to Semantic Lexicons},
  booktitle = {Proceedings of NAACL},
  year      = {2015},
}
```
