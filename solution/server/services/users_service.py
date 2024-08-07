from data.database import insert_query, read_query
from data.models import Order, Role, User
from mariadb import IntegrityError


_SEPARATOR = ';'

# passwords should be secured as hashstrings in DB
# def _hash_password(password: str):
#     from hashlib import sha256
#     return sha256(password.encode('utf-8')).hexdigest()


def find_by_username(username: str) -> User | None:
    data = read_query(
        'SELECT id, username, password, role FROM users WHERE username = ?',
        (username,))

    return next((User.from_query_result(*row) for row in data), None)


def try_login(username: str, password: str) -> User | None:
    user = find_by_username(username)

    # password = _hash_password(password)
    return user if user and user.password == password else None


def create(username: str, password: str) -> User | None:
    # password = _hash_password(password)
    try:
        generated_id = insert_query(
            'INSERT INTO users(username, password, role) VALUES (?,?,?)',
            (username, password, Role.CUSTOMER))

        return User(id=generated_id, username=username, password='', role=Role.CUSTOMER)

    except IntegrityError:
        # mariadb raises this error when a constraint is violated
        # in that case we have duplicate usernames
        return None


def create_token(user: User) -> str:
    # note: this token is not particulary secure, use JWT for real-world uses
    return f'{user.id}{_SEPARATOR}{user.username}'


def is_authenticated(token: str) -> bool:
    if token:
        return any(read_query(
        'SELECT 1 FROM users where id = ? and username = ?',
        # note: this token is not particulary secure, use JWT for real-world user
        token.split(_SEPARATOR)))


def from_token(token: str) -> User | None:
    _, username = token.split(_SEPARATOR)

    return find_by_username(username)


def owns_order(user: User, order: Order) -> bool:
    return order.user_id == user.id
