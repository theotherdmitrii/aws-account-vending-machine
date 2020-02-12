import pulumi
import pulumi_aws as aws
from decrypt import PasswordDecryptor
from pulumi import ComponentResource, ResourceOptions, Input, Output
from pulumi_aws import iam


class AWSOrganizationAccountUserArgs:
    account_id: Input[str]
    """
    AWS (spoke) account id
    """

    account_name: Input[str]
    """
    AWS (spoke) account name to generate user name
    """

    access_role_name: Input[str]
    """
    Access role for provider to assume
    """

    username: Input[str]
    """
    User's name
    """

    user_policy_arn: Input[str]
    """
    User's policy ARN
    """

    password_length: Input[int]
    """
    User's password length
    """

    def __init__(self, account_id: Input[str] = None, account_name: Input[str] = None,
                 access_role_name: Input[str] = None, username: Input[str] = None,
                 user_policy_arn: Input[str] = None, password_length: Input[int] = None):
        self.account_id = account_id
        self.account_name = account_name
        self.access_role_name = access_role_name
        self.username = username
        self.user_policy_arn = user_policy_arn
        self.password_length = password_length


class AWSOrganizationAccountUser(ComponentResource):
    """
    Creates an AWS Account within a given AWS Organization then creates a User
    within the new account with Administrator access
    """
    console_url: Output[str]
    """
    URL to follow to login to AWS console
    """

    username: Output[str]
    """
    User's name to login
    """

    password: Output[str]
    """
    Encrypted key for User to login 
    """

    def __init__(self,
                 name: str,
                 args: AWSOrganizationAccountUserArgs,
                 opts: ResourceOptions = None):
        super().__init__("nuage/aws:organizations:AWSOrganizationAccountUser", name, {}, opts)

        decryptor = PasswordDecryptor(email="qweasd@qwe.asd",
                                      passphrase="qweasd")

        provider = aws.Provider("freelance-account-provider",
                                assume_role={
                                    "role_arn": Output.all(args.account_id, args.access_role_name).apply(
                                        lambda a: f"arn:aws:iam::{a[0]}:role/{a[1]}")
                                })

        user = iam.User("freelance-account-user",
                        name=Output.all(args.account_name, args.username).apply(lambda a: f"{a[0]}-{a[1]}"),
                        opts=pulumi.ResourceOptions(
                            provider=provider
                        ))

        user_login_profile = iam.UserLoginProfile("freelance-account-user-login-profile",
                                                  user=user.name,
                                                  password_reset_required=True,
                                                  password_length=args.password_length,
                                                  pgp_key=decryptor.export(),
                                                  opts=pulumi.ResourceOptions(
                                                      provider=provider
                                                  ))

        user_policy_attachment = iam.UserPolicyAttachment("freelance-account-user_UserAccessRole",
                                                          policy_arn=args.user_policy_arn,
                                                          user=user.name,
                                                          opts=pulumi.ResourceOptions(
                                                              provider=provider
                                                          ))

        self.console_url = Output.all(args.account_id).apply(
            lambda a: f"https://{a[0]}.signin.aws.amazon.com/console")

        self.username = user.name

        self.password = Output.secret(user_login_profile.encrypted_password.apply(
            lambda enc: decryptor.decrypt(enc)))

        self.register_outputs({})
