from flask import Flask
from flask import jsonify
from supabase import create_client, Client



app = Flask(__name__)

SUPABASE_URL = 'https://tfnmnuiqumyolwayzbrh.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRmbm1udWlxdW15b2x3YXl6YnJoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTkzNTA1NDUsImV4cCI6MjAzNDkyNjU0NX0.hLndFZQvL94LYhllTZnpJXRqO-84ZSlrI9bofe6dVFE'

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

data = supabase.table('users').select('*').execute()

print(data)


class User:
    def __init__(self, id, firstName, lastName, dateOfBirth, onCreate):
        self.id = id
        self.firstName = firstName
        self.lastName = lastName
        self.dateOfBirth = dateOfBirth
        self.onCreate = onCreate

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data['id'],
            firstName=data['firstName'],
            lastName=data['lastName'],
            dateOfBirth=data['dob'],
            onCreate=data['onCreate']
        )

    def to_dict(self):
        return {
            'id': self.id,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'dateOfBirth': self.dateOfBirth.split('T')[0] if self.dateOfBirth else None,
            'onCreate': self.onCreate.split('T')[0] if self.onCreate else None
        }

    def __repr__(self):
        return f'<User {self.firstName} {self.lastName}>'
    


@app.route('/')
def index():
    response = supabase.table('users').select('*').execute()
    
    if 'error' in response:
        return jsonify({'error': response.error.message}), 500
    
    users_data = response.data
    print(users_data)
    
    users = [User.from_dict(user_data) for user_data in users_data]
    
    listOfUsers = [user.to_dict() for user in users]
    
    return jsonify(listOfUsers)


if __name__ == "__main__": 
    app.run(debug=True)