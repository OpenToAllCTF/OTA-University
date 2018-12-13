import rules

@rules.predicate
def is_staff(user):
    return user.is_staff

@rules.predicate
def is_own_profile(user, target_user_profile):
    return user == target_user_profile.id

# Add rules
rules.add_rule('is_staff', is_staff)
rules.add_rule('is_own_profile', is_staff)

# Add permissions
rules.add_perm('edit_profile', is_staff | is_own_profile)
