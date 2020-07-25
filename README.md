# ssh-home
Record dynamic public ip and use the record value to make SSH connection or transfer
- `ip_record`
- `home_connect`
- `home_rsync`


## Version 0.3.0
- Add `home_rsync` feature
- Add `version` option to show version information
- Change ip record method to record if only ip has change 

#### Version 0.2.2
- Add `setup` options
    - `home-connect`: Setup home-connect feature
    - `ip-record`: Setup ip-record feature
    - `all`: Setup all feature

#### Version 0.2.1 (hotfix)
- Fix missing google credential SCOPES definition 

#### Version 0.2.0
- Add `home-connect` feature (autoconnect)
- multiple ssh connect sections configuration

#### Version 0.1.0

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
SSH connection configuration
```
[CONNECTION_NAME_SSH]
ssh-user: ssh login user
ssh-port: ssh login port
ssh-key-path: secret key for ssh login
```

RSYNC connection configuration
```
[CONNECTION_NAME_RSYNC]
rsync-user = rsync user
rsync-dest = rsync destination (/destination/path)
rsync-source = rsync source
rsync-options = rsync options (-a --exclude) 
rsync-port = rsync login port
rsync-key-path = rsync login key path
# Optional setting
connection-ip = Set connection ip address manully (Optional)
```

**`setup.sh`** file  
Setup environment
```
./setup.sh home-connect|home-rsync|ip-record|all DESTINATION

    home-connect            Setup for home-connect function
    home-rsync              Setup for home-rsync function
    ip-record               Setup for ip-record function
    all                     Setup for all functions
```

## Usage

#### ip_record
Run this program to find your current public ip address and documented it to Google spreadsheet
```
usage: ip_record.py [-h] [-V]

optional arguments:
  -h, --help     show this help message and exit
  -V, --version  show program's version number and exit
```
#### home_connect
Run this program to ssh connect to `ip_record` lastest ip address
```
usage: home_connect.py [-h] [-V] connection

positional arguments:
  connection     Section name set in configuration file - config.ini

optional arguments:
  -h, --help     show this help message and exit
  -V, --version  show program's version number and exit
``` 
#### home_rsync
Run this program to perform rsync to destination of `ip_record` latest ip address
```
usage: home_rsync.py [-h] [-V] connection

positional arguments:
  connection     Section name set in configuration file - config.ini

optional arguments:
  -h, --help     show this help message and exit
  -V, --version  show program's version number and exit
```

## Error Code
`1` - program usage error  
`3` - template sheet not found    
`5` - target sheet not found  
`11` - conf_mod ConfigNotFoundError  
`12` - conf_mod NoSectionError  
`13` - conf_mod NoOptionError  
`14` - conf_mod OptionFormatError