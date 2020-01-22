from typing import Any

import boto3
from pulumi import Input
from pulumi.dynamic import ResourceProvider, CreateResult, UpdateResult, DiffResult, Resource, CheckResult, ReadResult

client = boto3.client('workmail')


class DynamicAliasProvider(ResourceProvider):

    def check(self, olds: Any, news: Any) -> CheckResult:
        """ This method basically first check whether or not a alias exist for a given group """

        if 'organization_id' in news and 'group_id' in news:

            # We will get a list of all the alias for the group.
            response = client.list_aliases(
                OrganizationId=news['organization_id'],
                EntityId=news['group_id'],
                MaxResults=100
            )
            # A for loop over list of all the alias for that group so that we can determine that whether or not
            # we have to call the update method for creation of new alias or just do nothing.

            for alias in response['Aliases']:
                # this condition will check if the alias name exist from the list of alias that we got for a group
                # then it will show that there is not need to add a new alias by calling the update method and just
                # do nothing as this alias name already exist.
                # If alias with the specified name is already there do nothing and
                # return false so that update is not called on the resource.

                if alias == news['alias_email']:
                    error = {'alias': alias, 'message': 'Alias name already exist', 'group_id': news['group_id'],
                             'organization_id': news['organization_id']}
                    news['errors'] = [error]

            return CheckResult(news, [])

    def create(self, props):

        # Here first we check there are there any errors that have came from check method if so we print out that
        # issues.
        if 'errors' in props:
            for error in props['errors']:
                if 'group_id' in error and 'alias' in error:
                    return CreateResult(error['alias'], {'alias_email': error['alias'], 'group_id': error['group_id'],
                                                         'message': error['message']})

        client.create_alias(
            OrganizationId=props['organization_id'],
            EntityId=props['group_id'],
            Alias=props['alias_email']
        )

        return CreateResult(props['alias_email'],
                            {'alias_email': props['alias_email'], 'group_id': props['group_id'],
                             'message': 'New Alias Created for Group', 'organization_id': props['organization_id']})

    def update(self, resource_id: str, olds: Any, news: Any) -> UpdateResult:
        """ This update method is called if the diff method return True which means that alias with the specified name
                does not exist and we need to create one for that particular group
                In this method we would be creating a new alias for that group. """

        client.create_alias(
            OrganizationId=news['organization_id'],
            EntityId=news['group_id'],
            Alias=news['alias_email']
        )

        return UpdateResult(
            {'alias_email': news['alias_email'], 'group_id': news['group_id'],
             'message': 'New Alias Created for Group', 'organization_id': news['organization_id']})

    def diff(self, resource_id: str, olds: Any, news: Any) -> DiffResult:
        """ This diff method will simply determine whether or not we need to call the update method depending on does
            the alias name specified already exist or we need to create a new alias by calling update method. """

        # If alias with the specified name is already there do nothing and
        # return false so that update is not called on the resource
        if 'errors' in news:
            for error in news['errors']:
                if 'group_id' in error and 'alias' in error:
                    return DiffResult(False)

        # If alias name not already there then create one by invoking update method.
        return DiffResult(True)

    def read(self, resource_id: str, props) -> ReadResult:
        """ This method will give list all the alias for that group. """
        response = client.list_aliases(
            OrganizationId=props['organization_id'],
            EntityId=props['group_id'],
            MaxResults=100
        )
        result = response['Aliases']
        while 'NextToken' in response:
            response = client.list_aliases(
                OrganizationId=props['organization_id'],
                EntityId=props['group_id'],
                NextToken=response['NextToken'],
                MaxResults=100
            )
            result.extend(response['Aliases'])

        return ReadResult(id_=resource_id, outs=result)

    def delete(self, resource_id: str, props: Any) -> None:
        if 'organization_id' in props and 'group_id' in props and 'alias_email' in props:
            client.delete_alias(
                OrganizationId=props['organization_id'],
                EntityId=props['group_id'],
                Alias=props['alias_email']
            )


class Alias(Resource):
    def __init__(self, name, group_id: str, alias_email: str, organization_id: str, opts=None):
        full_args = {'group_id': group_id, 'message': None, 'alias_email': alias_email,
                     'organization_id': organization_id}
        super().__init__(DynamicAliasProvider(), name, full_args, opts)
