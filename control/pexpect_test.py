# -*- coding: utf-8 -*-
import pexpect

child = pexpect.spawn('su')
child.expect("Пароль:")
child.sendline("udtufugeve")

file_path = "rimgid/images/red_point_mini_3.png"

child.expect(":")
s = '''git commit -a -m "*** added file '"'''+file_path+'''"' ***"'''
child.sendline(s)

child.sendline('exit')
child.expect(pexpect.EOF)

