import pulumi
import pulumi_aws as aws
from pulumi_aws import iam

config = pulumi.Config()

aws_organization_account_name = "freelancer1001"
aws_organization_account_user = "developer"
aws_organization_role_name = "NuageAccessRole"

provider = aws.Provider("privileged",
                        assume_role={
                            "role_arn": aws_organization_role_name,
                            "session_name": "PulumiSession",
                            "external_id": "PulumiApplication",
                        },
                        region=aws.config.requireRegion())

freelancer = iam.User("freelancer-user", name=f"{aws_organization_account_name}-{aws_organization_account_user}")

freelancer_login_profile = iam.UserLoginProfile("freelancer-login-profile",
                                                password_reset_required=True,
                                                password_length=8,
                                                user=freelancer.name)
