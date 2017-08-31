import urllib.request, urllib.parse
import string
import json

def get_ip_from_host(hostname, max_count = 5, cur_count = 0):
    if hostname[-1] == '.':
        hostname = hostname[:-1]
    if '.' in hostname and hostname.split('.')[-1][0] in string.ascii_letters and cur_count < max_count:
        resp = urllib.request.urlopen('https://dns.google.com/resolve?name='+hostname)
        out = json.loads(str(resp.read(), 'utf-8'))
        if ('Answer' in out.keys()) and (len(out['Answer']) > 0):
            output = out['Answer'][0]['data']
            if output.count('.') != 3 or (len(output.split('.')[-1]) == 0):
                return get_ip_from_host(hostname, max_count, cur_count + 1)
            else:
                return output.strip() 
    elif '.' in hostname and hostname.split('.')[-1][0] not in string.ascii_letters:
        return hostname
    else:
        return ''

if __name__ == "__main__":
    tested = {}
    for host in open('trs').read().split('\n'):
        if host.strip():
            count, host = host.split()
            server = urllib.parse.urlparse(host).netloc
            if not server:
                break
            if ':' in server:
                server = server.split(':')[0]
            if server not in tested.keys():
                ip = get_ip_from_host(server)
                if not ip:
                    ip = None
                if ip in ['127.0.0.1', '1.3.3.7']:
                    ip = None
                tested[server] = ip
                print(server, ip)
    dead = open('trz_dead', 'w')
    dead.write('\n'.join([host for (host, ip) in tested.items() if ip == None]))
