from pulumi import export, Config, get_stack

from dynamic_providers.workmail.group import Group

from dynamic_providers.workmail.alias import Alias
from pulumi.runtime import get_root_resource

config = Config()

group = Group(name="WorkMailGroupCreation", organization_id='m-b01addc6667743b0b865f62342b5a217',
              group_name='AWSFreelancersRoot')

export("group_export_group_id", group.group_id)

""" This method would give a exception if you don't enable the group that you have create that needs to be done manually
    as in boto3 or aws api there is no way to enable a group """

alias_email = 'root-' + config.get('alias_name') + '@' + config.get('sub_domain')
alias = Alias(name="WorkMailAliasCreation", group_id=group.group_id,
              alias_email=alias_email)
export("alias_export_alias_email", alias.alias_email)
export("alias_export_group_id", alias.group_id)
