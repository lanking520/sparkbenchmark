from pyspark.sql import SparkSession
import torch
from urllib import request
import tempfile
import os
import zipfile
PARTITION_NUM = 10

def downloadFromUrl(url):
    tmp = tempfile.gettempdir()
    modelDir = tmp + "/benchmodel"
    modelName = url.split("/")[-1].split("\\.")[0]
    modelPath = modelDir + "/" + modelName + ".pt"
    zipPath = modelDir + "/" + modelName + ".zip"
    if os.path.exists(modelPath):
        return modelPath
    # Start download
    filedata = request.urlopen(url)
    datatowrite = filedata.read()
    os.mkdir(modelDir)

    with open(zipPath, 'wb') as f:
        f.write(datatowrite)
    with zipfile.ZipFile(zipPath, 'r') as zip_ref:
        zip_ref.extractall(modelDir)
    return modelPath

def inferenceOnPartion(iter):
    file = downloadFromUrl("https://djl-ai.s3.amazonaws.com/resources/demo/pytorch/traced_resnet18.zip")
    model = torch.jit.load(file)
    model.eval()
    model.share_memory()
    result = []
    for _ in iter:
        t = torch.ones((1, 3, 224, 224))
        out = model(t)
        result.append(str(out.shape))
    return result


spark = SparkSession \
    .builder \
    .master("spark://localhost:7077") \
    .appName("Python Spark Benchmark") \
    .getOrCreate()


df = spark.read.csv(
    "players.csv", header=True, mode="DROPMALFORMED") \
    .repartition(PARTITION_NUM)

print('Partition cnt: ' + str(df.rdd.getNumPartitions()))

rdd = df.rdd.mapPartitions(inferenceOnPartion)
result = rdd.collect()

print(result)
