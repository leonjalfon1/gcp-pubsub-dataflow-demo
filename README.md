# Pub/Sub & Dataflow Demo

In this demo we will see how to create a data pipeline using Pub/Sub and Dataflow

<kbd>
  <img src="/pubsub-dataflow.png" width="700">
</kbd>

## Required Steps

1. Configure your Environment
2. Create the Pub/Sub Topic and Subscription
3. Deploy the Publisher Application
4. Setup the Environment to work with Apache Beam and Dataflow
5. Run the Data Pipeline Locally
6. Run the Data Pipeline using Dataflow

## Prerequisites

- Docker
- Google Cloud Project (and enough permissions)
- Python Development Environment (https://cloud.google.com/python/setup/)
- Enable the Dataflow API (https://console.developers.google.com/apis/api/dataflow.googleapis.com/overview)

## Instructions

### 1) Configure your Environment

In this step we will configure the local environment to perform the demo

- Create a service account with "project owner" permissions (https://cloud.google.com/docs/authentication/getting-started#cloud-console)

- Rename the download file to "service-account.json" and copy it to the "nodejs-pubsub-publisher-app/gcp-credentials" directory (the file will be ignored by git to avoid security issues)

- Create a environment variable that point to the repository root path
```
export REPOSITORY_ROOT_PATH="$(pwd)"
```
```
echo $REPOSITORY_ROOT_PATH
```

- Create a environment variable that point to the "service-account.json" file:
```
export GOOGLE_APPLICATION_CREDENTIALS="$REPOSITORY_ROOT_PATH/gcp-credentials/service-account.json"
```
```
echo $GOOGLE_APPLICATION_CREDENTIALS
```

- Create a environment variable with your GCP project Id
```
export GOOGLE_PROJECT_NAME="your-project-name"
```
```
echo $GOOGLE_PROJECT_NAME
```

- Create a environment variable with your GCP service account name (you can see it's name in the retrieved json file)
```
export GOOGLE_SERVICE_ACCOUNT_EMAIL="your-account-name@your-project-name.iam.gserviceaccount.com"
```
```
echo $GOOGLE_SERVICE_ACCOUNT_EMAIL
```

### 2) Create the Pub/Sub Topic and Subscription

In this step we will create the Pub/Sub topic and the subscription that we will use during the demo

- Create a Pub/Sub Topic called demo-topic (you can create it using the command below, from the console or using your local gcloud CLI)
```
docker run --rm -it -v $REPOSITORY_ROOT_PATH/gcp-credentials/service-account.json:/key/service-account.json google/cloud-sdk:latest bash -c "gcloud auth activate-service-account $(echo $GOOGLE_SERVICE_ACCOUNT_EMAIL) --key-file=/key/service-account.json; gcloud config set project $(echo $GOOGLE_PROJECT_NAME); gcloud pubsub topics create demo-topic"
```

- Create a Pub/Sub Subscription called demo-subscription (you can create it using the command below, from the console or using your local gcloud CLI)
```
docker run --rm -it -v $REPOSITORY_ROOT_PATH/gcp-credentials/service-account.json:/key/service-account.json google/cloud-sdk:latest bash -c "gcloud auth activate-service-account $(echo $GOOGLE_SERVICE_ACCOUNT_EMAIL) --key-file=/key/service-account.json; gcloud config set project $(echo $GOOGLE_PROJECT_NAME); gcloud pubsub subscriptions create demo-subscription --topic demo-topic"
```

### 3) Deploy the Publisher Application

In this step we will deploy the application to publish messages into our demo-topic

- Build the application image

```
cd $REPOSITORY_ROOT_PATH/nodejs-pubsub-publisher-app
docker build -t nodejs-pubsub-publisher-app:latest .
```

- Run the application image locally (note that the service-account.json is mounted as volume as some environment variables are set)
```
docker run -d -p 3000:3000 -e GOOGLE_PROJECT_NAME=$GOOGLE_PROJECT_NAME -e GOOGLE_TOPIC_NAME=demo-topic -v $REPOSITORY_ROOT_PATH/gcp-credentials:/key nodejs-pubsub-publisher-app:latest
```

- Browse to the application to publish a new message to the topic (a new message will be published for each request)
```
http://localhost:3000/publish
```

### 4) Setup the Environment to work with Apache Beam and Dataflow

In this step we will setup the local environment to work with Dataflow

- Move to the Dataflow project directory

```
cd $REPOSITORY_ROOT_PATH/data-pipelines
```

- Create a environment variable that point to the region you want to use for Dataflow
```
export DATAFLOW_REGION="europe-west1"
```
```
echo $DATAFLOW_REGION
```

- We need to create a Cloud Storage Bucket for Dataflow, save its name in a environment variable:

```
export BUCKET_NAME="your-bucket-name"
```
```
echo $BUCKET_NAME
```

- Create the bucket (you can create it using the command below, from the console or using your local gcloud CLI)
```
docker run --rm -it -v $REPOSITORY_ROOT_PATH/gcp-credentials/service-account.json:/key/service-account.json google/cloud-sdk:latest bash -c "gcloud auth activate-service-account $(echo $GOOGLE_SERVICE_ACCOUNT_EMAIL) --key-file=/key/service-account.json; gcloud config set project $(echo $GOOGLE_PROJECT_NAME); gsutil mb gs://$BUCKET_NAME"
```

- Ensure that you have a working Python and pip installation by running:

```
python --version
python -m pip --version
```

- Setup and activate a Python virtual environment:

```
sudo -H pip install virtualenv
virtualenv env
source env/bin/activate
```

- Install the latest version of the Apache Beam SDK for Python by running:

```
pip install apache-beam[gcp]
```

### 5) Run the Batch Data Pipeline Locally

- In this section we will run the wordcount batch data pipeline (locally) that performs the following steps:

  1. Takes a text file as input.
  2. Parses each line into words.
  3. Performs a frequency count on the tokenized words.

- Run the wordcount.py pipeline on your local machine with the following command:

```
python wordcount-batch.py --output outputs
```

- To view the outputs, run the following command:

```
more outputs*
```

- Executing your pipeline locally allows you to test and debug your Apache Beam program


### 6) Run a Batch Data Pipeline using Dataflow

- You can run the wordcount pipeline on the Dataflow service by specifying DataflowRunner in the runner field and selecting a region where the pipeline will execute:

```
python wordcount-batch.py \
  --region $DATAFLOW_REGION \
  --input gs://dataflow-samples/shakespeare/kinglear.txt \
  --output gs://$BUCKET_NAME/wordcount/results/outputs \
  --runner DataflowRunner \
  --project $GOOGLE_PROJECT_NAME \
  --temp_location gs://$BUCKET_NAME/wordcount/tmp
```

- To track and inspect the data pipeline browse to Dataflow:

```
https://console.cloud.google.com/dataflow
```

- To view your results browse to Cloud Storage:

```
https://console.cloud.google.com/storage/browser
```

### 7) Configure a Pub/Sub Streaming Data pipeline with Dataflow

- To configure the streaming data pipeline run:

```
python pubsub-streaming.py \
  --project=$GOOGLE_PROJECT_NAME \
  --region $DATAFLOW_REGION \
  --input_topic=projects/$GOOGLE_PROJECT_NAME/topics/demo-topic \
  --output_path=gs://$BUCKET_NAME/pubsub/results/output \
  --runner=DataflowRunner \
  --window_size=2 \
  --temp_location=gs://$BUCKET_NAME/pubsub/tmp
```

- After the job has been submitted, you can check its status in the GCP Console Dataflow page:

```
https://console.cloud.google.com/dataflow
```

- You can also check the output in your Cloud Storage Bucket:

```
https://console.cloud.google.com/storage/browser
```

- Generate load (from another terminal session)

```
for n in {1..250}; do curl http://localhost:3000/publish; done
```

- Ctrl+C to stop the program in your terminal. Note that this does not actually stop the job if you use DataflowRunner


## Cleanup

- Stop the Dataflow job in GCP Console Dataflow page. Cancel the job instead of draining it. This may take some minutes

```
export DATAFLOW_JOB_ID="check-the-job-id-in-dataflow-console"
```
```
docker run --rm -it -v $REPOSITORY_ROOT_PATH/gcp-credentials/service-account.json:/key/service-account.json google/cloud-sdk:latest bash -c "gcloud auth activate-service-account $(echo $GOOGLE_SERVICE_ACCOUNT_EMAIL) --key-file=/key/service-account.json; gcloud config set project $(echo $GOOGLE_PROJECT_NAME); gcloud dataflow jobs cancel $DATAFLOW_JOB_ID --region=$DATAFLOW_REGION"
```

- Delete the Pub/Sub topic

```
gcloud pubsub topics delete cron-topic

docker run --rm -it -v $REPOSITORY_ROOT_PATH/gcp-credentials/service-account.json:/key/service-account.json google/cloud-sdk:latest bash -c "gcloud auth activate-service-account $(echo $GOOGLE_SERVICE_ACCOUNT_EMAIL) --key-file=/key/service-account.json; gcloud config set project $(echo $GOOGLE_PROJECT_NAME); gcloud pubsub topics delete demo-topic"
```

- Delete the Cloud Storage Bucket

```
docker run --rm -it -v $REPOSITORY_ROOT_PATH/gcp-credentials/service-account.json:/key/service-account.json google/cloud-sdk:latest bash -c "gcloud auth activate-service-account $(echo $GOOGLE_SERVICE_ACCOUNT_EMAIL) --key-file=/key/service-account.json; gcloud config set project $(echo $GOOGLE_PROJECT_NAME); gsutil rb gs://$BUCKET_NAME"
```
