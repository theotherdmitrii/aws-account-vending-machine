### Creates Spoke Account and Admin User within the account


- Provide required configuration with `Pulumi.<stack-name>.yaml`

```yaml
config:
  create-spoke-account:aws_organization_root_id: r-b2xr
  create-spoke-account:spoke_account_access_role_name: NuageAccessRole
  create-spoke-account:spoke_account_name: freelancers
  create-spoke-account:spoke_account_username: awesomedev
  create-spoke-account:pgp_pub_key_path: '/home/<user>/my-secure.pgp' 
```

- Create User account with `pulimi up -y`

```bash
$ pulumi up -y

     Type                             Name                                              Plan       
 +   pulumi:pulumi:Stack              create-user-dev                                   create     
 +   ├─ pulumi:providers:aws          spoke-account-provider                            create     
 +   ├─ aws:iam:User                  spoke-account-user                                create     
 +   ├─ aws:iam:UserLoginProfile      spoke-account-user-login-profile                  create     
 +   ├─ aws:iam:Role                  spoke-account-admin-role                          create     
 +   └─ aws:iam:RolePolicyAttachment  spoke-account-admin-role_AdministratorAccessRole  create     
 
Resources:
    + 6 to create

Do you want to perform this update? yes
Updating (dev):

     Type                             Name                                              Status      
 +   pulumi:pulumi:Stack              create-user-dev                                   created     
 +   ├─ pulumi:providers:aws          spoke-account-provider                            created     
 +   ├─ aws:iam:User                  spoke-account-user                                created     
 +   ├─ aws:iam:UserLoginProfile      spoke-account-user-login-profile                  created     
 +   ├─ aws:iam:Role                  spoke-account-admin-role                          created     
 +   └─ aws:iam:RolePolicyAttachment  spoke-account-admin-role_AdministratorAccessRole  created     
 
Outputs:
    spoke_account_encrypted_password: "wcBMA5Q5z3W8uCrdAQg"
    spoke_account_url               : "https://123456789101.signin.aws.amazon.com/console"
    spoke_account_username          : "freelancers-awesomedev"

```

- Decrypt user password with `./decrypt.sh`

```bash
$ ./decrypy.sh wcBMA5Q5z3W8uCrdAQg
```
