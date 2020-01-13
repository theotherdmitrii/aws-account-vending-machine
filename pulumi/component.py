import pulumi
from pulumi_aws import s3

class MyComponent(pulumi.ComponentResource):
    """
    Todo
    """
    def __init__(self, name, opts = None):
        super().__init__('nuage:api:MyComponent', name, None, opts)
        bucket = s3.Bucket('test')
        self.register_outputs({
            'bucket_name': bucket.bucket
        })

