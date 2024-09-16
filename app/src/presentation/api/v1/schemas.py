from sqlalchemy import Enum


class WebhookType(Enum):
    incomingPayment = "incomingPayment"
    outgoingPayment = "outgoingPayment"
    incomingSbpPayment = "incomingSbpPayment"
    acquiringInternetPayment = "acquiringInternetPayment"
