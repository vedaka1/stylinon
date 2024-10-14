from sqlalchemy import Enum


class AcquiringWebhookType(Enum):
    incomingPayment = "incomingPayment"
    outgoingPayment = "outgoingPayment"
    incomingSbpPayment = "incomingSbpPayment"
    acquiringInternetPayment = "acquiringInternetPayment"
