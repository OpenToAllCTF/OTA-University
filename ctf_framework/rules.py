import rules

@rules.predicate
def is_staff(user):
    return user.is_staff

@rules.predicate
def is_own_profile(user, profile):
    return user.id == profile.user.id

@rules.predicate
def has_solved_challenge(user, challenge):
    solves = user.UserProfile.solves
    return challenge.id in [solve.challenge.id for solve in solves]

@rules.predicate
def is_own_writeup(user, writeup):
    return writeup.id in [writeup.id for writeup in user.UserProfile.writeup_set.all()]

@rules.predicate
def is_challenge_author(user, challenge):
    return challenge.author.user == user

# Add permissions
## Profiles
rules.add_perm('update_profile', is_staff | is_own_profile)

## Writeups
rules.add_perm('read_writeups_for_challenge', has_solved_challenge | is_challenge_author)
rules.add_perm('create_writeup', has_solved_challenge | is_challenge_author)
rules.add_perm('update_writeup', is_own_writeup)

## Challenges
rules.add_perm('create_challenge', is_staff)
rules.add_perm('update_challenge', is_staff)
rules.add_perm('delete_challenge', is_staff)

## Categories
rules.add_perm('manage_categories', is_staff)

## Titles
rules.add_perm('manage_titles', is_staff)
