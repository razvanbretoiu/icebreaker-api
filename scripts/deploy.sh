#!/bin/sh -ex

GCP_PROJECT=icebreaker-production
SERVICE=api
IMAGE=api

gcloud run deploy "$SERVICE" \
   --image gcr.io/"$GCP_PROJECT"/"$IMAGE" \
   --platform managed \
   --project "$GCP_PROJECT" \
   --region europe-west3 \
   --allow-unauthenticated
