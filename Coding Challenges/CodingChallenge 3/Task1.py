import os
import shutil

def make_dir(main,sub = 0,subsub = 0):
    if(sub == 0):
        os.makedirs(main)
    elif(sub != 0 and subsub == 0):
        os.makedirs('%s/%s' % (main, sub))
    else:
        os.makedirs('%s/%s/%s' % (main, sub, subsub))

make_dir('Draft Code','Pending')
make_dir('Draft Code','Complete')
make_dir('includes')
make_dir('layout','default')
make_dir('layout','post','posted')
make_dir('site')

shutil.rmtree('Draft Code')
shutil.rmtree('includes')
shutil.rmtree('layout')
shutil.rmtree('site')