# Addi Challenge
The current repository contains infraestructure as code, deployment and application logic to serve a very simple machine learning architectured composed of a feature + model + evaluation store.


## Challenge steps:
1. Train model and save in a model.joblib file in  https://github.com/RomuloSilvaRosa/addi_challenge/blob/41b7a9582b8ebaf77413cfcbf8296967a336ad73/lambdas/model_trainning/Trainning.ipynb
2. Deploy infraestructure (`./infraestructure`) using `scripts/CI.sh -a`
3. Deploy applications (`.lambdas`) using `scripts/CD.sh -a`


## Usage
To deploy all the stack
```shell
bash scripts/up_infra.sh
```

To clean the stack
```shell
bash scripts/clean.sh
```


## Project Structure
```
.
├── docs
│   └── images
├── infraestructure
│   ├── evaluation_store_main.tf # Evaluation Store Infraestructure
│   ├── feature_store_dynamo.tf # Dynamo Feature Store Infraestructure
│   ├── Makefile # Logic to deploy infraestructure
│   ├── model_store_model.tf # Model Store Machine learning Model Infraestructure
│   ├── model_store_orchestrator.tf # Model Store Orchestrator Infraestructure
│   └── provider.tf # Provider configurations
├── lambdas
│   ├── model_orchestrator # Model Store Orchestrator lambda to serve it
│   └── model_trainning # Model Store Machine learning Model trainning procedure and lambda to serve it
├── README.md
└── scripts # scripts to handle to deploy and destroy infra
    ├── CD.sh
    ├── CI.sh
    ├── clean.sh
    ├── evaluation_store.sql
    ├── python
    └── up_infra.sh
```
## Proposed Architecture
The architecture is compounded of 4 elements: 
1. A DynamoDB acting as an in memory feature store;
2. A Lambda (model) serving the machine learning model trainned in https://github.com/RomuloSilvaRosa/addi_challenge/blob/41b7a9582b8ebaf77413cfcbf8296967a336ad73/lambdas/model_trainning/Trainning.ipynb
3. A Kinesis Firehose + S3 + Athena acting as an evaluation store;
4. A Lambda (orchestrator) acting as a glue between feature gathering, model prediction and logging data in evaluation store.

<img src="./docs/images/addi_diag.png" align="center"/>
<!-- <img align="left" width="0" height="192px" hspace="10"/> -->
