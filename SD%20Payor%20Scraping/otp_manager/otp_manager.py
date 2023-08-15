import pyotp
secret_key = "ROAA4XIT5XFH2SXE"

def get_totp():
    totp = pyotp.TOTP(secret_key)
    return totp.now()