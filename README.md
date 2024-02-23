# ddchimp
Multi-Cloud Dynamic DNS

# .config.json sample 
```
{
     "system": {
        "check_timeout" : 300
    },
    "aws": {
        "aws_access_key": "ABCDE",
        "aws_secret_key": "QWERTY",
        "aws_r53_zone_id": "Z0121231",
        "aws_r53_name": "sub.example.com"
    },
    "cflr": {
        "cflr_email_address": "email@example.com,
        "cflr_api_key": "SECRET_KEY",
        "cflr_zone_id": "524cb4zoneid",
        "cflr_fqdn_name": "sub.example.tld"
    }
}
```
# Docker Repo
Docker Image can be pulled from this [Docker repository](https://hub.docker.com/r/puffago/ddchimp)