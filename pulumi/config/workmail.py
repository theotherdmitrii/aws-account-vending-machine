import pulumi

config = pulumi.Config()

workmail_organization_id = config.get('workmail_organization_id')
workmail_domain = config.get('sub_domain')
workmail_alias_name = config.get('alias_name')

workmail_group_name = config.get('workmail_group_name')
workmail_group_email = config.get('workmail_group_email')
