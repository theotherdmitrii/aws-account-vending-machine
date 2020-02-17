from dynamic_providers.workmail.alias import Alias
from pulumi import ComponentResource, ResourceOptions, Input, Output
from pulumi_aws.organizations import Account


class AWSOrganizationAccount(ComponentResource):
    account_id: Output[str]
    """
    ID of the organization account
    """

    workmail_alias: Output
    """
    WorkMail email of the root user
    """

    def __init__(self,
                 name: str,
                 account_unit_id: Input[str],
                 account_name: Input[str],
                 account_email: Input[str],
                 account_access_role_name: Input[str],
                 workmail_org_id: Input[str],
                 workmail_group_id: Input[str],
                 opts: ResourceOptions = None):
        super().__init__("nuage/aws:organizations:AWSOrganizationAccount", name, {}, opts)

        org_account = Account("org-account",
                              name=f"Sandbox account for {account_name}",
                              email=account_email,
                              parent_id=account_unit_id,
                              role_name=account_access_role_name)

        self.workmail_alias = Alias(name="org-account-workmail-alias",
                                    group_id=workmail_group_id,
                                    alias_email=account_email,
                                    organization_id=workmail_org_id)

        self.account_id = org_account.id

        self.register_outputs({})
