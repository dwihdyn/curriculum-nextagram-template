# all databases

import re
from models.base_model import BaseModel
import peewee as pw
from werkzeug.security import generate_password_hash


class UserCredential(BaseModel):
    name = pw.CharField(unique=False)
    email = pw.CharField()
    password = pw.CharField()

# uncomment validation when done production
    # dont do it in basemodel, because different class (UserCredential vs existingUser) need different validate rule
    def validate(self):
        # regex
        reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
        compile_regex = re.compile(reg)
        match_pass_regex = re.search(compile_regex, self.password)

        if not match_pass_regex:
            self.errors.append('''
            password must have :
            1) a number
            2) an uppercase & lowercase
            3) a special symbol (!,@,#,..)
            4) length 6 to 20 char
            ''')
        if not self.password == self.confPassword:
            self.errors.append('password and confirm password dont match')

        if len(self.errors) == 0:
            self.password = generate_password_hash(self.password)
