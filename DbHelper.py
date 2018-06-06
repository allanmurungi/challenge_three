import psycopg2,psycopg2.extras

class DbCalls:

    """A class that will hold database query functions"""
    __init__(self):

        """DbCalls constructor"""
        self.connection_string="dbname=maintenance user=allan password=root host=localhost"
        self.con
        self.cur
        
    def connect_to_db(self):
        """ This function creates a connection to the database server and a cursor object through which querries are executed"""

        try:
            self.con= psycopg2.connect(self.connection_string)
            self.cur=self.con.cursor()
            return True
        except:
            return False

    def kill_connection(self):
        """ This function kills or ends the connection to the database server """
        
