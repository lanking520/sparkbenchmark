/*
 * Copyright 2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance
 * with the License. A copy of the License is located at
 *
 * http://aws.amazon.com/apache2.0/
 *
 * or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES
 * OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions
 * and limitations under the License.
 */
package com.examples

import ai.djl.ndarray.types.Shape
import ai.djl.ndarray.NDList
import ai.djl.repository.zoo.{Criteria, ModelZoo, ZooModel}
import ai.djl.training.util.ProgressBar
import ai.djl.translate.{Batchifier, Translator, TranslatorContext}
import org.apache.spark
import org.apache.spark.sql.SparkSession
import org.apache.spark.{SparkConf, SparkContext}

object DataProcessExample {

  private lazy val model = loadModel()

  def loadModel(): ZooModel[NDList, NDList] = {
    val modelUrl = "https://djl-ai.s3.amazonaws.com/resources/demo/pytorch/traced_resnet18.zip"
    val criteria = Criteria.builder
      .setTypes(classOf[NDList], classOf[NDList])
      .optModelUrls(modelUrl)
      .optTranslator(new MyTranslator)
      .optProgress(new ProgressBar)
      .build()
    // load torchscript traced model
    ModelZoo.loadModel(criteria)
  }

  // Translator: a class used to do preprocessing and post processing
  class MyTranslator extends Translator[NDList, NDList] {
    override def processInput(ctx: TranslatorContext, input: NDList): NDList = {
      input
    }

    override def processOutput(ctx: TranslatorContext, list: NDList): NDList = {
      list
    }

    override def getBatchifier: Batchifier = null
  }

  def main(args: Array[String]) {

    val spark = SparkSession.builder()
      .appName("DJL Benchmark Job")
      .master("spark://localhost:7077")
      .getOrCreate()

    val df = spark.read.option("header", true).option("mode", "DROPMALFORMED").csv("players.csv")
    // Start assign work for each worker node
    val result = df.rdd.mapPartitions(partition => {
      // We need to make sure predictor are spawned on a executor basis to save memory
      val predictor = model.newPredictor()
      partition.map(streamData => {
        val array = model.getNDManager.ones(new Shape(1, 3, 224, 224))
        val out = predictor.predict(new NDList(array)).singletonOrThrow()
        val shape = out.getShape
        array.close()
        out.close()
        shape.toString
      })
    })

    // The real execution started here
    result.collect()
  }
}
