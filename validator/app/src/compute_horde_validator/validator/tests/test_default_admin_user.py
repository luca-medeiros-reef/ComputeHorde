import pytest
from django.conf import settings
from django.contrib.auth.models import User

from compute_horde_validator.validator.apps import maybe_create_default_admin


@pytest.mark.asyncio
@pytest.mark.django_db
def test__maybe_create_default_admin__missing_envvar():
    settings.DEFAULT_ADMIN_PASSWORD = None
    assert not User.objects.filter(is_superuser=True).exists()

    # should not create superuser
    maybe_create_default_admin(sender=None)
    assert not User.objects.filter(is_superuser=True).exists()


@pytest.mark.asyncio
@pytest.mark.django_db
def test__maybe_create_default_admin__create_superuser():
    settings.DEFAULT_ADMIN_PASSWORD = "test"
    assert not User.objects.filter(is_superuser=True).exists()

    # should create superuser
    maybe_create_default_admin(sender=None)
    assert User.objects.filter(is_superuser=True).exists()
    assert User.objects.filter(is_superuser=True).count() == 1


@pytest.mark.asyncio
@pytest.mark.django_db
def test__maybe_create_default_admin__user_exists():
    created_user = User.objects.create_superuser(
        username="admin", email="test@admin.com", password="test"
    )
    assert User.objects.filter(is_superuser=True).exists()

    # should not create another superuser
    maybe_create_default_admin(sender=None)
    assert User.objects.filter(is_superuser=True).count() == 1
    assert User.objects.get(is_superuser=True) == created_user
