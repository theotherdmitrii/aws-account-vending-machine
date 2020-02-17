### Create Spoke Account and Admin User within the account


#### Prerequisites
1. Python >= 3.7.5 
1. Pulumi CLI >= 1.9.1


#### Getting Started

1. Install dependencies with `pip`

    ```bash
    pip install -r requirements/global.txt
    ```

1. Create a stack with pulumi cli
    
    ```bash
    pulumi stack init <stack-name>
    ```

1. Provide required configuration for pulumi program with `./stacks/Pulumi.<stack-name>.yaml`
    
    ```yaml
    config:
      create-aws-account:org_id: o-123a
      create-aws-account:org_account_name: freelancer1001
      create-aws-account:org_account_email: freelancer1001@nuage.awsapps.com
      create-aws-account:org_account_access_role_name: NuageAccessRole
      create-aws-account:org_account_username: awesomedev
      create-aws-account:workmail_org_id: m-123b
      create-aws-account:workmail_group_email: root-workmail@nuage.awsapps.com
    ```

1. Create an account and admin user with `pulimi up -y`

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
        password          : "wcBMA5Q5z3W8uCrdAQg"
    
    ```

1. Use the outputs to login into the account


#### Dynamic providers

Few dynamic providers were added to complete the program

1. WorkMail dynamic providers were added to manage WorkMail Group and Alias resources as no other WorkMail providers exist at the moment. 
2. A dynamic provider `UserLoginProfileProvider` was added to avoid PGP key management required by default Terraform provider, and make user login profile creation transparent for end users. 

All dynamic providers used Boto3 client library to create and manage AWS resources. 
 