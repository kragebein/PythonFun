#!/usr/bin/python3.6
import os, sys, requests, json, apt, psutil, time, subprocess
''' Updates Plex Media Server to latest version, requires subprocess, apt, psutil '''
# 0 = 32bit, 1 = 64bit, 3 = armv8, 4 = armv7
arch = 1
class upd():
    def __init__(self):
        ''' Initialize and check for update '''
        if os.getuid() != 0:
            print('Not root!')
            sys.exit(2)
        self.pid = 0
        print('1/4. Checking for update..', end='', flush=True)
        cache = apt.Cache()
        try:
            pkg = cache['plexmediaserver']
            versions = pkg.versions
            self.version = str(versions[0]).split('=')[1]
            print('({}) '.format(self.version), end='', flush=True)
        except:
            self.version = 0
            pass
        versions = requests.get('https://plex.tv/api/downloads/5.json').text
        versions = json.loads(versions)
        self.new = versions['computer']['Linux']['version']
        self.new_url = versions['computer']['Linux']['releases'][arch]['url']
        #self.version = str(0)
        if self.new > self.version:
            print('Update found! ({})'.format(self.new))
            self.update()
        else:
            print('No update needed.')

    def update(self):
        '''Do the update'''
        print('\r2/4. Downloading..', flush=True, end='')
        try:
            r = requests.get(self.new_url, allow_redirects=True)
            debfile = '/tmp/.' + self.new + '.deb'
            open(debfile, 'wb').write(r.content)
            print('OK')
        except Exception as R:
            print('Failed!\nInstall manually from:\n{}'.format(self.new_url))
            raise BaseException(R)
        print('\r3/4. Installing update..', flush=True, end='')
        data = subprocess.Popen(["dpkg", "-i", "{}".format(debfile)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        dataout, dataerr = data.communicate()
        if data.wait() == 0:
            print('OK')
        else:
            print('failed (error below)\n{}'.format(str(dataerr)))
            exit(1)
        print('\r4/4. Verifying install: ', flush=True, end='')
        time.sleep(2)
        if self.plexrunning() > 0:
            print('OK! PID: {}'.format(self.pid))
        else:
            print('Plex not running.')
            print('5/4. Starting Plex Media Server..', flush=True, end='')
            data = subprocess.Popen(["service", "plexmediaserver", "start"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if data.wait() == 0:
                if self.plexrunning() > 0:
                    print('OK! PID: {}'.format(self.pid))
            else:
                print('\nSorry..\nUnable to start Plex Media server again.')

    def plexrunning(self):
        activeplex = 0
        for proc in psutil.process_iter(['pid', 'name', 'username']):
            if proc.info['name'] == 'Plex Media Serv':
                self.pid = str(proc.info['pid'])
                activeplex += 1
        return activeplex
upd()