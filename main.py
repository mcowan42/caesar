import webapp2
import cgi

from caesar import encrypt

page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>Caesar Cypher</title>
    <style type="text/css">
        .error {
            color: red;
        }
    </style>
</head>
<body>

"""

# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""

class MainHandler(webapp2.RequestHandler):
    def get(self):

        edit_header = """<h1><a href="/">Caesar Cypher</a></h1>
        <p>Encrypt a word or phrase using the form below:</p>"""

        cypher_form = """
        <form action="/encypher" method="post">
            <div>
                <label for="rot">Rotate by:</label>
                <input type="text" name="rot" value="0">
                <p class="error"></p>
            </div>
            <label for="text">Enter text to be encrypted:</label>
            <br>
            <textarea type="text" name="text"></textarea>
            <br>
            <input type="submit">
        </form>
        """


        error = self.request.get("error")
        error_element = "<p class='error'>" + error + "</p>" if error else ""

        main_content = edit_header + cypher_form + error_element
        response = page_header + main_content + page_footer
        self.response.write(response)

class Encypher(webapp2.RequestHandler):
    def post(self):

        text=self.request.get("text")

        #check that text box is not empty
        if not text:
            error = "You did not enter any text; Please enter text to be encrypted"
            self.redirect("/?error=" + error)

        #check for any html in the text box
        text=cgi.escape(text, quote=True)

        rot=self.request.get("rot")

        #check that the rotation value is an integer
        try:
            val = int(rot)
        except (ValueError or UnicodeError):
            error = "Rotation must be by an integer amount"
            self.redirect("/?error=" + error)
            return

        if(float(rot)%1 != 0):
            error = "Rotation must be by an integer amount"
            self.redirect("/?error=" + error)
        else:
            rot=int(rot)

        #run the cypher algorithm
        answer = encrypt(text,rot)

        # build response content
        linkback="""<a href="/">Encrypt another phrase</a>
        """
        response = page_header + "<p>" + answer + "</p>" + linkback + page_footer
        self.response.write(response)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/encypher', Encypher)
], debug=True)
