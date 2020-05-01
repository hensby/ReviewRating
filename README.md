# ReviewRating
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/Django)
![PyPI](https://img.shields.io/pypi/v/pip)
![](https://img.shields.io/badge/flask-1.1.2-brightgreen)
![](https://img.shields.io/badge/ubuntu-18.0.4-orange)
![](https://img.shields.io/badge/Google%20Cloud-Compute%20Engine-red)
## Deployment tools:  
Google Cloud Compute Engine
## Platform and environment: 
Flask==1.1.2, 
python==3.7

Other libraries version informations are in requirement.txt

## Deployment process
*(Hint)*
Cuz the Word2Vec files is larger than the limit of Github file size. 
**Word2Vec2.trainables.syn1neg.npy** and **Word2Vec2.wv.vectors.npy** are stored by using GIT LFS. And in deployment, these two files must upload by youtself under **"static/"**.

Files of model and Word2Vec language model: 

https://drive.google.com/drive/folders/158yUqcVOj35HQXOnF-zE9IrE971Pcv2I?usp=sharing

### Step1
Registered a Google Cloud Account and apply for a VM Instance under Compute Engine. Name it with your project name. Remember the **external IP address** so that you can connect your VM by uaing SSH client. 

### Step2
Use SSH client to connect instance and use **Git clone** commend in VM terminal to clone this repository into your VM.
```
git clone https://github.com/hensby/ReviewRating.git
```

### Step3
Upload the model and Word2Vec by using gcloud commend or using ssh brower window. Upload the files under **"static/"** direction. The command is shown below:
```
gcloud compute scp local-file-path instance-name:~
```

### Step4
Install the Project Dependencies in **requirements.txt** by using the commend below.
```
pip3 install -r requirements.txt --user
```

### Step5
Deploy the flask APP by using command below: I set the host as 0.0.0.0. It's easy to set the firewall rules.
```
export FLASK_APP=review_rating.py
flask run --host=0.0.0.0
```

### Setp6
Expose the Flask HTTP port (5000) from the VM’s firewall. This is done via gcloud tools in your local development environment.
```
gcloud compute firewall-rules create open-flask-rule --allow tcp:5000 --source-tags=flask-demo --source-ranges=0.0.0.0/0
```
Or you can set the firewall in yout Google Instance in the browser.