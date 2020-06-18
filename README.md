# Pub/Sub & Dataflow Demo

In this demo we will ...

## Required Steps
---

1. Configure your Environment
2. Create the Pub/Sub Topic and Subscription
3. Deploy the Publisher App
4. 
5. 

## Prerequisites
---

- Docker
- Google Cloud Project (and enough permissions)

## Instructions
---

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

- Create a environment variable with your GCP project Id
```
export GOOGLE_PROJECT_ID="your-project-name"
```
```
echo $GOOGLE_PROJECT_ID
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

- Create a Pub/Sub Topic called demo-topic (you can create it using the command below, from the console or using you local gcloud CLI)
```
docker run --rm -it -v $REPOSITORY_ROOT_PATH/gcp-credentials/service-account.json:/key/service-account.json google/cloud-sdk:latest bash -c "gcloud auth activate-service-account $(echo $GOOGLE_SERVICE_ACCOUNT_EMAIL) --key-file=/key/service-account.json; gcloud config set project $(echo $GOOGLE_PROJECT_ID); gcloud pubsub topics create demo-topic"
```

- Create a Pub/Sub Subscription called demo-subscription (you can create it using the command below, from the console or using you local gcloud CLI)
```
docker run --rm -it -v $REPOSITORY_ROOT_PATH/gcp-credentials/service-account.json:/key/service-account.json google/cloud-sdk:latest bash -c "gcloud auth activate-service-account $(echo $GOOGLE_SERVICE_ACCOUNT_EMAIL) --key-file=/key/service-account.json; gcloud config set project $(echo $GOOGLE_PROJECT_ID); gcloud pubsub subscriptions create demo-subscription --topic demo-topic"
```

### 3) Deploy the Publisher App

In this step we will deploy the application to publish messages into our demo-topic

- Build the application image

```
cd $REPOSITORY_ROOT_PATH/nodejs-pubsub-publisher-app
docker build -t nodejs-pubsub-publisher-app:latest .
```

- Run the application image locally (note that the service-account.json is mounted as volume as some environment variables are set)
```
docker run -d -p 3000:3000 -e GOOGLE_PROJECT_ID=$GOOGLE_PROJECT_ID -e GOOGLE_TOPIC_NAME=demo-topic -v $REPOSITORY_ROOT_PATH/gcp-credentials:/key nodejs-pubsub-publisher-app:latest
```

- Browse to the application to publish a new message to the topic (a new message will be published for each request)
```
http://localhost:3000/publish
```

### 4)

In this step we will ...

### 5)

In this step we will ...


## Cleanup
---

- Delete the Pub/Sub topic
