# ssh-home
Record dynamic public ip and use the record value to make SSH connection
- `ip_record`
- `home_connect`

## Version 0.2.1
- Fix missing google credential SCOPES definition 

### Version 0.2.0
- Add `home-connect` feature (autoconnect)
- multiple ssh connect sections configuration

### Version 0.1.0

## Additional Requirements
- GCP
    - Sheet API enabled
    - generate OAuth key: `credential.json`
    - Accept this program to read and edit spreadsheet
- Copy Google spreadsheet from template: [template spreadsheet](https://drive.google.com/open?id=1OBP1rr7CIUe1pXZ672gzklkFGRCnbZM2hYVeiE76W80)

## Preparation
**`config.ini`** file  
Program configuration
```
sheet-id: Set sheet id to read
credential-file: [Optional]
template-sheet: [Optional]
```
Connection configuration
```
[CONNECTION_NAME]
ssh-user: ssh login user
ssh-port: ssh login port
ssh-key-path: secret key for ssh login
```

**`setup.sh`** file  
Setup environment
```
./setup.sh DESTINATION_DIRECTORY
```

## Usage

#### ip_record
Run this program to find your current public ip address and document it to Google spreadsheet
```
python3 ip_record.py
```
#### home_connect
Run this program to ssh connect to `ip_record` lastest ip address
```
python3 home_connect.py CONNECT_NAME
``` 
- `CONNECT_NAME`: Section name set in `config.ini` file

## Error Code
`1` - program usage error
`3` - template sheet not found  
`5` - target sheet not found
`11` - conf_mod ConfigNotFoundError  
`12` - conf_mod NoSectionError  
`13` - conf_mod NoOptionError  