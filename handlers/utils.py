from json import load, dump

def load_users():
    # try:
    #     with open('users.json', 'r', encoding='utf-8') as f:
    #         return load(f)
    # except FileNotFoundError:
    #     return []
    f = open('users.json',)
    return load(f)

def save_users(users):
    with open('users.json', 'w', encoding='utf-8') as f:
        dump(users, f, indent=4, ensure_ascii=False)
