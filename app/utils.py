import secrets
import string

# Вспомогательные функции
def generate_short_id(length: int = 6) -> str:
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))