import smtplib

from email.message import EmailMessage

def send_email(content, subject, fromm, mail):
    s=smtplib.SMTP(host='smtp.ethereal.email', port=587)
    s.starttls()
    s.login("charity.marquardt69@ethereal.email", "Njg738P7fcmC6vvjcW")
    msg = EmailMessage()
    
    msg.set_content(content)
    msg['Subject'] = subject
    msg['From'] = fromm
    msg['To'] = mail
    
    s.send_message(msg)
    s.quit()

def new_res_message(reservation):
    lines={"Reservation ID: ": reservation.id,
            "Date: ": reservation.date, 
            "Duration: ": reservation.duration, 
            "Seat Number: ": reservation.seatNumber, 
            "Full name: ": reservation.fullName, 
            "Phone number: ": reservation.phone, 
            "Email adress: ": reservation.email, 
            "Number of seats: ": reservation.numberOfSeats}
    output=""
    for k,v in lines.items():
        output=output + k + str(v) + "\n"
    return output
    
def new_res(reservation):
    content="We have received your reservation!\n\n"+new_res_message(reservation)
    subject='New Reservation'
    fromm='Solvro <new_reservation@solvro.com>'
    to=reservation.email
    
    send_email(content, subject, fromm, to)
    
def request_cancelation_message(reservation):
    lines={"Reservation ID: ": reservation.id,
           "Cancelation key: ": reservation.cancelationKey}
    output=""
    for k,v in lines.items():
        output=output + k + str(v) + "\n"
    return output
    
def request_cancelation(reservation):
    content="We can see that you would like to cancel your reservation :(\n\n"+request_cancelation_message(reservation)
    subject="Requested cancelation"
    fromm='Solvro <requested_cancelation@solvro.com>'
    to=reservation.email
    
    send_email(content, subject, fromm, to)
    
def confirm_cancelation(reservation):
    content="You have successfully canceled your reservation.\n"
    subject=f"Reservation {reservation.id} Cancelled"
    fromm='Solvro <cancelled@solvro.com>'
    to=reservation.email
    
    send_email(content, subject, fromm, to)
    