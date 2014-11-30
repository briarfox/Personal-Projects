import hashlib
conf = ''
with open('config.conf','w') as f:
    #[host]
    f.write('[host]\n')
    #url
    print '+++Setting up host.+++'
    print '+Server Info+'
    res = raw_input('Server address: ')
    f.write('server=%s\n'% res)
    res = raw_input('Port: ')
    f.write('port=%s\n' % res)
    res = raw_input('Password: ')
    f.write('passwd=%s\n\n' % hashlib.md5(res).hexdigest())
    
    print '+Garage Camera+'
    f.write('[camera]\n')
    res = raw_input('Server: ')
    f.write('server=%s\n'% res)
    res = raw_input('Port: ')
    f.write('port=%s\n'% res)
    res = raw_input('User: ')
    f.write('user=%s\n'% res)
    res = raw_input('Password: ')
    f.write('passwd=%s\n'% res)
    
    #rpi/arduino
    print '+RPi Setup+'
    print '--BCM Pin numbers--'
    f.write('[rpi]\n')
    res = raw_input('Open Pin: ')
    f.write('open=%s\n' % res)
    res = raw_input('Sensor Pin: ')
    f.write('sensor=%s\n\n' % res)
    
    #mail setup
    print '+Mail Setup+'
    f.write('[mail]\n')
    res = raw_input('Send as: ')
    f.write('send_as=%s\n' % res)
    res = raw_input('SMTP Server: ')
    f.write('smtp=%s\n' % res)
    res = raw_input('Server port: ')
    f.write('port=%s\n' % res)
    res = raw_input('TTL? (y,n): ')
    f.write('ttl=%s\n' % res)
    res = raw_input('Username: ')
    f.write('user=%s\n' % res)
    res = raw_input('Password: ')
    f.write('passwd=%s\n' % res)
    res = raw_input('Send To(ex. test@aol.com, fake@emial.com): ')
    f.write('recipients=%s\n' % res)
    f.write('notify=True\n')
