import pulumi
import pulumi_aws as aws
import src.pgp_util as pgp
from pulumi_aws import iam

config = pulumi.Config()

# Input args
spoke_account_id = config.require("spoke_account_id")
spoke_account_name = config.require("spoke_account_name")
spoke_account_username = config.require("spoke_account_username")
spoke_account_access_role_name = config.require("spoke_account_access_role_name")
pgp_pub_key_path = config.require("pgp_pub_key_path")

# Constants
spoke_account_user_pass_length = 8
aws_organization_role_arn = f"arn:aws:iam::{spoke_account_id}:role/{spoke_account_access_role_name}"

aws_organization_account_pgp_base64 = pgp.b64text(pgp_pub_key_path)

spoke_account_provider = aws.Provider("spoke-account-provider",
                                      assume_role={
                                          "role_arn": aws_organization_role_arn
                                      })

spoke_account_user = iam.User("spoke-account-user",
                              name=f"{spoke_account_name}-{spoke_account_username}",
                              opts=pulumi.ResourceOptions(
                                  provider=spoke_account_provider
                              ))

spoke_account_user_login_profile = iam.UserLoginProfile("spoke-account-user-login-profile",
                                                        user=spoke_account_user.name,
                                                        password_reset_required=True,
                                                        password_length=spoke_account_user_pass_length,
                                                        pgp_key=aws_organization_account_pgp_base64,
                                                        opts=pulumi.ResourceOptions(
                                                            provider=spoke_account_provider
                                                        ))

spoke_account_admin_policy_attachment = iam.UserPolicyAttachment("spoke-account-user_AdministratorAccessRole",
                                                                 policy_arn="arn:aws:iam::aws:policy/AdministratorAccess",
                                                                 user=spoke_account_user.name,
                                                                 opts=pulumi.ResourceOptions(
                                                                     provider=spoke_account_provider
                                                                 ))

pulumi.export("spoke_account_username", spoke_account_user.name)
pulumi.export("spoke_account_encrypted_password", spoke_account_user_login_profile.encrypted_password)
pulumi.export("spoke_account_url", f"https://{spoke_account_id}.signin.aws.amazon.com/console")
