#!/bin/sh -ex
GCP_PROJECT=icebreaker-production

gcloud builds submit --tag gcr.io/"$GCP_PROJECT"/api --project "$GCP_PROJECT"
