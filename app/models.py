

class UserModel:
    

    
    
    def save_to_db(self):
        pass
        
    

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)

    @staticmethod
    def validate_entry(entry):
        pass
    

