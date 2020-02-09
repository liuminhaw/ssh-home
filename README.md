# ip-record
Record dynamic ip address to Google sheet

## Version 0.1.0

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

**`setup.sh`** file  
Setup environment
```
./setup.sh DESTINATION_DIRECTORY
```

## Usage
Run this program to find your current public ip address and document it to Google spreadsheet
```
python3 ip_record.py
```

## Error Code
`3` - template sheet not found  
`11` - conf_mod ConfigNotFoundError  
`12` - conf_mod NoSectionError  
`13` - conf_mod NoOptionError  