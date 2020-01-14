from typing import Any

import boto3
from pulumi import Input, export
from pulumi.dynamic import ResourceProvider, CreateResult, UpdateResult, DiffResult, Resource, CheckResult, ReadResult

client = boto3.client('workmail')


class GroupArgs(object):
    organization_id: Input[str]
    group_name: Input[str]

    def __init__(self, organization_id, group_name):
        self.organization_id = organization_id
        self.group_name = group_name


class DynamicGroupProvider(ResourceProvider):

    def check(self, olds, news):
        if 'organization_id' in news and 'group_name' in news:
            response = client.list_groups(
                OrganizationId=news['organization_id'],
                MaxResults=100
            )
            for group in response['Groups']:
                """ this condition will check if the group name exist from the list of groups that we got for a organization
                               and if the State of the group is not DELETED then it will show that there is not need to 
                               add a new group by calling the update method and just do nothing as this group 
                               already exist. """
                if group['Name'] == news['group_name'] and group['State'] != 'DELETED':
                    error = {'group_id': group['Id'], 'message': 'group already exist'}
                    news['errors'] = [error]
        return CheckResult(news, [])

    def create(self, props):

        """ This method basically first check whether or not a group exist for a given organization if so it outputs group_id
                and a message that group already exist.
                If the group does not exist we just simply create one and outputs group_id and a message that new group
                created """

        # Here first we check there are there any errors that have came from check method if so we print out that
        # issues
        if 'errors' in props:
            for error in props['errors']:
                if 'group_id' in error:
                    return CreateResult(error['group_id'], {'group_id': error['group_id'],
                                                            'message': error['message']})

        response = client.create_group(
            OrganizationId=props['organization_id'],
            Name=props['group_name']
        )

        return CreateResult(response['GroupId'],
                            {'group_id': response['GroupId'],
                             'message': 'New Group Created'})

    def update(self, resource_id: str, olds: Any, news: Any) -> UpdateResult:
        """ This update method is called if the diff method return True which means that group with the specified name
               does not exist and we need to create one.
               In this method we would be creating a new group for that organization. """

        response = client.create_group(
            OrganizationId=news['organization_id'],
            Name=news['group_name']
        )

        return UpdateResult({'group_id': response['GroupId'],
                             'message': 'New Group Created'})

    def diff(self, resource_id: str, olds: Any, news: Any) -> DiffResult:
        """ This diff method will simply determine whether or not we need to call the update method depending on does the
                group name specified already exist or we need to create a new group by calling update method """

        # If group with the specified name is already there do nothing and
        # return false so that update is not called on the resource
        if 'errors' in news:
            for error in news['errors']:
                if 'group_id' in error:
                    return DiffResult(False)

        # If group name not already there then create one by invoking update method
        return DiffResult(True)

    # For this we don't think we need to use read method that's why it simply pass the control.
    def read(self, id_: str, props: Any) -> ReadResult:
        pass


class Group(Resource):
    def __init__(self, name, group_name: str, organization_id: str, opts=None):
        full_args = {'group_id': None, 'message': None,
                     **vars(GroupArgs(organization_id, group_name))}
        super().__init__(DynamicGroupProvider(), name, full_args, opts)
