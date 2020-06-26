# DeepCite

<p> Google Chrome extension that finds the source of a claim using BeautifulSoup, spaCy, and gensim libraries. Please look at documentation for implemenation details. :trollface:</p>

## Table of Contents

* [Contributions](#contributions)
* [Setup](#setup)
* [Installation](#installation)
* [Testing](#testing)
* [Configuration](#configuration)
* [Authors](#authors)

## Contributions

Unfortunatly running code on AWS is not cheap and I would really appreciate any support you could give to see this project flourish.

| website               | payment address                    |
|-----------------------|------------------------------------|
| Bitcoin               | 361Dq2e5wnjAhCnQ8FEkeiK3CYZZJ9QuGs |
| Venmo                 | @fippy24                           |
| Paypal and Sofi Money | connor.trumpet@gmail.com           |

## Setup

#### Chrome

1. Install Google Chrome
2. In Chrome, navigate to `chrome://extensions/`
3. Enable developer mode
4. Then click `Load unpacked` 
5. Select DeepCite/extension folder

#### Firefox

1. Install Firefox
2. Navigate to `about:debugging`
3. Then select `This FireFox`
4. Next click on the button `Load Temporary Add-on...`
5. Select `DeepCite/extension/manifest.json`

Once installed you can use DeepCite by clicking on the on the icon in the top right of the browser. There you can enter a link or claim and click `Cite` to run DeepCite. You can also populate the claim input by highlighting text, then right clicking and selecting _"Populate claim"_. Similiarly you can populate the link input with _"Populate link"_. 

## Installation for Server
Installations and downloads required before server can funciton properly

### Downloads
  * Google News vector space.
  	* Google's word2vec can be found here https://code.google.com/archive/p/word2vec/ but you can no longer install the source code from here.
  	* If you want to just download the Pre-trained models [recommended] then you can download it from this [google drive link](https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit) then extract it.
  	* You can also find this link from the [archive page](https://code.google.com/archive/p/word2vec/) mentioned above.
  	* Once you have your model you'll need to first create the directory `./DeepCite/backend/word_vectors` then you can copy or move the model into that folder.
  	* Note: the backend expects a specific file name so you may need to rename the file. The end result should look like this `./DeepCite/backend/word_vectors/GoogleNews-vectors-negative300.bin`
  * Chrome driver https://sites.google.com/a/chromium.org/chromedriver/home -- in DeepCite/backend, check compatibility 

<small>n Note: 'en_core_web_sm' installation is testing purposes. It has lower accurary compared to the word google vectors </small>


## Testing

### Frontend Testing
* Download and install node.js from <a href="https://nodejs.org/en/"> their website </a>
* For the following commands navigate to DeepCite/extension folder
  * Use command `npm install mocha` to install testing framework
  * Use command `npm test` to run tests


* DeepCite/test-folder contains a basic web server meant for testing frontend functionality before we connect the frontend and backend together.
  * Follow the readme in that folder for its instructions

### System Testing
* To run a local server testing bash shell script:
* python -m spacy download en_core_web_sm
* run `pip install coverage`
* In DeepCite/backend, run run_tests.sh 

<small>Note: connection issues make occur when webscrapping, wait a minute then run again</small>

## Future Features
* Video transcription
* More Robust Webscrapping

## Curl request for testing
Run `gunicorn -c gunicorn_config.py wsgi` in Deepcite/backend

* Local testing:
`curl -d '{"claim":"the death of Sherlock Holmes almost destroyed the magazine that had originally published the stories. When Arthur Conan Doyle killed him off in 1893, 20,000 people cancelled their subscriptions. The magazine barely survived. Its staff referred to Holmes’ death as “the dreadful event”.", "link":"http://www.bbc.com/culture/story/20160106-how-sherlock-holmes-changed-the-world"}' -H "Content-Type: application/json" -X POST http://127.0.0.1:8000/api/v1/deep_cite`
* Server Testing:
`curl -d '{"claim":"the death of Sherlock Holmes almost destroyed the magazine that had originally published the stories. When Arthur Conan Doyle killed him off in 1893, 20,000 people cancelled their subscriptions. The magazine barely survived. Its staff referred to Holmes’ death as “the dreadful event”.", "link":"http://www.bbc.com/culture/story/20160106-how-sherlock-holmes-changed-the-world"}' -X POST https://jzvkkf7p6d.execute-api.us-east-2.amazonaws.com/dev/deepcite`

## Reporting Bugs

If you happen upon any bugs please feel free to submit an official issue. When submitting bugs please try to follow these guidlines:

```
### Issue description: 

...

### Steps to reproduce:

...

### Expected result:

...

### Actual result:

...

### Details:

 * Browser version:
 * OS:
 * ( any additional relevant information and/or screenshots )
```

## Configuration

There are a couple ways to configure both the backend and the aws lambda service. The first priority, or the first place the config will look is in the root folder for a json file named `deep-cite-config.json`. Next the config will look in the environment, and finally anything not found in the json config or environment will fallback to the defaults. Here are the defaults and config options:

 * As a JSON `./DeepCite/deep-cite-config.json`:

 ```json
 {
  "backend": {
    "env": "development",
    "language": "en",
    "gn_path": "./DeepCite/backend/word_vectors/GoogleNews-vectors-negative300.bin",
    "server": {
      "host": "0.0.0.0",
      "port": "5000" 
    },
    "gunicorn": {
      "host": "0.0.0.0",
      "port": "8000" ,
      "workers": "1",
      "timeout": "180"
    }
  },
  "aws": {
    "env": "development",
    "versions": {
      "model": "0.1",
      "lambda": "0.1",
      "api": "0.1",
      "extension": "0.1"
    },
    "db": {
      "rds": "deepcite.ckbyp3nhsmiu.us-east-2.rds.amazonaws.com",
      "name": "postgres",
      "port": "5432",
      "username": "postgres",
      "password": "deepcite"
    },
    "ec2": {
      "ip": "172.31.35.42",
      "port": "8000",
      "url": "http://172.31.35.42:8000/api/v1/deep_cite"
    }
  }
}
 ```

 * As an `.env`:

 ```bash
 ENV=development
 LANGUAGE=en
 GN_PATH=./DeepCite/backend/word_vectors/GoogleNews-vectors-negative300.bin
 SERVER_HOST=0.0.0.0
 SERVER_PORT=5000
 GUNICORN_HOST=0.0.0.0
 GUNICORN_PORT=8000
 GUNICORN_WORKERS=1
 GUNICORN_TIMEOUT=180
 EC2_IP=172.31.35.42
 EC2_PORT=8000
 DB_RDS=deepcite.ckbyp3nhsmiu.us-east-2.rds.amazonaws.com
 DB_NAME=postgres
 DB_PORT=5432
 DB_USERNAME=postgres
 DB_PASSWORD=deepcite
 VERSIONS_MODEL=0.1
 VERSIONS_LAMBDA=0.1
 VERSIONS_API=0.1
 VERSIONS_EXTENSION=0.1
 ```

## Authors
Connor O'Leary

With great help from the University of Wisconsin, Madison CS506 team
Shourya Goel, Jiayi Hu, Vinay Janardhanam, Dillon O'Leary, Noah SickLick, and Catherine Yan
