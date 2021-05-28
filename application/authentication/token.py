  
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class TokenFactory(PasswordResetTokenGenerator):
    """
    Class used to store the email and token of the new user during the validation process.
    """
    def _make_hash_value(self, user, timestamp):
        return (
            str(user.pk) + str(timestamp) + str(user.is_active)
        )


activation_token = TokenFactory()
