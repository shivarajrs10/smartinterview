
import os
import smtplib
import imghdr
from email.message import EmailMessage


def mail_send(name, mail, password):

    EMAIL_ADDRESS = "srsbangalore@gmail.com"
    EMAIL_PASSWORD = "Hellosir@123"

    msg = EmailMessage()
    msg['Subject'] = 'Smart Interviewer'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = mail

    msg.set_content('This is a plain text email')

    msg.add_alternative("""\
   <!DOCTYPE html>
<html>

<body>

    <h3><strong>Dear {0},</strong></h3>

    <h4><strong>Congratulations !!! </strong> </h4>

    We are glad to inform you that based on your skill set, your profile has been shortlisted for next round which is an
    online test. The instructions for the test are as follows: <br>
    <strong>Please read the instructions very carefully</strong><br>
    1. Test will be conducted using an online tool: <strong> "Smart Interviewer".</strong><br>
    2. You are being monitored and your facial expressions will be captured continuously. <br>
    3. After clicking on the test link provided below you have to sign in by using given credentials. <br>
    4. Once you are signed in you will be asked to rate yourself from the dropdown menu in three levels of expertise for
    each area: <strong>Beginner / Intermediate / Advance </strong>. By default the "Beginner" option will be selected.
    You can change as per your expertise level. <br>
    5.The difficulty level of questions will vary according to the selected expertise level. <br>
    6. More marks are awarded if difficulty level increases.<br>
    7. The test comprises <strong>10 multiple choice questions</strong> from each area, and the duration of the test is
    30 minutes. <strong> Each question will have 4 answers out of which only one answer is correct.</strong><br>
    8. You can submit the test any time during the test, once submitted you will not be allowed to retake the test.<br>
    9.<strong> There will not be any penalty for wrong answers. However accuracy will be taken into
        consideration.</strong> <br>
    10. Do click on the <strong>“Go Full Screen” </strong>button <strong> 30 seconds </strong>of opening the test page
    or else <strong> test will be submitted automatically</strong>. You will not be allowed to re-take the test.
    <strong> questions are compulsory.</strong> <br><br>


    <strong>Pre-requisites:</strong>
    <br>1. Working camera during interview process. The candidate need not manually switch on / off the camera as it
    will be done automatically. <br>
    2. Uninterrupted internet connection preferably more than 10 MBPS including electricity during the test
    process. We are not responsible for any disturbances. <br>
    3.<strong> Google chrome browser</strong><br>


    <br><strong>Do's:</strong> <br>
    1. <strong> all other applications before you start the test.</strong><br>
    2. Do click on the <strong>“Go Full Screen” button within 30 seconds</strong> of opening the test page.<br>
    3. Prepare well before you start the test.<br>
    4. Be confident <br>
    5. Be careful on clicking on the submit button before you want to end the test <br> 6. Keep watching the timer for
    your convenience. <br><br>


    <strong>Don'ts: </strong><br>
    1.Once you start the test don't leave the system until you complete it.<br>
    2. Don't press any key during the test.<br>
    3. Don't refresh the test link once it is started <br>
    4. Don't try to share screen <br>
    5. Once the test is live, minimizing test screen / navigation between tabs is not allowed. <br>If you attempt any of
    the above, your candidature will be
    rejected even if you complete the test and secure good marks. We assume you accept all the above terms and
    conditions to proceed for the test.<br>

    <strong> <br>All the best !!! <br></strong><br>
    The link for test is given below:
    <strong>
        <p>click the link to procede : http://localhost:8080/C_Login</p>
        <p>Your email :{1}</p>
        <p>Your password:{2}</p>
    </strong>

</body>

</html>
    """.format(name, mail, password), subtype='html')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
    return True
