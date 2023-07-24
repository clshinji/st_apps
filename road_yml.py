import yaml

class yml_list:
    def __init__(self):
        with open('config.yml', 'r') as file:
            data = yaml.safe_load(file)
        
        self.column_names_pg1 = data['column_names_pg1']
        self.column_names_pg2 = data['column_names_pg2']
