# Bsc-Final-Project
Bsc SW Eng. degree final project - improving performance for an RNN based LSTM language model using TensorFlow for Python

## How to Run
Make sure your current working directory is the project's root folder
python main.py

## Assumptions
we assume of the following:
1. Your vocab file fits in memory (train, test and validation is unlimited)
2. We need the num batches of each {train, test, validation} to be inserted into hyperparameters.json
this is due to the fact that tf.data.Dataset loads in mini batches your data without taking into how much data there is.