import json
import urllib
import sys
import os
from time import sleep


def getSSL(config: dict) -> dict:
    req = urllib.request.Request(
        config["endpoint"] + '/ssl/retrieve/' + config["domain"])
    req.data = json.dumps(config).encode('utf8')
    response = urllib.request.urlopen(req).read()

    allRecords = json.loads(response.decode('utf-8'))

    if allRecords["status"] != "SUCCESS":
        sys.stderr.write('Error retrieving SSL Certs!')
        sys.stderr.write(allRecords["message"])
        sys.exit(1)

    return (allRecords)


def main():
    apiConfig = {
        "endpoint": "https://porkbun.com/api/json/v3",
        "apikey": os.getenv('API_KEY', 'NOT-SET'),
        "secretapikey": os.getenv('SECRET_API_KEY', 'NOT-SET'),
        "domain": os.getenv('DOMAIN', 'NOT-SET'),
        "domainCertLocation": "/etc/ssl/cert.pem",
        "privateKeyLocation": "/etc/ssl/key.pem",
        "intermediateCertLocation": "/etc/ssl/intermediate-cert.pem",
        "publicKeyLocation": "/etc/ssl/key.pub",
    }

    sleep_time = os.getenv('SLEEP', 24)

    while True:
        print("Downloading certs for " + apiConfig["domain"])
        certJSON = getSSL(apiConfig)

        with open(apiConfig["domainCertLocation"], "w") as f:
            print("Installing " + apiConfig["domainCertLocation"])
            f.write(certJSON["certificatechain"])
            f.close()

        with open(apiConfig["privateKeyLocation"], "w") as f:
            print("Installing " + apiConfig["privateKeyLocation"])
            f.write(certJSON["privatekey"])
            f.close()

        with open(apiConfig["publicKeyLocation"], "w") as f:
            print("Installing " + apiConfig["publicKeyLocation"])
            f.write(certJSON["publickey"])
            f.close()

        with open(apiConfig["intermediateCertLocation"], "w") as f:
            print("Installing " + apiConfig["intermediateCertLocation"])
            f.write(certJSON["intermediatecertificate"])
            f.close()

        print("Sleeping {} h".format(sleep_time))
        sleep(sleep_time*60*60)


if __name__ == "__main__":
    main()
