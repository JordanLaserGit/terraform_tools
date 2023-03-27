def get_attrs():
    """
    Attributes copied from tf show and then used to build a terraform config file.
    """
    attrs = {}

    attrs['aws_vpc'] = [
        'cidr_block',
        'instance_tenancy',
        'enable_dns_support',
        'enable_dns_hostnames',
        'enable_network_address_usage_metrics',
        'tags',
        'ipv6_cidr_block',
        'assign_generated_ipv6_cidr_block',
        'ipv4_ipam_pool_id',
        'ipv4_netmask_length'
        ]

    attrs['aws_subnet'] = [
        'availability_zone',
        'map_public_ip_on_launch',
        'cidr_block',
        'default_for_az',
        'filter',
        'ipv6_cidr_block',
        'state',
        'tags',
        'vpc_id'
        ]       
        
    attrs['aws_instance'] = [
        'ami',
        'associate_public_ip_address',
        'availability_zone',
        'capacity_reservation_specification',
        'cpu_core_count',
        'cpu_threads_per_core',
        'credit_specification',
        'disable_api_stop',
        'disable_api_termination',
        'ebs_block_device',
        'ebs_optimized',
        'enclave_options',
        'ephemeral_block_device',
        'get_password_data',
        'hibernation',
        'host_id',
        'host_resource_group_arn',
        'iam_instance_profile',
        'instance_initiated_shutdown_behavior',
        'instance_type',
        'key_name',
        'launch_template',
        'maintenance_options',
        'metadata_options',
        'monitoring',
        'network_interface',
        'placement_group',
        'placement_partition_number',
        'private_dns_name_options',
        'private_ip',
        'secondary_private_ips',
        'security_groups',
        'subnet_id',
        'tags',
        'tenancy',
        'vpc_security_group_ids'
        ]  

    attrs['aws_security_group'] = [
        'description',
        'egress',
        'ingress',
        'name',
        'tags',
        'vpc_id'
        ] 

    attrs['ingress/egress'] = [
            'cidr_blocks',
            'description',
            'from_port',
            'ipv6_cidr_blocks',
            'prefix_list_ids',
            'protocol',
            'security_groups',
            'self',
            'to_port'
    ]    
    
    return attrs