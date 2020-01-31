# from config.workmail import workmail_organization_id, workmail_domain, workmail_alias_name, workmail_group_name, \
#     workmail_group_email
# from dynamic_providers.workmail.alias import Alias
# from dynamic_providers.workmail.group import Group
from config.organization import aws_organization_root_id, aws_organization_account_name, \
    aws_organization_account_email
from pulumi import Config, export
from pulumi_aws import organizations as org, iam

config = Config()

# # Workmail part of the story
# group = Group(name="WorkMailGroupCreation", organization_id=workmail_organization_id,
#               group_name=workmail_group_name, group_email=workmail_group_email)
#
# export("group_export_group_id", group.group_id)
#
# alias_email = f"root-{workmail_alias_name}@{workmail_domain}"
# alias = Alias(name="WorkMailAliasCreation", group_id=group.group_id,
#               alias_email=alias_email, organization_id=workmail_organization_id)
#
# export("alias_export_alias_email", alias.alias_email)
# export("alias_export_group_id", alias.group_id)


# AWS Organizations part of the story
freelancer_account_unit = org.OrganizationalUnit("freelancer-accounts-unit",
                                                 name="Freelancer accounts",
                                                 parent_id=aws_organization_root_id)

freelancer_account = org.Account("freelancer-account",
                                 name=f"Sandbox account for {aws_organization_account_name}",
                                 email=aws_organization_account_email,
                                 parent_id=aws_organization_root_id,
                                 # role_name=
                                 )

freelancer = iam.User("freelancer-user", name=f"{aws_organization_account_name}-{aws_organization_account_user}")

freelancer_login_profile = iam.UserLoginProfile("freelancer-login-profile",
                                                password_reset_required=True,
                                                password_length=8,
                                                user=freelancer.name)

# TODO
export("user_name", freelancer.name)
export("user_password", freelancer.name)
export("user_password", freelancer_login_profile)