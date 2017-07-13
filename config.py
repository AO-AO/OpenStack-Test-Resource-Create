# Set manage_ip here, search it with `keystone endpoint-list`
manage_ip = '10.10.162.40'

auth_url = 'http://%s:5000/v2.0/' % manage_ip

# Set vdc_id here
project_admin_id = 'b263b90cba844d6a834a795f72eceddf'
project_vdc00_id = 'b6e2e8d97d524f99a8037b6d7e9177af'
project_vdc01_id = '6179661736194b0f88de1825bf8a8837'
project_vdc10_id = 'f2c68d794ef34a6c9b8030658eb8bb2b'

# Set user_id and user_passwd here
user_admin_id, user_admin_pa = 'a643912a387048c69c3eca8b723bb44c', 'admin'
user_admin000_id, user_admin000_pa = '632afa25bf0a4b6c86051ebf30ba3734', 'Aa111111'
user_user001_id, user_user001_pa  = '859325a5a63e4300883bd1fe10bdf7f6', 'Aa111111'
user_user010_id, user_user010_pa = '7721a17b56944110ab355f1854624939', 'Aa111111'
user_admin100_id, user_admin100_pa = 'c7f78d13f08046fbb9609b432c17ce2a', 'Aa111111'

# Public key /root/.ssh/rsa.pub
pub_key = \
"ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAGEAvLpEpIroCe4xhKt6HTOiy8gQUMnwzyJFRCRPGPc6A3gLkGbIEagDa8gx8572TZfIfjTCnSATTOYmZfEMmgm0OFriVepjEgcyrpet+7k1KyR35JMV7UTOE7GCxJF245U7\n"

# Not change
user_map = [{'project_name': 'admin', 'project_id': project_admin_id, 'user_info':
                 [{'user_name': 'admin', 'user_id': user_admin_id, 'password': user_admin_pa}]},
            {'project_name': 'vdc00', 'project_id': project_vdc00_id, 'user_info':
                 [{'user_name': 'admin000', 'user_id': user_admin000_id, 'password': user_admin000_pa},
                  {'user_name': 'user001', 'user_id': user_user001_id, 'password': user_user001_pa}]},
            {'project_name': 'vdc01', 'project_id': project_vdc01_id, 'user_info':
                 [{'user_name': 'user010', 'user_id': user_user010_id, 'password': user_user010_pa}]},
            {'project_name': 'vdc10', 'project_id': project_vdc10_id, 'user_info':
                 [{'user_name': 'admin100', 'user_id': user_admin100_id, 'password': user_admin100_pa}]}
           ]

