Command2Vec
=========================


### Abstract

Command2Vec is an embedding algorithm designed for clustering 3D modeling behavior sequences in design industries. Its input data is originally extracted from Command-object graph which is a data structure retrieved from event logs generated during modeler’s 3D modeling process. Command graph can represent the modeler’s operational ‘map’ during the modeling process. Command2Vec is applied in a study of 112 participants modeling on a ‘spiral stair’ task. By extracting the event log generated in each participant’s modeling process into command graph, we classified their behavior sequences into certain groups using Command2Vec. To verify the effectiveness of our classification, we use external evaluation by inviting experts with extensive modeling experience to grade the classification results. The final grading show that our algorithm performs well in some clustering results that were with significant features.


![Alt](./workflow.png#pic_center=100x)

This repository provides an implementation for Command2vec in:
Paper link


### Requirements

The codebase is implemented in Python 2.7.18 | Anaconda3 (Python 3.8.5 64-bit). Package used for development are just below.
```
numpy             
gensim           
matplotlib        
sklearn
```
