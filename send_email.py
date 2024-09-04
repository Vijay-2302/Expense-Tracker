from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

class Register():
    def __init__(self):
        self.FROM_EMAIL = 'ibm.expensetracker2022@gmail.com'
        # update to your dynamic template id from the UI
        self.TEMPLATE_ID = 'd-fd9c0124a1594ed8a582d9d382e76c06'

    def get_email(self,email):
        self.email = email

    def SendDynamic(self):

        # create Mail object and populate
        message = Mail(
            from_email=self.FROM_EMAIL,to_emails=self.email)
        # pass custom values for our HTML placeholders
        message.dynamic_template_data = {
            'subject': 'SendGrid Test',
            'place': 'New York City',
            'event': 'Twilio Signal'
        }
        message.template_id = self.TEMPLATE_ID
        # create our sendgrid client object, pass it our key, then send and return our response objects
        try:
            sg = SendGridAPIClient('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')
            response = sg.send(message)
            code, body, headers = response.status_code, response.body, response.headers
            print(f"Response code: {code}")
            print(f"Response headers: {headers}")
            print(f"Response body: {body}")
            print("Dynamic Messages Sent!")
        except Exception as e:
            print("Error: {0}".format(e))
        return str(response.status_code)
