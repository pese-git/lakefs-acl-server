# Группы
from app.schemas.group import GroupCreate
from app.schemas.policy import PolicyCreate
from app.schemas.user import UserCreate
from app.services.group_service import GroupService
from app.services.policy_service import PolicyService
from app.services.user_service import UserService


def init_default_groups_and_policies(db):
    print("## init_default_groups_and_policies")
    user_service = UserService(db)
    group_service = GroupService(db)
    policy_service = PolicyService(db)

    DEFAULT_USERS = [
        # {"username": "admin", "email": "admin@lakefs-acl.com"},
    ]

    DEFAULT_GROUPS = [
        {"name": "Admins"},
        {"name": "Supers"},
        {"name": "Writers"},
        {"name": "Readers"},
    ]

    DEFAULT_POLICIES = [
        {"name": "AdminPolicy", "document": '{"effect": "allow", "actions": ["*"]}'},
        {"name": "SuperPolicy", "document": '{"effect": "allow", "actions": ["*"]}'},
        {"name": "WritePolicy", "document": '{"effect": "allow", "actions": ["write"]}'},
        {"name": "ReadPolicy", "document": '{"effect": "allow", "actions": ["read"]}'},
    ]

    for user in DEFAULT_USERS:
        try:
            user_service.create_user(
                UserCreate.model_construct(username=user["username"], email=user["email"])
            )
        except Exception as e:
            print(f"Failed to create user {user['name']}: {e}")

    for group in DEFAULT_GROUPS:
        try:
            group_service.create_group(GroupCreate.model_construct(name=group["name"]))
        except Exception as e:
            print(f"Failed to create group {group['name']}: {e}")

    for policy in DEFAULT_POLICIES:
        try:
            policy_service.create_policy(
                PolicyCreate.model_construct(name=policy["name"], document=policy["name"])
            )
        except Exception:
            pass  # уже есть
