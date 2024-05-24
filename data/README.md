# AWS Secrets encryption/decryption with  Eyaml - GnuPG

Scripts and data repository for managing aws secrets data

## Prerequisites

- [GnuPG](https://gnupg.org/download/index.html) installed

### MAC-OS installation

Install gpg

```bash
brew install gpg
```

Install hiera-eyaml gpg

```bash
brew install ruby
```

Add these paths into `PATH` environment variable

```text
/opt/homebrew/lib/ruby/gems/3.3.0/bin
/opt/homebrew/opt/ruby/bin
```

Run update gem system

```bash
sudo gem update --system
```

Install mandatory gems

```bash
sudo gem install gpgme hiera-eyaml hiera-eyaml-gpg ruby_gpg
```

### Ubuntu / Debian install

Install gpg

```bash
sudo apt-get update -y
sudo apt-get -y install gpg
```

Install hiera-eyaml

```bash
sudo apt-get -y install build-essential ruby rubygems ruby-dev
```

Install hiera-gpg with gem

```bash
sudo gem install gpgme hiera-eyaml hiera-eyaml-gpg ruby_gpg
```

## Feature

- Encrypt sensitive data by eyaml backend gpg
- Decrypt data with your private gpg key

## Get started

Verify if your gpg is working

```bash
gpg --version
```

### Generate your gpg key

Run the below command

```bash
gpg --full-generate-key
```

Finish the prompt to generate gpg key. Verify the key ring

```bash
gpg -k
```

It should output the information like below. The `ultimate` mean its your key

```text
/Users/daidao/.gnupg/pubring.kbx
---------------------------------
pub   rsa3072 2024-05-24 [SC]
      7987AA6BF4E1EE4BFB27B302930F90DAFA994FF1
uid           [ultimate] Dai Dao (Personal GPG key) <daovandai94@gmail.com>
sub   rsa3072 2024-05-24 [E]
```

### Export public key

```bash
gpg --output your_name.gpg --armor --export your_email@email
```

### Upload it into member folder then create PR to main

#### Others member of keyring have to do the following

Import new member public key

```bash
gpg --import your_name.gpg
```

Sign the key

```bash
gpg --sign-key your_email@email
```

Alternative, key_id/thumbprint could be used instead of email

#### After that, the keyrings should be up to date with all member public key

Import and sign all key in keyring

```bash
./gpg-keys/sign_key.sh ./gpg-keys/keyrings/all.gpg
```

### After importing and signing, your key ring should have your member key

### Decrypt secrets file

```bash
eyaml decrypt -n gpg -f secrets.yaml
```

### Encrypts data, edit file

```bash
eyaml edit secrets.yaml --gpg-recipients-file recipients
```

Encrypt the value you wish to be encrypted by adding following pattern `DEC::GPG[sensitive_data]!`

## Author

- Dai Dao

## License

Copyright © 2024
