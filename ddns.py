import requests
from datetime import datetime
import configparser
# TODO:
# put on a cronjob


def main():
    log = open('run.log', 'a')
    starttime = datetime.now()
    log.write(f'run started {starttime.strftime("%c")}\n')
    current_ip = get_current_ip()
    log.write(f'retrieved current ip: {current_ip}\n')
    response = api_dns_call('get')
    listed_ip = response.json()['domain_record']['data']
    log.write(f'retrieved listed ip: {listed_ip}\n')
    if current_ip != listed_ip:
        log.write('DNS needs to be updated, updating\n')
        api_dns_call('put', current_ip)
        log.write(f'DNS updated to {current_ip}\n')
    else:
        log.write('current ip and listed ip match\n')
    finishtime = datetime.now()
    runtime = finishtime - starttime
    secs = runtime.total_seconds()
    log.write(f'run finished at {finishtime}, {secs} seconds runtime \n\n')


def get_current_ip():
    ip_request = requests.get('https://api.ipify.org?format=json')
    current_ip = ip_request.json()['ip']
    return current_ip


def api_dns_call(type, ip='0.0.0.0', id='91341316'):
    config = configparser.ConfigParser()
    config.read('api.ini')
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
