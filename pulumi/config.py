from pulumi import Config

config = Config()

# Inputs
org_id = config.require("org_id")
org_account_name = config.require("org_account_name")
org_account_email = config.require("org_account_email")
org_account_access_role_name = config.require("org_account_access_role_name")
org_account_username = config.require("org_account_username")

workmail_org_id = config.require("workmail_org_id")
workmail_group_email = config.require("workmail_group_email")