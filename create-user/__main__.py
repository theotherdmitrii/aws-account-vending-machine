import pulumi
import pulumi_aws as aws
import src.pgp_util as pgp
from pulumi_aws import iam

config = pulumi.Config()

#  Input args
aws_organization_account_id = ''
aws_organization_account_name = ''
aws_organization_account_user = ''
pgp_pub_key_path = ''

# Constants
aws_organization_account_pass_length = 16
aws_organization_role_name = 'NuageAccessRole'
aws_organization_role_arn = f"arn:aws:iam::{aws_organization_account_id}:role/{aws_organization_role_name}"

aws_organization_account_pgp_base64 = pgp.b64text(pgp_pub_key_path)

provider = aws.Provider("privileged",
                        assume_role={
                            "role_arn": aws_organization_role_arn
                        })

freelancer = iam.User("freelancer-user",
                      name=f"{aws_organization_account_name}-{aws_organization_account_user}",
                      opts=pulumi.ResourceOptions(
                          provider=provider
                      ))

freelancer_login_profile = iam.UserLoginProfile("freelancer-login-profile",
                                                user=freelancer.name,
                                                password_reset_required=True,
                                                password_length=aws_organization_account_pass_length,
                                                pgp_key=aws_organization_account_pgp_base64,
                                                opts=pulumi.ResourceOptions(
                                                    provider=provider
                                                ))

pulumi.export("user_name", freelancer.name)
pulumi.export("user_encrypted_password", freelancer_login_profile.encrypted_password)
pulumi.export("user_url", f"https://{aws_organization_account_id}.signin.aws.amazon.com/console")
