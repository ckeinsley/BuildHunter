import sys
sys.path.insert(0, '../cli_')
from click_shell import shell 
import click as c
from cli_ import cli_state

from pprint import pprint

r = cli_state.CliState()

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

@c.option('-u', '--username', prompt=True)
@cli.command('user-change')
def change_active_user(username):
    if r.is_user(username):
        r.active_user = username
    else:
        print(username + ' not found. Creating...')
        r.add_user(username, True)

@cli.command('user-delete')
def delete_user():
    if c.confirm('This will delete all information associated with ' + r.active_user + '. Are you sure you want to continue?'):
        r.delete_user(r.active_user)

####----Builds----####

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

# TODO need MAJOR refactor
@cli.command('build-get-details')
def get_build_details():
    part_dict = r.get_build_parts()
    for part, id in part_dict.items():
        if id != None:
            item_type = 'armor'
            if part == 'weapon':
                item_type = part
            name = r.get_object_name(int(id), item_type)
            decorations = r.get_decorations(part)
            print(part.capitalize() + ': ' + name.decode('utf-8'), end='\t')
            if decorations != None:
                print('Decorations:')
                for d in decorations:
                    d_name = r.get_object_name(d, 'decoration')
                    print(d_name.decode('utf-8'))
    print("Total Defense: \t" + str(r.get_build_total_defense()))
    print("Resistances: ")
    for k, v in r.get_build_resistances().items():
        print('\t' + k.capitalize() + ': ' + str(v))
    print("Skills: ")
    for k, v in r.get_build_skills().items():
        print('\t' + k.capitalize() + ': ' + str(v))
        
####----Parts----####

@c.option('--part', '-p', type=c.Choice(r.BUILD_PARTS), prompt=True)
@c.option('--id', '-i', type=int, prompt=True)
@cli.command('part-add')
def add_part(part, id):
    item_type = 'armor'
    if part == 'weapon':
        item_type = part
    if r.is_object(id, item_type):
        if (r.is_part(id, part)):
            r.add_build_component(part, id)
        else:
            raise ValueError(str(id) + ' is not a valid ' + part)
    else:
        raise ValueError(str(id) + ' is not a piece of ' + item_type)
    
@c.option('--part', '-p', type=c.Choice(r.BUILD_PARTS), prompt=True)
@cli.command('part-delete') 
def delete_part(part):
    r.remove_build_component(part)

####----Objects----####

@c.option('--id', '-i', prompt=True, type=int)
@c.option('--type_', '-t', prompt=True, type=c.Choice(r.ITEM_TYPES))
@cli.command('object-name')
def get_object_name(id, type_):
    print(r.get_object_name(id, type_).decode('utf-8'))

@c.option('--name', '-n', prompt=True)
@c.option('--type_', '-t', prompt=True, type=c.Choice(r.ITEM_TYPES.union(r.BUILD_PARTS)))
@cli.command('object-name-search')
def search_object_name(name, type_):
    item_type = type_ 
    if item_type not in r.ITEM_TYPES:
        item_type = 'armor'
    for obj in r.search_object_name(name, item_type):
        if item_type is type_ or r.is_part(int(obj[1].decode()),type_):
            print(obj[1].decode() + ': ' + obj[0].decode('utf-8'))

####----Items----####

@c.option('--id', '-i', prompt=True, type=int)
@cli.command('item-info')
def get_item_info(id):
    pprint(r.get_item_data(id))

####----Decorations----####

@c.option('--id', '-i', prompt=True, type=int)
@cli.command('decoration-info')
def get_decoration_data(id):
    pprint(r.get_decoration_data(id))

@c.option('--part', '-p', prompt=True, type=c.Choice(r.BUILD_PARTS))
@c.option('--decoration-id', '-i', prompt=True, type=int)
@cli.command('decoration-add')
def add_decoration(part, decoration_id):
    if (r.is_decoration(decoration_id)):
        r.add_decoration(part, decoration_id)
    else:
        raise ValueError(str(decoration_id) + ' is not a valid decoration')


@c.option('--part', '-p', prompt=True, type=c.Choice(r.BUILD_PARTS))
@c.option('--decoration-id', '-i', prompt=True, type=int)
@cli.command('decoration-remove')
def remove_decoration(part, decoration_id):
    if (r.is_decoration(decoration_id)):
        decorations = r.get_decorations(part)
        if str(decoration_id) in decorations:
            r.remove_decoration(part, decoration_id)
        else:
            raise ValueError(str(decoration_id) + 'is not in the build')
    else:
        raise ValueError(str(decoration_id) + ' is not a valid decoration')

@c.option('--part', '-p', prompt=True, type=c.Choice(r.BUILD_PARTS))
@cli.command('decoration-remove-all')
def remove_all_decorations(part):
    r.remove_all_decorations(part)

####----Advanced Features----####

@c.option('--skill', '-s', type=c.Tuple([str, int]), multiple=True)
@cli.command('generate-armor-sets')
def generate_armor_sets(skill):
    skill_list = []
    print(skill_list)
    for tup in skill:
        id = int(r.get_object_id(tup[0], 'skill'))
        value = tup[1]
        skill_list.append((id, value))
    print(skill_list) #TODO: Lookup armor set in Neo4J
    pprint(r.get_build_by_attr_value(skill_list))

def main():
    cli()

if __name__ == "__main__":
    main()

