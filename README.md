# ReviewRating
## Deployment tools:  
Google Cloud Compute Engine
## Platform and environment: 
Flask==1.1.2

Other libraries version informations are in requirement.txt

## Deployment process
Cuz the Word2Vec files is larger than the limit of Github file size. 
**Word2Vec2.trainables.syn1neg.npy** and **Word2Vec2.wv.vectors.npy** are stored by using GIT LFS. And in deployment, these two files must upload by youtself under **"static/"**.

Files of model and Word2Vec
https://drive.google.com/drive/folders/158yUqcVOj35HQXOnF-zE9IrE971Pcv2I?usp=sharing

### Step1
Registered a Google Cloud Account and apply for a VM Instance under Compute Engine. Name it with your project name.

### Step2
Use SSH to connect instance and use **Git clone** commend in VM to clone this repository.

### Step3
Upload the model and Word2Vec by using gcloud commend or using ssh brower window. Upload the files under **"static/"**.

### Step4
Install the Project Dependencies by using the commend below.
```
pip3 install -r requirements.txt --user
```
```
export FLASK_APP=review_rating.py
flask run --host=0.0.0.0
```

### Setp5
Expose the Flask HTTP port (5000) from the VM’s firewall. This is done via gcloud tools in your local development environment.
```
gcloud compute firewall-rules create open-flask-rule --allow tcp:5000 --source-tags=flask-demo --source-ranges=0.0.0.0/0
```
Or you can set the firewall in yout Google Instance in the browser.