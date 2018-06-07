import psycopg2,psycopg2.extras

class DbCalls:

    """A class that will hold database query functions"""
    def __init__(self):

        """DbCalls constructor"""
        self.connection_string="dbname=maintenance user=postgres password=root host=localhost"
        self.con=None
        self.cur=None
        
    def connect_to_db(self):
        """ This function creates a connection to the database server"""
        """and a cursor object through which querries are executed""" 
        try:
            self.con= psycopg2.connect(self.connection_string)
            self.cur=self.con.cursor()
            return True
        except:
            return False

    def create_new_user(self,email,password,role):
        """ This functions uses the cursor object to insert a new user/row to the users 
        table in the database"""
        self.cur.execute("INSERT INTO users (email,password,role) VALUES (%s, %s,%s)",(email,password,role))
        self.con.commit()
        return True
        
    def check_existing_user(self,email):
        pass    

    def log_in_user(self,email,password):
        """This function uses the cursor object to check if a certain user exists in the users table
        given the user details provided"""
        pass

    def get_user_requests(self,email):
        """This function users the cursor object to get a user's requests from the requests table"""
        pass

    def get_all_requests(self):
        """ This function uses the cursor object to get all requests onnthe application 
        from the requests' table  """   
        pass 


    def get_request(self,req_id):
        """This function uses the cursor object to get a specific request using its id from the
         requests table """
        pass

    def add_request(self,req_title,req_details,req_owner,req_status):
        """ This function uses the cursor object to add a new request/row to the requests table """
        self.cur.execute("INSERT INTO requests (req_title,req_details,req_owner,req_status) VALUES (%s, %s,%s,%s)",(req_title,req_details,req_owner,req_status))
        self.con.commit()
        return True
        pass
    def delete_request(self,req_id):
        """ This function uses the cursor object to delete request/row from the requests table 
        given its id """
        pass

    def edit_request(self,req_title,req_details,req_owner,req_status):
        """ This function uses the cursor object to edit/modify a request/row in the requests table """
        pass

    def approve_request(self,req_id):
        """ This function uses the cursor object to approve request/row in the requests table given 
        its id """
        pass

    def resolve_request(self,req_id):
        """ This function uses the cursor object to resolve a request/row in the requests table given 
        its id """
        pass
    
    def disapprove_request(self,req_id):
        """ This function uses the cursor object to disapprove request/row in the requests table given 
        its id """
        pass
    
    def kill_connection(self):
        """ This function kills or ends the connection to the database server """
        self.cur.close()
        self.con.close()
        
