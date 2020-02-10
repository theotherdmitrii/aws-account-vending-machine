import pulumi
import src.pgp_util as pgp
from pulumi import Config
from pulumi_aws.organizations import Organization, OrganizationalUnit
from src.dynamic_providers.workmail.group import Group
from src.organization.account import AWSOrganizationAccount, AWSOrganizationAccountArgs
from src.organization.account_user import AWSOrganizationAccountUser, AWSOrganizationAccountUserArgs

config = Config()

# Inputs
org_id = config.require("org_id")
org_account_name = config.require("org_account_name")
org_account_email = config.require("org_account_email")
org_account_access_role_name = config.require("org_account_access_role_name")
org_account_username = config.require("org_account_username")
org_account_userpass_length = config.require("org_account_userpass_length")
org_account_userpass_encryption_pub_key = config.require("org_account_userpass_encryption_pub_key")
org_account_userpass_encryption_pub_key_base64 = pgp.b64text(org_account_userpass_encryption_pub_key)

workmail_org_id = config.require("workmail_org_id")
workmail_group_email = config.require("workmail_group_email")

org = Organization("Nuage",
                   opts=pulumi.ResourceOptions(
                       import_=org_id
                   ))

org_account_unit = OrganizationalUnit(f"Nuage-unit",
                                      name="Freelancer accounts",
                                      parent_id=org.roots[0]["id"])

workmail_group = Group(name="freelancer-emails",
                       organization_id=workmail_org_id,
                       group_name='freelancer-emails',
                       group_email=workmail_group_email)

org_account = AWSOrganizationAccount("Nuage-account",
                                     args=AWSOrganizationAccountArgs(
                                         org_account_unit_id=org_account_unit.id,
                                         org_account_name=org_account_name,
                                         org_account_email=org_account_email,
                                         org_account_access_role_name=org_account_access_role_name,
                                         workmail_org_id=workmail_org_id,
                                         workmail_group_id=workmail_group.group_id
                                     ))

org_user = AWSOrganizationAccountUser("org-account-user",
                                      args=AWSOrganizationAccountUserArgs(
                                          account_id=org_account.account_id,
                                          account_name=org_account_name,
                                          access_role_name=org_account_access_role_name,
                                          username=org_account_username,
                                          user_policy_arn="arn:aws:iam::aws:policy/AdministratorAccess",
                                          password_length=org_account_userpass_length,
                                          password_encryption_pub_key=org_account_userpass_encryption_pub_key_base64
                                      ))

pulumi.export("console_url", org_user.console_url)
pulumi.export("username", org_user.username)
pulumi.export("encrypted_password", org_user.encrypted_password)
