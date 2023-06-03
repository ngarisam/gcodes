from social_core.pipeline.user import create_user


def update_username(strategy, details, user=None, *args, **kwargs):
    if user:
        first_name = details.get('first_name')
        last_name = details.get('last_name')
        if first_name and last_name:
            user.first_name = first_name
            user.last_name = last_name
            user.username = f"{first_name} {last_name}"
            user.save()

    return {
        'user': user,
        'is_new': user is not None
    }


# Add the function to the pipeline
SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'your_project.pipeline.update_username',  # Replace 'your_project' with your project's name
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)