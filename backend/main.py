from flask import Flask, abort, request, Response
from flask_restful import Api, Resource, reqparse, abort
from flask_sqlalchemy import SQLAlchemy

import post_data_validation
import get_data_validation
import functions
import time_functions
import table_functions
import email_sender

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

#database model class
class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    seatNumber = db.Column(db.Integer, nullable=False)
    fullName = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    numberOfSeats= db.Column(db.Integer, nullable=False)
    cancelationKey= db.Column(db.Integer, nullable=True)
    def __repr__(self):
        return f"Reservation(date={self.date}, duration={self.duration}, seatNumber={self.seatNumber}, fullName={self.fullName}, phone={self.phone}, email={self.email}, numberOfSeats={self.numberOfSeats})"

#/reservations endpoint
class Reservations(Resource):
    def post(self):
        #parse json from request
        parser = reqparse.RequestParser()
        parser.add_argument("date", type=str, required=True, help="Date string is required in dd.mm.yyyy HH:MM format")
        parser.add_argument("duration", type=int, required=True, help="Duration is required in minutes")
        parser.add_argument("seatNumber", type=int, required=True, help="Seat number is required")
        parser.add_argument("fullName", type=str, required=True, help="Full name is required")
        parser.add_argument("phone", type=str, required=True, help="Phone number is required")
        parser.add_argument("email", type=str, required=True, help="Email adress is required")
        parser.add_argument("numberOfSeats", type=int, required=True, help="Number of seats is required")
        args = parser.parse_args()
        
        #check if json data is valid
        post_data_validation.abort_if_invalid_data(args)
        #check if seat is free at given time
        post_data_validation.abort_if_unavailable(args, Reservation.query.all())

        #add reservation to database
        reservation = Reservation(date=args.date, duration=args.duration, seatNumber=args.seatNumber, fullName=args.fullName, phone=args.phone, email=args.email, numberOfSeats=args.numberOfSeats)
        
        db.session.add(reservation)
        db.session.commit()
        email_sender.new_res(reservation)
        
        return {"reservationId": str(reservation.id)}, 201
    
    
    def get(self):
        #parse json from request
        parser = reqparse.RequestParser()
        parser.add_argument("date", type=str, required=True, help="Date string is required in dd.mm.yyyy or dd.mm.yyyy HH:MM format")
        args = parser.parse_args()
        
        reservations=Reservation.query.all()
        
        hourGiven = get_data_validation.abort_if_wrong_date_format(args.date)
        output=[]
        for reservation in reservations:
            #if hour given return reservations that start after this time on given day
            if hourGiven and time_functions.is_after(args.date, reservation.date):
                output.append(functions.reservation_dict(reservation))
            #if no hour given then return all reservations on given day        
            elif not hourGiven and args.date==reservation.date.split(" ")[0]: 
                output.append(functions.reservation_dict(reservation))
                
        return {"bookings": output}, 200
   
#/reservations/id endpoint 
class ReservationsId(Resource):
    def put(self, reservation_id):
        parser = reqparse.RequestParser()
        parser.add_argument("status", type=str, required=True, help="Action status is required")
        args=parser.parse_args()
        #validate json
        if args.status!="requested cancelation":
            abort(400, message="Invalid status")
        reservation=Reservation.query.filter_by(id=reservation_id).first()
        if reservation is None:
            abort(404, description="Reservation not found...")
        if time_functions.less_than_two_hours(reservation.date):
            abort(405, description="You cannot delete this reservation anymore...")
            
        if reservation.cancelationKey is None:
            reservation.cancelationKey=functions.generateKey()
        
        
        db.session.add(reservation)
        db.session.commit()
        #send email
        email_sender.request_cancelation(reservation)
        return Response(status=200)
    
    def delete(self, reservation_id):
        args=request.json
        if args is None:
            abort(400, description="Cannot read json")
        if "varificationCode" not in args:
            abort(400, message="Verification code is required")
        if type(args["varificationCode"])!=str:
            abort(400, message="Verification code must be string")
        
        reservation=Reservation.query.filter_by(id=reservation_id).first()
        if reservation is None:
            abort(404, message="Reservation not found...")
        
        if time_functions.less_than_two_hours(reservation.date):
            abort(405, description="You cannot delete this reservation anymore...")
        
        if reservation.cancelationKey==int(args["varificationCode"]):
            email_sender.confirm_cancelation(reservation)
            db.session.delete(reservation)
            db.session.commit()
            return {"message": "yeeet"}, 200
        return {"message": "wrong code"}, 403
    
class Tables(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("status", type=str, required=True, help="Table status is required")
        parser.add_argument("min_seats", type=int, required=True, help="Number of seats is required")
        parser.add_argument("start_date", type=str, required=True, help="Date is required in 'dd.mm.yyyy HH:MM format'")
        parser.add_argument("duration", type=str, required=True, help="Duration in minutes is required")
        args = parser.parse_args()
        
        if args.status not in ("free", "taken", "all"):
            abort(400, description="Wrong status...")
        
        resdt=time_functions.is_date_time_format(args.start_date)
        if not resdt:
            abort(400, description="Invalid date format...")
        
        #get all seats with min_seats
        #check if seat collides with reservations
        reservations=Reservation.query.all()
        taken=table_functions.get_taken_seats_number(reservations, args)
        
        if args.status == "taken":
            return {"tables": table_functions.get_seats_from_list(taken)}
        all=table_functions.get_seats_for_x_people(args.min_seats)
        if args.status == "free":
            free=[x for x in all if x not in taken]
            return {"tables": table_functions.get_seats_from_list(free)}
        if args.status=="all":
            return {"tables": table_functions.get_seats_from_list(all)}
        
           
api.add_resource(Reservations, "/reservations")
api.add_resource(ReservationsId, "/reservations/<int:reservation_id>")
api.add_resource(Tables, "/tables")
    

if __name__ == '__main__':
    app.run(debug=True)
