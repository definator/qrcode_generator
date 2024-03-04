import random

def create_link(username, template):
    username_template = "[USERNAME]"
    if username_template in template:
        return template.replace(username_template, username)

def generate(base_tuples):
    usernames = base_tuples[0]
    categories = base_tuples[1]
    templates = base_tuples[2]
    username = random.choice(usernames)
    category = random.choice(categories)
    for template in templates:
        print(template.strip())
        print(category.strip())
        print(category in template)
        if category.strip() in template.strip():
            return create_link(username, template)
        else:
            create_link(username, "https://telegram.com/users/[USERNAME]")


# category = categories.get_random_category()