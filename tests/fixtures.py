from creatder.models import User, Creature, Review


# Design Pattern: Factory
def gen_user(
        name="John",
        login="Doe",
        email="john@doe.test.com",
        password="P@ssw0rd!",
        about_myself="I like pizza, movies and hanging out with friends"
    ):
    user = User(
        name=name,
        login=login,
        email=email,
        about_myself=about_myself
    )
    user.set_password(password)
    return user


def gen_creature(
        name='Pig',
        age='5',
        sex='Male',
        breed='Other',
        color_pattern='Mix',
        crossed_rainbow_bridge=False,
        owner='user'
    ):
    creature = Creature(
        name=name,
        age=age,
        sex=sex,
        breed=breed,
        color_pattern=color_pattern,
        crossed_rainbow_bridge=crossed_rainbow_bridge,
        owner=owner
    )
    creature.save()
    return creature
