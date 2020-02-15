import pulumi
import password
from config import org_id, org_account_name, org_account_email, org_account_access_role_name, org_account_username, \
    workmail_org_id, workmail_group_email
from dynamic_providers.workmail.group import Group
from organization.account import AWSOrganizationAccount, AWSOrganizationAccountArgs
from organization.account_user import AWSOrganizationAccountUser, AWSOrganizationAccountUserArgs
from pulumi_aws.organizations import Organization, OrganizationalUnit


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
                                         account_unit_id=org_account_unit.id,
                                         account_name=org_account_name,
                                         account_email=org_account_email,
                                         account_access_role_name=org_account_access_role_name,
                                         workmail_org_id=workmail_org_id,
                                         workmail_group_id=workmail_group.group_id
                                     ))

org_user = AWSOrganizationAccountUser("org-account-user",
                                      args=AWSOrganizationAccountUserArgs(
                                          account_id=org_account.account_id,
                                          account_name=org_account_name,
                                          access_role_name=org_account_access_role_name,
                                          username=org_account_username,
                                          password=password.generate(16),
                                          user_policy_arn="arn:aws:iam::aws:policy/AdministratorAccess"
                                      ))

pulumi.export("console_url", org_user.console_url)
pulumi.export("username", org_user.username)
pulumi.export("password", org_user.password)
