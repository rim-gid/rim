# -*- coding: utf-8 -*-
def git_add(file_path):
    import subprocess
    pre = "/usr/local/www/rim/"
    if pre in file_path:
        file_path = file_path[len(pre):]
    print "new file_path:", file_path
    #print "call =", subprocess.call("git add "+file_path, cwd=pre, shell=True)
    
    #p.communicate("ceTNil")
    #return
    try:
        subprocess.check_call("git add "+file_path, cwd=pre, shell=True)
    except:
        print "git add ERROR"
    else:
        print "git add SUCCESS"
        try:
            #mp = get_main_params()
            import pexpect

            child = pexpect.spawn('su')
            child.expect("Пароль:")
            child.sendline("udtufugeve")
            
            child.expect(":")
            s = '''git commit -a -m "*** added file '"'''+file_path+'''"' ***"'''
            child.sendline(s)

            child.sendline('exit')
            child.expect(pexpect.EOF)
            
            #subprocess.check_call(s, cwd=pre, shell=True)
        except:
            print "git commit ERROR"
        else:
            print "git commit SUCCESS"
        
def git_push():
    #return
    #import subprocess
    #p = Popen("su")
    #p.communicate("ceTNil")
    def get_branch_name():
        import subprocess
        pre = "/usr/local/www/rim/"
        p = subprocess.Popen("git branch | grep \*", cwd=pre, shell=True, stdout=subprocess.PIPE)
        out = p.stdout.read()
        return out[1:]
    branch = get_branch_name()
    #print "out =", out
    try:
        #mp = get_main_params()
        import pexpect

        child = pexpect.spawn('su')
        child.expect("Пароль:")
        child.sendline("udtufugeve")
        
        child.expect(":")
        child.sendline('git push origin '+branch)

        child.expect("id_rsa': ")
        child.sendline(u'lhepmz')

        child.sendline('exit')
        child.expect(pexpect.EOF)
    except:
        print "git push ERROR"
    else:
        print "git push SUCCESS"

#git_add("/usr/local/www/rim/rimgid/images/_r.png")
git_push()