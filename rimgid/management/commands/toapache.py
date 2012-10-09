# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
#from polls.models import Poll
import subprocess

class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'
    
    can_import_settings = True

    def handle(self, *args, **options):
        from django.conf import settings

        sitename = "rimgid"
        host = "*"
        port = "8000"
        server_admin = "aa.veter@gmail.com"
        project_path = "/usr/local/www/" + sitename
        
        project_path = settings.PROJ_PATH
        control_path = project_path + "/control"
        logs_path = control_path + "/logs"
        admin_media_prefix = "/admin-media/"
        admin_media_root = project_path + "/../.env/lib/python2.6/site-packages/django/contrib/admin/media/"
        
        mass = [ ["$SITENAME",sitename],
            ["$HOST",host],
            ["$PORT",port],
            ["$SERVER_ADMIN",server_admin],
            ["$PROJECT_PATH",project_path],
            ["$CONTROL_PATH",control_path],
            ["$LOGS_PATH",logs_path],
            ["$ADMIN_MEDIA_PREFIX",admin_media_prefix],
            ["$ADMIN_MEDIA_ROOT",admin_media_root] ]
            
        cel_mass = [ ["$PROJECT_PATH",project_path],
            ["$CONTROL_PATH",control_path] ]
        
        to_apache = project_path + '/control/to_apache'
        apache_file = "/etc/apache2/sites-available/" + sitename
        ln_path = "/etc/apache2/sites-enabled/" + sitename
        
        celeryb = "/etc/init.d/celeryb"
        to_celeryb = control_path + "/celeryb"
        
        to_start_celery = [ '#! /bin/bash\n',
            'cd $PROJECT_PATH\n',
            './manage_py celeryd --settings=settings\n' ]
        start_celery = control_path +"/start_celery"
        
        to_sv_celery = [ '#!/bin/bash\n',
            'exec 2>&1\n',
            'exec '+start_celery+'\n']
        sv_celery = "/etc/sv/"+sitename+"_celery/run"
        
        to_sv_celery_log = ['#!/bin/bash\n',
        "LOG_FOLDER=/var/log/"+sitename+"_celery\n",
        'mkdir -p $LOG_FOLDER\n',
        'exec svlogd -tt $LOG_FOLDER\n']
        sv_celery_log = "/etc/sv/"+sitename+"_celery/log/run"

            
        def write_file(from_file, to_file, mass, from_list=False):
            def rewrite(line, mass):
                for m in mass:
                    line = line.replace(m[0], m[1])
                return line
            try:
                fw = open(to_file,"w")
                if from_list:
                    fr = from_file
                else:
                    fr = open(from_file)
                for line in fr:
                    fw.write(rewrite(line, mass),)
                fw.close()
            except:
                self.stdout.write("FILE from %s to %s ERROR!\n", from_file, to_file)
            
        def sub_exec(command):
            try:
                subprocess.check_call(command, shell=True)
            except:
                self.stdout.write(command +" ERROR!\n")
        
        self.stdout.write('PROJ_PATH = "%s"\n' % settings.PROJ_PATH)
        
        #write_file(to_apache, apache_file, mass)
        
        #sub_exec(" ".join(["ln","-s",apache_file,ln_path]))
        #sub_exec("apt-get install libapache2-mod-wsgi")
        #sub_exec("a2enmod wsgi")
        #sub_exec("/etc/init.d/apache2 restart")
        
        sub_exec("apt-get install runit")
        
        #write_file(to_celeryb, celeryb, cel_mass)
        write_file(to_start_celery, start_celery, cel_mass, from_list=True)
        
        sub_exec("mkdir /etc/sv/"+sitename+"_celery/")
        sub_exec("mkdir /etc/sv/"+sitename+"_celery/log/")
        write_file(to_sv_celery, sv_celery, [], from_list=True)
        write_file(to_sv_celery_log, sv_celery_log, [], from_list=True)
        
        #sub_exec("chmod +rwxX "+celeryb)
        sub_exec("chmod +rwxX "+start_celery)
        sub_exec("chmod +rwxX "+sv_celery)
        sub_exec("chmod +rwxX "+sv_celery_log)
        
        sub_exec("ln -s /etc/sv/"+sitename+"_celery /etc/service/"+sitename+"_celery")
            
        self.stdout.write("installing to apache finished!\n")

        