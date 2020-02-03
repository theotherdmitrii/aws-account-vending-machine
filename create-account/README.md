### Create Spoke Account 


- Provide required configuration with `Pulumi.<stack>.yaml`

```yaml
config:
  create-account:aws_organization_root_id: r-12qw
  create-account:spoke_account_name: awesomedev
  create-account:spoke_account_access_role_name: NuageAccessRole
```

- Create Spoke account with `pulimi up -y`

```bash
$ pulumi up -y

Outputs:
    spoke_account_id                : "123456789101"
    spoke_account_access_role       : "NuageAccessRole"

```



