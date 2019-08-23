from __future__ import print_function

import sys
from random import random
from operator import add

# from pyspark.sql import SparkSession

from pyspark import SparkContext
from pyspark import SparkConf


if __name__ == "__main__":
    """
        Usage: pi [partitions]
    """
    # spark = SparkSession\
    #     .builder\
    #     .appName("PythonPi")\
    #     .getOrCreate()
    conf=SparkConf().setAppName("pi-example").setMaster("spark://127.0.0.1:7077")
    sc=SparkContext.getOrCreate(conf)
    partitions = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    n = 100000 * partitions

    def f(_):
        x = random() * 2 - 1
        y = random() * 2 - 1
        return 1 if x ** 2 + y ** 2 <= 1 else 0

    count = sc.parallelize(range(1, n + 1), partitions).map(f).reduce(add)
    print("Pi is roughly %f" % (4.0 * count / n))