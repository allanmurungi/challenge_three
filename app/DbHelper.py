import psycopg2
import psycopg2.extras


class DbCalls:

    """A class that will hold database query functions"""

    def __init__(self):
        """DbCalls constructor"""
        self.connection_string = "dbname=maintenance user=postgres password=root host=localhost"
        self.con = None
        self.cur = None

    def connect_to_db(self):
        """ This function creates a connection to the database server"""
        """and a cursor object through which querries are executed"""
        try:
            self.con = psycopg2.connect(self.connection_string)
            self.cur = self.con.cursor()
            return True
        except:
            return False

    def create_new_user(self, email, password, role):
        """ This functions uses the cursor object to insert a new user/row to the users 
        table in the database"""
        self.cur.execute(
            "INSERT INTO users (email,password,role) VALUES (%s, %s,%s)", (email, password, role))
        self.con.commit()
        return True

    def check_existing_user(self, email):
        """ a function to get if a user exists"""

        self.cur.execute("SELECT * FROM users where email=%s", (email))
        while True:

            row = self.cur.fetchone()
            if row == None:
                return False
                break
            else:
                return True
                break

    def log_in_user(self, email, password):
        """This function uses the cursor object to check if a certain user exists in the users table
        given the user details provided"""
        result = []
        self.cur.execute("SELECT * FROM users where email=%s", (email))
        row = self.cur.fetchone()
        result.append(row[1])
        result.append(row[2])

        return result

    def get_user_requests(self, email):
        """This function users the cursor object to get a user's requests from the requests table"""
        self.cur.execute("SELECT * FROM requests where req_owner=%s", (email))
        reqs = []
        while True:

            row = self.cur.fetchone()

            if row == None:
                break
            reqs.append(
                {"req_title": row[1], "req_details": row[2], "req_owner": row[3], "req_status": row[4]})
        return reqs

    def get_all_requests(self):
        """ This function uses the cursor object to get all requests onnthe application 
        from the requests' table  """
        self.cur.execute("SELECT * FROM requests")
        reqs = []
        while True:

            row = self.cur.fetchone()

            if row == None:
                break
            reqs.append(
                {"req_title": row[1], "req_details": row[2], "req_owner": row[3], "req_status": row[4]})
        return reqs

    def get_request(self, req_id):
        """This function uses the cursor object to get a specific request using its id from the
         requests table """
        self.cur.execute("SELECT * FROM requests where id=%s", (req_id))
        result = ""

        while True:

            row = self.cur.fetchone()
            result = {"req_title": row[1], "req_details": row[2],
                      "req_owner": row[3], "req_status": row[4]}
            if row == None:
                result = "request not found"
                return result

            break
        return result

    def add_request(self, req_title, req_details, req_owner, req_status):
        """ This function uses the cursor object to add a new request/row to the requests table """
        self.cur.execute("INSERT INTO requests (req_title,req_details,req_owner,req_status) VALUES (%s, %s,%s,%s)",
                         (req_title, req_details, req_owner, req_status))
        self.con.commit()
        return True

    def delete_request(self, req_id):
        """ This function uses the cursor object to delete request/row from the requests table 
        given its id """
        self.cur.execute("delete FROM requests where id=%s", (req_id))
        self.con.commit()

    def edit_request(self, req_title, req_details, req_owner, req_status, req_id):
        """ This function uses the cursor object to edit/modify a request/row in the requests table """

        self.cur.execute("UPDATE requests SET req_title=%s req_details=%s req_owner=%s req_status=%s WHERE req_id=%s",
                         (req_title, req_details, req_owner, req_status, req_id))
        self.con.commit()

    def approve_request(self, req_id):
        """ This function uses the cursor object to approve request/row in the requests table given 
        its id """
        req_status = "approved"
        self.cur.execute("UPDATE requests SET  req_status=%s WHERE req_id=%s",
                         (req_status, req_id))
        self.con.commit()

    def resolve_request(self, req_id):
        """ This function uses the cursor object to resolve a request/row in the requests table given 
        its id """
        req_status = "resolved"
        self.cur.execute("UPDATE requests SET  req_status=%s WHERE req_id=%s",
                         (req_status, req_id))
        self.con.commit()

    def disapprove_request(self, req_id):
        """ This function uses the cursor object to disapprove request/row in the requests table given 
        its id """
        req_status = "disapprove"
        self.cur.execute("UPDATE requests SET  req_status=%s WHERE req_id=%s",
                         (req_status, req_id))
        self.con.commit()

    def kill_connection(self):
        """ This function kills or ends the connection to the database server """
        self.cur.close()
        self.con.close()
