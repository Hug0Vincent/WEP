# WEP

## Description

Python implementation to brute force shared key authentication of the WEP protocol. 


## Usage



```
usage: rc4brute.py [-h] -i IV -p PASSWORD_FILE [-c CPU_COUNT] -r
                   RESPONSE_CHALLENGE -s SEND_CHALLENGE

optional arguments:
  -h, --help            show this help message and exit
  -i IV, --iv IV        iv of the trame
  -p PASSWORD_FILE, --password-file PASSWORD_FILE
                        input file
  -c CPU_COUNT, --cpu-count CPU_COUNT
                        number of core
  -r RESPONSE_CHALLENGE, --response-challenge RESPONSE_CHALLENGE
                        The response challenge
  -s SEND_CHALLENGE, --send-challenge SEND_CHALLENGE
                        The challenge send by the AP
                        
 ```
 
 ## Example 
 
--iv :   ```0xae39d6```

--send-challenge :   ```e4:77:8a...ff:5d```

--response-challenge :   ```e4:77:8a...ff:5d```

the **SEND_CHALLENGE** must be **128** bits long and the **RESPONSE_CHALLENGE** must be **136** bits long.
 
