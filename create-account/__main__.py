from pulumi import export, Config
from pulumi_aws import organizations as org

config = Config()

organization_root_id = config.require("aws_organization_root_id")
spoke_account_access_role_name = config.require("spoke_account_access_role_name")
spoke_account_name = config.require("spoke_account_name")

# Constants
spoke_account_email = f"root-{spoke_account_name}@aws.nuage.studio"

# AWS Organizations part of the story
spoke_account_unit = org.OrganizationalUnit("spoke-accounts-unit",
                                            name="Freelancer accounts",
                                            parent_id=organization_root_id)

spoke_account = org.Account("spoke-account",
                            name=f"Sandbox account for {spoke_account_name}",
                            email=spoke_account_email,
                            parent_id=spoke_account_unit.id,
                            role_name=spoke_account_access_role_name)

export("spoke_account_id", spoke_account.id)
export("spoke_account_access_role", spoke_account.role_name)
