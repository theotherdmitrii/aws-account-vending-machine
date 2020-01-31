from config.workmail import workmail_organization_id, workmail_domain, workmail_alias_name, workmail_group_name, \
    workmail_group_email
from dynamic_providers.workmail.alias import Alias
from dynamic_providers.workmail.group import Group
from pulumi import export, Config

config = Config()

group = Group(name="WorkMailGroupCreation", organization_id=workmail_organization_id,
              group_name=workmail_group_name, group_email=workmail_group_email)

export("group_export_group_id", group.group_id)

alias_email = f"root-{workmail_alias_name}@{workmail_domain}"
alias = Alias(name="WorkMailAliasCreation", group_id=group.group_id,
              alias_email=alias_email, organization_id=workmail_organization_id)

export("alias_export_alias_email", alias.alias_email)
export("alias_export_group_id", alias.group_id)
