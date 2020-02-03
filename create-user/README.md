### Create Admin User within Spoke Account


- Provide required configuration with `Pulumi.<stack>.yaml`

```yaml
config:
  create-user:spoke_account_id: 123456789101
  create-user:spoke_account_name: freelancers
  create-user:spoke_account_username: awesomedev
  create-user:spoke_account_access_role_name: NuageAccessRole
  create-user:pgp_pub_key_path: '/home/<user>/my-secure.pgp'
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
