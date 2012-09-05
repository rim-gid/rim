# -*- coding: utf-8 -*-
from celery.task import task
import subprocess, pexpect, settings
from settings import MP

@task()
def duplicate_article(x, y):
    return x + y

@task(ignore_result=True)
def duplicate_image(file_path):
    pre = settings.PROJ_PATH + "/"
    if pre in file_path:
        file_path = file_path[len(pre):]
    print "duplicate_image: new file_path:", file_path
    
    command = ' '.join(['scp', settings.MEDIA_ROOT + file_path,
            'root@'+settings.get_pointed_address()+':'+settings.MEDIA_ROOT+'images/'])
    print "duplicate_image: command", command
    child = pexpect.spawn( command )
    child.expect(":")
    child.sendline(settings.get_pointed_pass())
    
    ok = False
    try:
        i = child.expect(['100%', 'No such file or directory', 'yes/no'])
        if i==0:
            ok = True
        elif i==2:
            child.sendline("yes\n")
            i = child.expect(['100%', 'No such file or directory'])
            if i==0:
                ok = True
    except:
        ok = False
    if not ok:
        command = ' '.join(['scp', 'root@'+settings.get_pointed_address()+':'+settings.MEDIA_ROOT + file_path,
            settings.MEDIA_ROOT+'images/'])
        print "new command:", command
        child = pexpect.spawn( command )
        child.expect(":")
        #print "pass:", settings.get_pointed_pass()
        child.sendline(settings.get_pointed_pass())
        child.expect(':')

    child.sendline('exit')
    child.expect(pexpect.EOF)
    
    print "FIN"

@task(ignore_result=True)
def dump_pages():
    passw = settings.DATABASES['default']['PASSWORD']
    db = settings.DATABASES['default']['NAME']
    user = settings.DATABASES['default']['USER']
    
    tables = [
        'articles_article',
        'articles_article_specials',
        'articles_articlespecial',
        'articles_articletype',
        'articles_articletype_specials',
        'articles_articletypespecial',
        'articles_foto',
        'articles_foto_sites'
        'django_flatpage'
        'django_flatpage_sites'
    ]
    
    command = ' '.join(["mysqldump", "-u", user, " -p" + passw, db ] + tables + [">", "article.sql"])
    print "dump_pages: command", command
        
    #try:
    subprocess.check_call(command, cwd=pre, shell=True)
    #except:
    #    print "git add ERROR"
    #else:
    #    print "git add SUCCESS"
    #    try:
    #mysqldump -u aaveter_0 -puR1zdiC7 aaveter_0 articles_article articles_article_specials articles_articlespecial articles_articletype articles_articletype_specials articles_articletypespecial articles_foto articles_foto_sitesdjango_flatpagedjango_flatpage_sites > article.sql

