import pandas as pd
df = pd.read_csv("hotels.csv", dtype={"id": str})
df_cards = pd.read_csv("cards.csv", dtype= str).to_dict(orient="records")
df_cards_security = pd.read_csv("card_security.csv", dtype=str)

class Hotel:
    def __init__(self, hotel_id):
        self.hotel_id = hotel_id
        self.name = df.loc[df["id"] == self.hotel_id, "name"].squeeze()


    def book(self):
        """Book the hotel by changing its availability to no"""
        df.loc[df["id"] == self.hotel_id, "available"] = "no"
        df.to_csv("hotels.csv", index=False)

    def available(self):
        """Check if the hotel is available or not"""
        avaliablity = df.loc[df["id"] == self.hotel_id, "available"].squeeze()
        if avaliablity == 'yes':
            return True
        else:
            return False
        

    @classmethod   
    def get_hotel_count(cls, data):
        return len(data)


class ReservationTicket:
    def __init__(self, customer_name, hotel_object):
        self.customer_name = customer_name
        self.hotel = hotel_object

    def generate(self):
        content = f"""
        Reservation Ticket
        -------------------
        Customer Name: {self.customer_name}
        Hotel Name: {self.hotel.name}
        """
        return content
    
    @property
    def the_customer_name(self):
        return self.customer_name.strip().title()
    
    @staticmethod
    def convert(amount):
        return amount * 0.84


class CreditCard:
    def __init__(self, card_number):
        self.card_number = card_number

    def validate(self, expiration, holder, cvc):
       card_data = {"number": self.card_number, "expiration": expiration, "holder": holder, "cvc": cvc}
       if card_data in df_cards:
            return True
       else:
            return False
       

class SecureCreditCard(CreditCard):
    def authenticate(self, given_password):
        password = df_cards_security.loc[df_cards_security["number"] == self.card_number, "password"].squeeze()
        if given_password == password:
            return True
        else:
            return False
        

print(df)
hotel_ID = input("Enter the hotel id: ")
hotel = Hotel(hotel_ID)

if hotel.available():
    credit_card = SecureCreditCard(card_number="1234567890123456")
    if credit_card.validate(expiration="12/26", holder="JOHN SMITH", cvc="123"):
        if credit_card.authenticate(given_password="mypass"):
            hotel.book()
            name = input("Enter your name: ")
            reservation_ticket = ReservationTicket(name, hotel)
            print(reservation_ticket.generate())
        else:
            print("There was an issue with the password")
    else:
        print("There was an issue with the credit card")

else:
    print("Hotel is not available")
