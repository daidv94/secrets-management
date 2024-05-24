# AWS Secret manager management

Python core module with GPG(decrypted) which help to manage secrets in AWS secret manager

## Manage secrets on your development workstation

Please walkthrough in this [guide](./data/README.md) to learn how to use `eyaml` with GPG to encrypted/decrypted values

## Prerequisites

- AWS accounts
- [GnuPG](https://gnupg.org/download/index.html)
- Python3 installed

## Feature

- Decrypt encrypted gpg file to plain text
- From decrypted file, read it and sync to AWS account

## Get started

### Install dependencies

```bash
pip install -r requirements.txt
```

### Example usage

Create an `secrets.yaml` file like following sample

```yaml
workload:
  region: ap-southeast-1
  role_arn: arn:aws:iam::1239124113:role/secretmanager-role
  secrets:
  - name: dev/api/oauth-token
    status: active
    description: Oauth token
    value:
      - Key: token
        Value: c385bc594d0759865055d436f844a4c2
```

#### Inputs

| Name | Description | Type |
|------|-------------|------|
| `workload` | Identifier of aws account, could be whatever, just make sure its uniquie | `object` |
| `region` | AWS regions of secrets to be created in | `string` |
| `role_arn` | Role to be assumed by your AWS identity, this role need to have sufficient permission to AWS Secrets Manager resources | `string` |
| `secrets` | List of definitation secret object | `list` |
| `name` | AWS secret identifier | `string` |
| `status` | Must be `active` or `inactive`, whether secret to be created or deleted | `string` |
| `description` | AWS secret description | `string` |
| `value` |  List of `Key` and `Value` object, which value of secret | `list` |

#### Encrypt file

Example encrypt, change `recipient` flag argument to your desire

```bash
gpg -a --encrypt --output secrets.gpg --recipient your_colleage_name@gmail.com secrets.yaml
```

Now we have a `secrets.gpg` file which is the encrypted data of `secrets.yaml` file

#### Lets run it

Prepare AWS creds. It could be exported to environment varable or default aws cred files

Run python script

```bash
python3 src/main.py --encryptedfile secrets.yaml --gnupghome "/Users/daidao/.gnupg"
```

The `--gnupghome` flag can be ommited, default is `$HOME/.gnupg`

#### Verify result by aws cli or aws console

#### Clean up
  
- Remove `secrets.yaml` and `secrets.gpg` file

## Author

- Dai Dao

## License

Copyright © 2024
