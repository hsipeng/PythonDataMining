from pyspark import SparkContext
from pyspark import SparkConf
import os
cwd=os.getcwd()
conf=SparkConf().setAppName("miniProject").setMaster("spark://127.0.0.1:7077")
sc=SparkContext.getOrCreate(conf)
textFile = sc.textFile("file:///"+cwd + "/word.txt")
wordCount = textFile.flatMap(lambda line: line.split(" ")).map(lambda word: (word,1)).reduceByKey(lambda a, b : a + b)
wordCount.foreach(print)