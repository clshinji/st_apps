import yaml

class yml_list:
    def __init__(self):
        with open('config.yml', 'r') as file:
            data = yaml.safe_load(file)
        
        self.update_date = data['update_date']
        self.column_names_pg1 = data['column_names_pg1']
        self.column_names_pg2 = data['column_names_pg2']

    def set_update_date(self, update):
        """ 画面上に表示する更新日を変更する
        Args:
            update(datetime) :変更後の日付
        """
        with open('config.yml', 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
        
        data['update_date'] = update

        with open('config.yml', 'w', encoding='utf-8') as file:
            yaml.dump(data, file, allow_unicode=True, default_flow_style=False, sort_keys=False)
        
