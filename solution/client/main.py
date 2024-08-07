
import commands.category as categories
import commands.users as users
import commands.orders as orders
from storage import TokenStorage


def welcome_prompt():
    token = TokenStorage.get_token()
    if not token:
        print('Hello, please [L]ogin or [R]egister')
        choice = input().upper()
        if choice == 'L':
            users.login()
        elif choice == 'R':
            users.register()
        else:
            welcome_prompt()  # you must login!
    else:
        print('Hello, ', end='')
        users.info(token)


def main():
    welcome_prompt()
    print('Commands = [C]ategories / [P]roducts / [U]sers / [O]rders')
    choice = input().upper()

    if choice == 'C':
        categories.select_action()
    if choice == 'P':
        raise NotImplementedError()
    if choice == 'U':
        users.select_action()
    if choice == 'O':
        orders.select_action()


if __name__ == '__main__':
    main()
