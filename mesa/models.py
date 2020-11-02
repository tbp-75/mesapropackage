import pandas as pd


class dataconnector:
    def __init__(self):
        self.file = 'mesa/products.csv'

    def read_data(self):
        self.data = pd.read_csv(self.file, decimal='.')
        return self.data

    def append_data(self, record):
        self.data = pd.read_csv(self.file, decimal='.')
        self.record = record
        self.record.to_csv(self.file, mode='a', index=False, header=False, decimal='.')
        return self.read_data()

    def delete_data(self, record):
        self.data = pd.read_csv(self.file, decimal='.')
        self.record = record
        item_to_delete = record.name[0]
        self.data.query('name !=@item_to_delete').to_csv(self.file, mode='w', index=False, header=True, decimal='.')
        return self.read_data()

    def edit_data(self, record):
        self.data = pd.read_csv(self.file, decimal='.')
        self.record = record
        item_to_edit = record.name[0]

        idx = self.data.query('name == @item_to_edit').index[0]

        for i in ['price per gm', 'quantity']:
            self.data.loc[idx, i] = record.loc[0, i]

        self.data.to_csv(self.file, mode='w', index=False, header=True, decimal='.')

        return self.read_data()

    def get_record(self, item):
        self.data = pd.read_csv(self.file, decimal='.')
                
        rec = self.data.query('name == @item')

        return rec