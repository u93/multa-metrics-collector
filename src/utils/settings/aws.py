import os

USERS_TABLE_NAME = (os.environ.get("USERS_TABLE_NAME"),)
ORGANIZATIONS_TABLE_NAME = os.environ.get("ORGANIZATIONS_TABLE_NAME")
PLANS_TABLE_NAME = os.environ.get("PLANS_TABLE_NAME")
ROLES_TABLE_NAME = os.environ.get("ROLES_TABLE_NAME")
