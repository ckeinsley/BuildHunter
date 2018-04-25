from click_shell import shell 
import click as c
from redis_ import redisDriver

r = redisDriver.RedisDriver()

@shell(prompt= 'BuildHunter> ', intro='Welcome to BuildHunter!')
def cli():
    username = c.prompt('What is your username?')
    if r.is_user(username):
        r.active_user = username
    else:
        print(username + ' not found. Creating...')
        r.add_user(username, True)

@cli.command('username')
def get_active_user():
    print(r.active_user)

@c.option('--name', '-n', prompt=True)
@cli.command('build-add')
def add_build(name):
    r.add_build(name)

@c.option('--name', '-n', prompt=True)
@cli.command('build-delete')
def delete_build(name):
    r.delete_build(name)

@cli.command('builds')
def get_builds():
    for build in r.get_all_builds():
        print(build.decode('utf-8').partition(':')[2])

@c.option('--name', '-n', prompt=True)
@cli.command('build-set-active')
def set_active_build(name):
    r.active_build = name

@cli.command('build-get-active')
def get_active_build():
    print(r.active_build)

@c.option('--part', '-p', type=c.Choice(r.BUILD_PARTS), prompt=True)
@c.option('--id', '-i', type=int, prompt=True)
@cli.command('part-add')
def add_part(part, id):
    r.add_build_component(part, id)
    
@c.option('--part', '-p', type=c.Choice(r.BUILD_PARTS), prompt=True)
@cli.command('part-delete')
def delete_part(part):
    r.remove_build_component(part)




