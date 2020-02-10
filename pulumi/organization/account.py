from dynamic_providers.workmail.alias import Alias
from pulumi import ComponentResource, ResourceOptions, Input, Output
from pulumi_aws.organizations import Account


class AWSOrganizationAccountArgs:
    account_unit_id: Input[str]
    """
    Organization unit ID to create account units and attach organization accounts
    """

    account_name: Input[str]
    """
    Common name for all users under the account
    """

    account_email: Input[str]
    """
    Root email for the account
    """

    account_access_role_name: Input[str]
    """
    Assume role name for the account
    """

    workmail_org_id: Input[str]
    """
    WorkMail organization id to create account Alias
    """

    workmail_group_id: Input[str]
    """
    WorkMail organization group id to create account Alias
    """

    def __init__(self, account_unit_id: Input[str] = None,
                 account_name: Input[str] = None,
                 account_email: Input[str] = None,
                 account_access_role_name: Input[str] = None,
                 workmail_org_id: Input[str] = None,
                 workmail_group_id: Input[str] = None):
        self.account_unit_id = account_unit_id
        self.account_name = account_name
        self.account_email = account_email
        self.account_access_role_name = account_access_role_name
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
                              name=f"Sandbox account for {args.account_name}",
                              email=args.account_email,
                              parent_id=args.account_unit_id,
                              role_name=args.account_access_role_name)

        self.workmail_alias = Alias(name="org-account-workmail-alias",
                                    group_id=args.workmail_group_id,
                                    alias_email=args.account_email,
                                    organization_id=args.workmail_org_id)

        self.account_id = org_account.id

        self.register_outputs({})
