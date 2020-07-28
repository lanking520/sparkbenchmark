from pyspark.sql import SparkSession
import torch
from urllib import request
import tempfile
import time
import zipfile

def downloadFromUrl(url):
    tmp = tempfile.TemporaryDirectory()
    modelDir = tmp.name
    modelName = url.split("/")[-1].split(".")[0]
    modelPath = modelDir + "/" + modelName + ".pt"
    zipPath = modelDir + "/" + modelName + ".zip"
    # Start download
    filedata = request.urlopen(url)
    datatowrite = filedata.read()

    with open(zipPath, 'wb') as f:
        f.write(datatowrite)
    with zipfile.ZipFile(zipPath, 'r') as zip_ref:
        zip_ref.extractall(modelDir)
    return modelPath, tmp

def inferenceOnPartion(iter):
    file, tmp = downloadFromUrl("https://djl-ai.s3.amazonaws.com/resources/demo/pytorch/traced_resnet18.zip")
    model = torch.jit.load(file)
    model.eval()
    result = []
    tmp.cleanup()
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
    "players.csv", header=True, mode="DROPMALFORMED")

print('Partition cnt: ' + str(df.rdd.getNumPartitions()))

rdd = df.rdd.mapPartitions(inferenceOnPartion)

start = time.process_time()
result = rdd.collect()
elapsed_time = time.process_time() - start
print(result)
print(elapsed_time)
