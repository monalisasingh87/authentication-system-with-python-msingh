from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column,relationship

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    #relationships
    #invoice_list: Mapped[list["Invoice"]]= relationship(back_populates='user')


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
class Invoice(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    invoice_date: Mapped[str] = mapped_column(String(120), nullable=False)
    invoice_number: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    invoice_amount: Mapped[float] = mapped_column(Float(), nullable=False)

    #realtionship
    #user_id: Mapped[int]= mapped_column(ForeignKey("user.id"))
    #invoice_list: Mapped["User"]= relationship(back_populates='invoice_list')


def serialize(self):
        return {
            "invoice_date": self.invoice_date,
            "invoice_number": self.invoice_number,
            "invoice_amount": self.invoice_amount
            }