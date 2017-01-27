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
import re
import cgi

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

# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""

# a form for user signup
add_form = """
<form method="post">
    <table>
        <tr>
            <td>
                <label for="username">Username</label>
                <span class="error"></span>
            </td>
            <td>
                <input type="text" name="username"/>
            </td>
        </tr>
        <tr>
            <td>
                <label for="password">Password</label>
                <span class="error"></span>
            </td>
            <td>
                <input type="text" name="password"/>
                <span class="error"></span>
            </td>
        </tr>
        <tr>
            <td>
                <label for="verify">Verify Password</label>
            </td>
            <td>
                <input type="text" name="verify"/>
                <span class="error"></span>
            </td>
        </tr>
        <tr>
            <td>
                <label for="email">E-mail (optional)</label>
                <span class="error"></span>
            </td>
            <td>
                <input type="email" name="email"/>
                <span class="error"></span>
            </td>
        </tr>
    </table>
    <input type="submit"/>
</form>
"""
username_regex = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
password_regex = re.compile(r"^.{3,20}$")
email_regex = re.compile(r"^[\S]+@[\S]+.[\S]+$")

class MainHandler(webapp2.RequestHandler):
    def get(self):
        # if we have an error, make a <p> to display it
        error = self.request.get("error")
        error_element = "<p class='error'>" + error + "</p>" if error else ""

        # combine all the pieces to build the content of our response
        main_content = add_form + error_element
        content = page_header + main_content + page_footer
        self.response.write(content)

    def post(self):
        user_name = self.request.get("username")
        password = self.request.get("password")
        password_verify = self.request.get("verify")
        # e-mail is optional, but if entered, verify.
        email = self.request.get("email")


        if user_name != username_regex.match(user_name):
            error = "Please enter a valid username"
            error_escaped = cgi.escape(error, quote=True)
            self.redirect("/?error=" + error_escaped)

        elif password != password_regex.match(password):
            error = "Please enter a valid password"
            error_escaped = cgi.escape(error, quote=True)
            self.redirect("/?error=" + error_escaped)

        elif password != verify:
            error = "Your passwords do not match"
            error_escaped = cgi.escape(error, quote=True)
            self.redirect("/?error=" + error_escaped)

        elif email != email_regex.match(email):
            error = "Please enter a valid e-mail address"
            error_escaped = cgi.escape(error, quote=True)
            self.redirect("/?error=" + error_escaped)

        content = "<h5>" + "Welcome " + user_name + "</h5"
        self.response.write(content)






# Example from crossed_off_movie in Flicklist:
# """
# crossed_off_movie = self.request.get("crossed-off-movie")
# if (crossed_off_movie in getCurrentWatchlist()) == False:
#     # the user tried to cross off a movie that isn't in their list,
#     # so we redirect back to the front page and yell at them
#
#     # make a helpful error message
#     error = "'{0}' is not in your Watchlist, so you can't cross it off!".format(crossed_off_movie)
#     error_escaped = cgi.escape(error, quote=True)
#
#     # redirect to homepage, and include error as a query parameter in the URL
#     self.redirect("/?error=" + error_escaped)
#
# # if we didn't redirect by now, then all is well
# crossed_off_movie_element = "<strike>" + crossed_off_movie + "</strike>"
# confirmation = crossed_off_movie_element + " has been crossed off your Watchlist."
# content = page_header + "<p>" + confirmation + "</p>" + page_footer
# self.response.write(content)
# """


app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)

# """
# # First try, worked but ugly bc text boxes didn't line up!
# # add_form = """
# # <form action="/add" method="post">
# #     <label>
# #         Username
# #         <input type="text" name="username"/>
# #         <p></p>
# #     </label>
# #     <label>
# #         Password
# #         <input type="text" name="password"/>
# #         <p></p>
# #     </label>
# #     <label>
# #         Verify Password
# #         <input type="text" name="verify-password"/>
# #         <p></p>
# #     </label>
# #     <label>
# #         E-mail (optional)
# #         <input type="email" name="e-mail-optional"/>
# #         <p></p>
# #     </label>
# #     <input type="submit"/>
# # </form>
# # """
# # content = page_header + add_form + page_footer
# # self.response.write(content)
#
# # def post(self):
# #     edit_header = "<h4>Welcome </h4>"
# #
# #
# #
# #     self.response.write(add_form)
# """
