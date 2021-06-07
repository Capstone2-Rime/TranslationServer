# TranslationServer
</hr>

## Installation

### Google STT API

```
  echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list 
  sudo apt-get install apt-transport-https ca-certificates gnupg
  curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -

  sudo apt-get update && sudo apt-get install google-cloud-sdk

  sudo apt-get install google-cloud-sdk-app-engine-python

  sudo apt-get install google-cloud-sdk-app-engine-python-extras

  python3 -m pip install --upgrade google-cloud-speech

  export GOOGLE_APPLICATION_CREDENTIALS="YOUR GOOGLE CLOUD JSON KEY PATH"
```

### Text Processing

```
  pip install hgtk
```

```
  pip install textdistance
```
You sholud install library in https://github.com/Capstone2-Rime/Dataset<br>
***Set your path in makeSttDataset.py***


### Maria DB

```
  pip install pymysql
```

***you should make your database and set account in connect.py***
## Start

```
  python3 audio2captionServer.py
```
