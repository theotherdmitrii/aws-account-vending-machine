### Creates Spoke Account and Admin User within the account


- Provide required configuration with `Pulumi.<stack-name>.yaml`

```yaml
config:
  create-spoke-account:org_id: o-123a
  create-spoke-account:org_account_name: freelancer1001
  create-spoke-account:org_account_email: freelancer1001@nuage.awsapps.com
  create-spoke-account:org_account_access_role_name: NuageAccessRole
  create-spoke-account:org_account_username: awesomedev
  create-spoke-account:org_account_userpass_length: 8
  create-spoke-account:org_account_userpass_encryption_pub_key: '/home/<user>/my-secure.pgp'
  create-spoke-account:workmail_org_id: m-123b
  create-spoke-account:workmail_group_email: root-workmail@nuage.awsapps.com
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
    console_url       : "https://123456789101.signin.aws.amazon.com/console"
    username          : "freelancers-awesomedev"
    encrypted_password: "wcBMA5Q5z3W8uCrdAQg"

```

- Decrypt user password with `./decrypt.sh`

```bash
$ ./decrypy.sh wcBMA5Q5z3W8uCrdAQg
```
