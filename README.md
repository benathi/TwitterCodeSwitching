Ben Athiwaratkun (c) 2014

__________________________________________________
This repository is the code base for code-switching NLP project. 
The goal is to identify significant n-grams  that contribute 
to the occurrence of code-switching. The ML algorithm used is lasso 
regression. This also gives a predictor of whether there will be a 
code-switching instance given the features(n-grams). 

Future work: refine the determination of code-switching with translation API. 
This will generalize the work to more general base language. 


Author's note: The code could be cleaner but I figured I should make
the code public in case it might help others. I plan to clean this up soon.

https://github.com/benathi/TwitterCodeSwitching/blob/master/Report/code-switching-project.pdf
___________________________________________________
The following packages are required to run the code

1. C enchant
Install: brew install enchant
2. Python Enchant
Install: pip install pyenchant
3. Python NLTK
Install: pip install nltk

4. Language Identification : Recommended by Code Switching Community
https://github.com/saffsd/langid.py
Install: pip install --pre langid

5. CMU ARK Twitter Part-of-Speech Tagger

6. Install libthai (C library from sourceforge)
	- compatible with ubuntu 13.01
7. Install pythai
	pip install pythai
