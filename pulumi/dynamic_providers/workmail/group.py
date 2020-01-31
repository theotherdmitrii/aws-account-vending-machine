from typing import Any

import boto3
from pulumi.dynamic import ResourceProvider, CreateResult, UpdateResult, DiffResult, Resource, CheckResult, ReadResult

client = boto3.client('workmail')


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
                    error = {'group_id': group['Id'], 'message': 'group already exist',
                             'organization_id': news['organization_id']}
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

        create_group_response = client.create_group(
            OrganizationId=props['organization_id'],
            Name=props['group_name']
        )

        group_id = create_group_response['GroupId']

        client.register_to_work_mail(
            OrganizationId=props['organization_id'],
            EntityId=group_id,
            Email=props['group_email']
        )

        return CreateResult(group_id, {'group_id': group_id,
                                       'message': 'New Group Created',
                                       'organization_id': props['organization_id']})

    def update(self, resource_id: str, olds: Any, news: Any) -> UpdateResult:
        """ This update method is called if the diff method return True which means that group with the specified name
               does not exist and we need to create one.
               In this method we would be creating a new group for that organization. """
        response = client.create_group(
            OrganizationId=news['organization_id'],
            Name=news['group_name']
        )

        return UpdateResult({'group_id': response['GroupId'],
                             'message': 'New Group Created',
                             'organization_id': news['organization_id']})

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
    def read(self, resource_id: str, props) -> ReadResult:
        """ This method will give a groups for an organization. """
        response = client.list_groups(
            OrganizationId=props['organization_id'],
            GroupId=props['group_id']
        )
        return ReadResult(id_=resource_id, outs=response)

    def delete(self, resource_id: str, props: Any) -> None:
        """This method will delete the group according to the group_id and organization_id"""
        if 'group_id' in props and 'organization_id' in props:
            client.deregister_from_work_mail(
                OrganizationId=props['organization_id'],
                EntityId=props['group_id']
            )
            client.delete_group(
                OrganizationId=props['organization_id'],
                GroupId=props['group_id']
            )


class Group(Resource):
    def __init__(self, name, group_name: str, group_email: str, organization_id: str, opts=None):
        full_args = {'group_id': None, 'message': None, 'organization_id': organization_id, 'group_name': group_name,
                     'group_email': group_email}
        super().__init__(DynamicGroupProvider(), name, full_args, opts)
