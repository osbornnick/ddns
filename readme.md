# A simple dynamic DNS tool written in python.

Communicates with DigitalOcean API to retrieve DNS A records, tests if they are up-to-date with the servers reported ip (gotten by pinging ipify), if not, updates the DigitalOcean record.

Uses requests, datetime, and configparser
