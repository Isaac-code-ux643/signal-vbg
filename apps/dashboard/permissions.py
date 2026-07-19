from django.contrib.auth.decorators import user_passes_test


def is_coordinator_or_admin(user):
    return user.is_authenticated and user.role in ('coordinator', 'admin')


coordinator_required = user_passes_test(
    is_coordinator_or_admin,
    login_url='accounts:login'
)
