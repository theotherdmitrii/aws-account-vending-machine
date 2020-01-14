from typing import Any

import boto3
from pulumi import Input, export, Config
from pulumi.dynamic import ResourceProvider, CreateResult, UpdateResult, DiffResult, Resource, CheckResult, ReadResult

client = boto3.client('workmail')


class AliasArgs(object):
    organization_id: Input[str]
    group_id: Input[str]

    def __init__(self, organization_id, group_id):
        self.organization_id = organization_id
        self.group_id = group_id


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
                    error = {'alias': alias, 'message': 'Alias name already exist', 'group_id': news['group_id']}
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
                             'message': 'New Alias Created for Group'})

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
             'message': 'New Alias Created for Group'})

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

    # For this we don't think we need to use read method that's why it simply pass the control.

    def read(self, id_: str, props: Any) -> ReadResult:
        pass


class Alias(Resource):
    def __init__(self, name, group_id: str, alias_email: str, opts=None):
        args = AliasArgs('m-b01addc6667743b0b865f62342b5a217', group_id)
        full_args = {'group_id': None, 'message': None, 'alias_email': alias_email,
                     **vars(args)}
        super().__init__(DynamicAliasProvider(), name, full_args, opts)
