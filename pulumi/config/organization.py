import pulumi

config = pulumi.Config()

aws_organization_id = "o-syu4m3phrj"
aws_organization_root_id = "r-b2xr"

aws_organization_account_name = "freelancer1001"
aws_organization_account_email = f"root-{aws_organization_account_name}@aws.nuage.studio"
aws_organization_account_user = "blabla"