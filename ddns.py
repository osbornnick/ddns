import requests
from datetime import datetime
import configparser
# TODO: take config details out of code
# add logging capabilites
# put on a cronjob


def main():
    log = open('run.log', 'a')
    starttime = datetime.now()
    log.write(f'run started {starttime.strftime("%c")}')
    current_ip = get_current_ip()
    log.write(f'retrieved current ip: {current_ip}')
    response = api_dns_call('get')
    listed_ip = response.json()['domain_record']['data']
    log.write(f'retrieved listed ip: {listed_ip}')
    if current_ip != listed_ip:
        log.write('DNS needs to be updated, updating')
        api_dns_call('put', current_ip)
        log.write(f'DNS updated to {current_ip}')
    else:
        log.write('current ip and listed ip match')
    finishtime = datetime.now()
    runtime = finishtime - starttime
    secs = runtime.total_seconds()
    log.write(f'run finished at {finishtime}, {secs} seconds runtime \n')


def get_current_ip():
    ip_request = requests.get('https://api.ipify.org?format=json')
    current_ip = ip_request.json()['ip']
    return current_ip


def api_dns_call(type, ip='0.0.0.0', id='91341316'):
    config = configparser.ConfigParser()
    config.read('config.ini')
    apiurl = config['api']['url']
    token = config['api']['token']
    headers = {"Authorization": f'Bearer {token}'}
    if type == 'get':
        return requests.get(apiurl + id, headers=headers)
    elif type == 'put':
        if ip == '0.0.0.0':
            raise ValueError("Choose new ip value for A record.")
        else:
            data = {'data': 'ip'}
            return requests.put(apiurl + id, headers=headers, data=data)
    else:
        return ValueError("type must be 'get' or 'put'.")


if __name__ == '__main__':
    main()
