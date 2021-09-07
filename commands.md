ssh -i "~/DeepCite.pem" ec2-user@ec2-18-217-10-151.us-east-2.compute.amazonaws.com

ps ax|grep gunicorn
pkill gunicorn

python3 -m venv v-env

scp -i "~/DeepCite.pem" -r /mnt/c/Users/conno/Documents/GitHub/DeepCite/backend/model/v-env-test/lib64/python3.7/site-packages/en_core_web_lg/ ec2-user@ec2-18-222-119-231.us-east-2.compute.amazonaws.com:
sudo mv /usr/local/lib/python3.7/site-packages/en_core_web_lg /mnt/efs/fs1/

docker build -t deepcite_model .
PORT=8080 && docker run -p 9090:${PORT} -e PORT=${PORT} deepcite_model:latest

gcloud sql connect deepcite --user=postgres

https://chrome.google.com/webstore/devconsole/48556bdc-768a-4c11-9f1c-d7a96bf9737f?hl=en

format json
shift+alt+f

# update chrome extension
rm deepcite_extension.zip
zip -r deepcite_extension.zip extension

# update cloud functions code
cd backend/lambda/
rm function.zip
zip -g function.zip main.py create_response.py lambda_config.py database_calls.py defaults.json requirements.txt
gsutil cp function.zip gs://deepcite-function
gcloud functions deploy deepcite --source=gs://deepcite-function/function.zip

# update cloud run code
gcloud builds submit --tag gcr.io/deepcite-306405/deepcite-model
gcloud run deploy deepcite-model --image gcr.io/deepcite-306405/deepcite-model:latest --platform managed --region us-central1