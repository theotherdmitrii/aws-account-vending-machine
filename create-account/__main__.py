from pulumi import export, Config
from pulumi_aws import organizations as org

config = Config()

aws_organization_root_id = "r-b2xr"
aws_organization_role_name = "NuageAccessRole"
aws_organization_account_name = "freelancer1001"
# aws_organization_account_email = f"root-{aws_organization_account_name}@aws.nuage.studio"
aws_organization_account_email = "dmitrii.hundred.o.one@gmail.com"

# AWS Organizations part of the story
freelancer_account_unit = org.OrganizationalUnit("freelancer-accounts-unit",
                                                 name="Freelancer accounts",
                                                 parent_id=aws_organization_root_id)

freelancer_account = org.Account("freelancer-account",
                                 name=f"Sandbox account for {aws_organization_account_name}",
                                 email=aws_organization_account_email,
                                 parent_id=freelancer_account_unit.id,
                                 role_name=aws_organization_role_name)

export("freelancer_account_arn", freelancer_account.arn)
export("freelancer_account_role", freelancer_account.role_name)
