from typing import Any

import boto3
from pulumi import Input
from pulumi.dynamic import ResourceProvider, Resource, CheckResult, CreateResult, DiffResult, CheckFailure, UpdateResult

required_props = ['username', 'password']


def client_with_session(name: str, role_arn):
    sts = boto3.client('sts')
    response = sts.assume_role(
        RoleArn=props["assume_role_arn"],
        RoleSessionName="pulumi.UserLoginProfileProvider",
        DurationSeconds=900)

    session = response["Credentials"]

    return boto3.resource(name,
                          aws_access_key_id=session["AccessKeyId"],
                          aws_secret_access_key=session["SecretAccessKey"],
                          aws_session_token=session["SessionToken"])


def client(name: str, props: Any):
    return client_with_session(name, props["assume_role_arn"]) if "assume_role_arn" in props else boto3.resource(name)


class AssumeRole:
    assume_role_arn: Input[str]

    def __init__(self, role_arn: Input[str] = None):
        self.assume_role_arn = role_arn


class UserLoginProfileProvider(ResourceProvider):

    def check(self, _olds: Any, _news: Any):
        failures = []

        for prop in required_props:
            if prop not in _news:
                failures.append(CheckFailure(property_='username', reason=f"property {prop} missing"))

        return CheckResult(inputs=_news, failures=failures)

    def create(self, _news: Any):
        iam = client("iam", _news)

        username = _news['username']
        password = _news['password']
        login_profile = iam.LoginProfile(user_name=username)
        login_profile.create(Password=password,
                             PasswordResetRequired=True)

        return CreateResult(username, {**_news, 'password_reset_required': True})

    def update(self, _id: str, _olds: Any, _news: Any):
        iam = client("iam", _news)
        username = _olds["username"]
        password = _news["password"]
        login_profile = iam.LoginProfile(user_name=username)
        login_profile.update(Password=password,
                             PasswordResetRequired=True)

        return UpdateResult()

    def delete(self, _id: str, _olds: Any):
        iam = client("iam", _olds)
        username = _olds['username']
        login_profile = iam.LoginProfile(user_name=username)
        login_profile.delete()

    def diff(self, _id: str, _olds: Any, _news: Any):
        changes = _olds['username'] == _news['username'] and not _olds['password'] == _news['password']
        return DiffResult(changes=bool(changes))


class UserLoginProfile(Resource):

    def __init__(self, name, username: Input[str], password: Input[str], assume_role: AssumeRole = None, opts=None):
        full_args = {'username': username, 'password': password, **vars(assume_role)} if (assume_role) else {
            'username': username, 'password': password}
        super().__init__(UserLoginProfileProvider(), name, full_args, opts)
