#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import webapp2
import string
import re
import cgi

# def escape_html(s):
#     return cgi.escape(s, quote = True)

# html boilerplate for the top of every page
page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>User Sign Up</title>
    <style type="text/css">
        .error {
            color: red;
        }
    </style>
</head>
<body>
    <h1>
        <a href="/">Sign Up</a>
    </h1>
"""

username_regex = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
password_regex = re.compile(r"^.{3,20}$")
email_regex = re.compile(r"^[\S]+@[\S]+.[\S]+$")

def valid_username(username):
    # username_regex.findall('')
    return username and username_regex.match(username)

def valid_password(password):
    return password and password_regex.match(password)

def valid_email(email):
    return not email or email_regex.match(email)

# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""
# a form for user signup
form = """
<form method="post">
    <table>
        <tr>
            <td>
                <label for="username">Username</label>
            </td>
            <td>
                <input type="text" name="username" placeholder="Enter Username" value="%(username)s" required>
                <span class="error">%(errorUsername)s</span>
            </td>
        </tr>
        <tr>
            <td>
                <label for="password">Password</label>
            </td>
            <td>
                <input type="password" placeholder="Enter Password" name="password" required>
                <span class="error">%(errorPassword)s</span>
            </td>
        </tr>
        <tr>
            <td>
                <label for="verify">Verify Password</label>
            </td>
            <td>
                <input type="password" placeholder="Re-Enter Password" name="verify"  required>
                <span class="error">%(errorVerify)s</span>
            </td>
        </tr>
        <tr>
            <td>
                <label for="email">E-mail (optional)</label>
            </td>
            <td>
                <input type="email" name="email" value="%(email)s">
                <span class="error">%(errorEmail)s</span>
            </td>
        </tr>
    </table>
        <input type="submit">
</form>
"""

class SignUp(webapp2.RequestHandler):
    def write_form(self, errorUsername="", errorPassword="", errorVerify="", errorEmail="", username="", email=""):
        self.response.out.write(form % {"errorUsername": errorUsername, "errorPassword":errorPassword, "errorVerify":errorVerify, "errorEmail":errorEmail, "username": username, "email": email})

    def get(self):
        self.write_form()

    def post(self):
        have_error = False
        user_username = self.request.get('username')
        user_password = self.request.get('password')
        user_verify = self.request.get('verify')
        user_email = self.request.get('email')

        errorUsername = ""
        errorPassword = ""
        errorVerify = ""
        errorEmail = ""

        if not valid_username(user_username):
            errorUsername = "Please enter a valid username"
            have_error = True

        if not valid_password(user_password):
            errorPassword = "Please enter a valid password"
            have_error = True
        elif user_password != user_verify:
            errorVerify = "Your passwords do not match"
            have_error = True

        # e-mail is optional, but if entered, verify.
        if not valid_email(user_email):
            errorEmail = "Please enter a valid e-mail address"
            have_error = True

        if have_error:
            self.write_form(errorUsername, errorPassword, errorVerify, errorEmail, user_username, user_email)
        else:
            username = self.request.get('username')
            self.redirect('/welcome?username=%s' % username)

class Welcome(webapp2.RequestHandler):
    def get(self):
        username = self.request.get('username')
        content = "Welcome " + username + "!"
        self.response.out.write(content)

app = webapp2.WSGIApplication([
    ('/', SignUp),
    ('/welcome', Welcome)
], debug=True)



# From Slack
# class MainHandler(webapp2.RequestHandler):
    # def write_form(self):

    # def get(self):
        # content = write_form()
        # self.response.write(content)

    # def post(self):
       #add a redirect upon successful input

# class SuccessHandler(webapp2.RequestHandler):
#     def get(self):
        #get the username parameter
        #use self.response.write() to create a success message
