import pulumi
import pulumi_aws as aws
import src.pgp_util as pgp
from pulumi import Config
from pulumi_aws import iam
from pulumi_aws import organizations as org

config = Config()

# Inputs
organization_root_id = config.require("aws_organization_root_id")
pgp_pub_key_path = config.require("pgp_pub_key_path")
spoke_account_name = config.require("spoke_account_name")
spoke_account_username = config.require("spoke_account_username")
spoke_account_access_role_name = config.require("spoke_account_access_role_name")
spoke_account_user_pass_length = 8

aws_organization_account_pgp_base64 = pgp.b64text(pgp_pub_key_path)


class CreateUserOutput:
    """
    DTO to handle outputs of user creation procedure
    """

    console_url: pulumi.Output[str]
    """
    Url to login to AWS console
    """

    username: pulumi.Output[str]
    """
    Username to login to the console
    """

    encrypted_password: pulumi.Output[str]
    """
    Encrypted password to login to the console
    """

    def __init__(self, console_url: pulumi.Output[str], username: pulumi.Output[str],
                 encrypted_password: pulumi.Output[str]):
        self.console_url = console_url
        self.username = username
        self.encrypted_password = encrypted_password


def create_user(account_id, user_policy_arn: str = "arn:aws:iam::aws:policy/AdministratorAccess"):
    """
    Creates a User within provided account with provided policy assigned

    :param account_id:
    :param user_policy_arn:
    :return:
    """

    aws_organization_role_arn = f"arn:aws:iam::{account_id}:role/{spoke_account_access_role_name}"

    account_provider = aws.Provider("spoke-account-provider",
                                    assume_role={
                                        "role_arn": aws_organization_role_arn
                                    })

    account_user = iam.User("spoke-account-user",
                            name=f"{spoke_account_name}-{spoke_account_username}",
                            opts=pulumi.ResourceOptions(
                                provider=account_provider
                            ))

    account_user_login_profile = iam.UserLoginProfile("spoke-account-user-login-profile",
                                                      user=account_user.name,
                                                      password_reset_required=True,
                                                      password_length=spoke_account_user_pass_length,
                                                      pgp_key=aws_organization_account_pgp_base64,
                                                      opts=pulumi.ResourceOptions(
                                                          provider=account_provider
                                                      ))

    account_user_policy_attachment = iam.UserPolicyAttachment("spoke-account-user_UserAccessRole",
                                                              policy_arn=user_policy_arn,
                                                              user=account_user.name,
                                                              opts=pulumi.ResourceOptions(
                                                                  provider=account_provider
                                                              ))

    return CreateUserOutput(
        console_url=pulumi.Output.from_input(f"https://{account_id}.signin.aws.amazon.com/console"),
        username=account_user.name,
        encrypted_password=account_user_login_profile.encrypted_password
    )


def create_spoke_account():
    """
    Creates Spoke account
    :return:
    """
    spoke_account_email = f"root-{spoke_account_name}@aws.nuage.studio"

    spoke_account_unit = org.OrganizationalUnit("spoke-accounts-unit",
                                                name="Freelancer accounts",
                                                parent_id=organization_root_id)

    spoke_account = org.Account("spoke-account",
                                name=f"Sandbox account for {spoke_account_name}",
                                email=spoke_account_email,
                                parent_id=spoke_account_unit.id,
                                role_name=spoke_account_access_role_name)

    return spoke_account.id


# Entry point
spoke_account_id = create_spoke_account()
create_user_output = spoke_account_id.apply(lambda account_id: create_user(account_id))

pulumi.export("spoke_account_url", create_user_output.console_url)
pulumi.export("spoke_account_username", create_user_output.username)
pulumi.export("spoke_account_encrypted_password", create_user_output.encrypted_password)
