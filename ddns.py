import requests
from datetime import datetime
import configparser
# TODO:
# put on a cronjob


def main():
    starttime = datetime.now()
    print(f'run started {starttime.strftime("%c")}')
    current_ip = get_current_ip()
    print(f'retrieved current ip: {current_ip}')
    response = api_dns_call('get')
    listed_ip = response.json()['domain_record']['data']
    print(f'retrieved listed ip: {listed_ip}')
    if current_ip != listed_ip:
        print('DNS needs to be updated, updating')
        api_dns_call('put', current_ip)
        print(f'DNS updated to {current_ip}')
    else:
        print('current ip and listed ip match')
    finishtime = datetime.now()
    runtime = finishtime - starttime
    secs = runtime.total_seconds()
    print(f'run finished at {finishtime}, {secs} seconds runtime')


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
