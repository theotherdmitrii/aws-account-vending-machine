from typing import Any

import boto3
from pulumi import Input
from pulumi.dynamic import ResourceProvider, Resource, CheckResult, CreateResult, DiffResult, CheckFailure, UpdateResult

required_props = ['username', 'password']


def client_with_session(name: str, role_arn):
    """
    Creates boto3 resource with assuming provided role

    :param name:
    :param role_arn:
    :return:
    """

    sts = boto3.client('sts')
    response = sts.assume_role(
        RoleArn=role_arn,
        RoleSessionName="pulumi.dynamic.UserLoginProfileProvider",
        DurationSeconds=900)

    session = response["Credentials"]

    return boto3.resource(name,
                          aws_access_key_id=session["AccessKeyId"],
                          aws_secret_access_key=session["SecretAccessKey"],
                          aws_session_token=session["SessionToken"])


def client(name: str, props: Any):
    """
    Creates boto3 resource from provided props

    :param name:
    :param props:
    :return:
    """

    return client_with_session(name, props["assume_role_arn"]) if "assume_role_arn" in props else boto3.resource(name)


class AssumeRole:
    """
    The class holds role arn when assume role action required
    """

    assume_role_arn: Input[str]

    def __init__(self, role_arn: Input[str] = None):
        self.assume_role_arn = role_arn


class UserLoginProfileProvider(ResourceProvider):

    def check(self, _olds: Any, _news: Any):
        """
        Checks all required props are set

        :param _olds:
        :param _news:
        :return:
        """
        failures = []

        for prop in required_props:
            if prop not in _news:
                failures.append(CheckFailure(property_=prop, reason=f"property {prop} missing"))

        return CheckResult(inputs=_news, failures=failures)

    def create(self, _news: Any) -> CreateResult:
        """
        Creates new UserLoginProfile resource

        :param _news:
        :return:
        """

        iam = client("iam", _news)
        username = _news['username']
        password = _news['password']
        login_profile = iam.LoginProfile(user_name=username)
        login_profile.create(Password=password,
                             PasswordResetRequired=True)

        return CreateResult(username, outs={**_news, 'password_reset_required': True})

    def update(self, _id: str, _olds: Any, _news: Any) -> UpdateResult:
        """
        Updates existing UserLoginProfile resource

        :param _id:
        :param _olds:
        :param _news:
        :return:
        """

        iam = client("iam", _news)
        username = _olds["username"]
        password = _news["password"]
        login_profile = iam.LoginProfile(user_name=username)
        login_profile.update(Password=password,
                             PasswordResetRequired=True)

        return UpdateResult(outs={**_news, 'password_reset_required': True})

    def diff(self, _id: str, _olds: Any, _news: Any) -> DiffResult:
        """
        Checks if an update needed

        :param _id:
        :param _olds:
        :param _news:
        :return:
        """
        changes = _olds['username'] == _news['username'] and not _olds['password'] == _news['password']
        return DiffResult(changes=bool(changes))

    def delete(self, _id: str, _olds: Any):
        """
        Deletes UserLoginProfile resource

        :param _id:
        :param _olds:
        :return:
        """

        iam = client("iam", _olds)
        username = _olds['username']
        login_profile = iam.LoginProfile(user_name=username)
        login_profile.delete()


class UserLoginProfile(Resource):
    """
    IAM UserLoginProfile resource to provide access to AWS Console
    """

    def __init__(self, name, username: Input[str], password: Input[str], assume_role: AssumeRole = None, opts=None):
        full_args = {'username': username, 'password': password, **vars(assume_role)} if assume_role else {
            'username': username, 'password': password}
        super().__init__(UserLoginProfileProvider(), name, full_args, opts)
