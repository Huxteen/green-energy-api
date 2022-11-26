from rest_framework.exceptions import APIException


class TransactionValidatedAlready(APIException):
    status_code = 400
    default_detail = "Transaction has already been validated."
    default_code = "transaction_validated_already"
