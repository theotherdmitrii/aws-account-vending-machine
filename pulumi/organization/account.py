from pulumi import ComponentResource, ResourceOptions, Input, Output
from pulumi_aws.organizations import Account
from dynamic_providers.workmail.alias import Alias


class AWSOrganizationAccountArgs:
    org_account_unit_id: Input[str]
    """
    Organization unit ID to create account units and attach organization accounts
    """

    org_account_name: Input[str]
    """
    """

    org_account_email: Input[str]
    """
    """

    org_account_access_role_name: Input[str]
    """
    """

    workmail_org_id: Input[str]
    """
    """

    workmail_group_id: Input[str]
    """
    """

    def __init__(self, org_account_unit_id=None, org_account_name=None, org_account_email=None,
                 org_account_access_role_name=None, workmail_org_id=None, workmail_group_id=None):
        self.org_account_unit_id = org_account_unit_id
        self.org_account_name = org_account_name
        self.org_account_email = org_account_email
        self.org_account_access_role_name = org_account_access_role_name
        self.workmail_org_id = workmail_org_id
        self.workmail_group_id = workmail_group_id


class AWSOrganizationAccount(ComponentResource):
    account_id: Output[str]
    """
    """

    workmail_alias: Output
    """
    """

    def __init__(self,
                 name: str,
                 args: AWSOrganizationAccountArgs,
                 opts: ResourceOptions = None):
        super().__init__("nuage/aws:organizations:AWSOrganizationAccount", name, {}, opts)

        org_account = Account("org-account",
                              name=f"Sandbox account for {args.org_account_name}",
                              email=args.org_account_email,
                              parent_id=args.org_account_unit_id,
                              role_name=args.org_account_access_role_name)

        self.workmail_alias = Alias(name="org-account-workmail-alias",
                                    group_id=args.workmail_group_id,
                                    alias_email=args.org_account_email,
                                    organization_id=args.workmail_org_id)

        self.account_id = org_account.id

        self.register_outputs({})
