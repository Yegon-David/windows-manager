import sqlite3

# CREATE_DB = 'create database {}'
DB_NAME = 'database.db'

CREATE_TABLE_DIMENSIONS = '''CREATE TABLE IF NOT EXISTS dimension (
    id integer primary key autoincrement,
    x integer not null,
    y integer not null,
    screen_len integer not null
 
    )

'''

UPDATE_DIM = 'update dimension set x=?,y=?,screen_len=? where id = 1'
GET_XY = 'select x,y,screen_len from dimension'
INSERT_XY = 'insert into dimension (x,y,screen_len) values (?,?,?)'

class DBControl:
    def __init__(self) -> None:
        self.conn = None
        self.c = None

    def open(self):    
        self.conn = sqlite3.connect(DB_NAME)
        self.c = self.conn.cursor()

    def close(self):
        self.conn.commit()
        self.conn.close()

    def create_table(self,script:str)->None:
        self.open()
        self.c.execute(script)
        self.close()

    def insert_row(self,script:str,values:tuple)->None:
        self.open()
        self.c.execute(script,values)
        self.close()

    def get_all_data(self,table):
        self.open()
        self.c.execute('select * from {}'.format(table))
        data = self.c.fetchall() 
        self.close()  
        return data

class Dimensions(DBControl):
    def __init__(self) -> None:
        super().__init__()

        self.create_table(CREATE_TABLE_DIMENSIONS)

    def get_dimensions(self):
        self.open()
        self.c.execute(GET_XY) 
        data = self.c.fetchone()
        # print(data,self.c.fetchall(),self.c.fetchmany())
        self.close()
        return data

    def update_xy_s(self,x:int,y:int,s:int)->None:
        self.open()
        self.c.execute(UPDATE_DIM,(x,y,s))   
        self.close() 

    def insert_xy_s(self,x:int,y:int,s:int)->None:
        self.open()
        self.c.execute(INSERT_XY,(x,y,s))   
        self.close() 

    def get_all_data(self, table='dimension'):
        return super().get_all_data(table)    
