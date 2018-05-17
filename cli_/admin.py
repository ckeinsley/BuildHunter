import sys
sys.path.insert(0, '../cli_')
sys.path.insert(0, '../kafka_')
from click_shell import shell 
import click as c
import pickle
from kafka_ import producer as prod

@shell(prompt= 'Admin> ', intro='BuildHunter Administrator Interface')
def admin():
    pass

@c.option('--file-path', '-f', prompt=True, type=str)
@admin.command('insert-armor')
def insert_armor(file_path):
    armor_file = open(file_path, 'rb')
    armor = pickle.load(armor_file, encoding='unicode')
    armor_file.close()
    prod.insert_armor(armor)

def main():
    admin()

if __name__ == "__main__":
    main()

