import boto3

class Boto3Response():

    def __init__(self):
        self.ami  = ''
        self.ec2  = boto3.client('ec2')
        self.ec2_responses = dict()

    def gen_vpc_response(self):

        self.ec2_responses['vpcs']      = self.ec2.describe_vpcs()
        self.ec2_responses['instances'] = self.ec2.describe_instances()
        tag_response     = self.ec2.describe_tags()

        # split tags based on resource type
        response_types = []
        for jtag in tag_response['Tags']:
            rs_type = jtag['ResourceType']
            if rs_type not in response_types:
                response_types.append(rs_type)

        tags = dict()
        for jtype in response_types: 
            tags[jtype] = []

        for jtag in tag_response['Tags']:
            rs_type = jtag['ResourceType']
            if rs_type in response_types:
                tags[rs_type].append(jtag)

        self.ec2_responses['tags'] = tags

        """
        describe_account_attributes
        describe_address_transfers
        describe_addresses
        describe_addresses_attribute
        describe_aggregate_id_format
        describe_availability_zones
        describe_aws_network_performance_metric_subscriptions
        describe_bundle_tasks
        describe_byoip_cidrs
        describe_capacity_reservation_fleets
        describe_capacity_reservations
        describe_carrier_gateways
        describe_classic_link_instances
        describe_client_vpn_authorization_rules
        describe_client_vpn_connections
        describe_client_vpn_endpoints
        describe_client_vpn_routes
        describe_client_vpn_target_networks
        describe_coip_pools
        describe_conversion_tasks
        describe_customer_gateways
        describe_dhcp_options
        describe_egress_only_internet_gateways
        describe_elastic_gpus
        describe_export_image_tasks
        describe_export_tasks
        describe_fast_launch_images
        describe_fast_snapshot_restores
        describe_fleet_history
        describe_fleet_instances
        describe_fleets
        describe_flow_logs
        describe_fpga_image_attribute
        describe_fpga_images
        describe_host_reservation_offerings
        describe_host_reservations
        describe_hosts
        describe_iam_instance_profile_associations
        describe_id_format
        describe_identity_id_format
        describe_image_attribute
        describe_images
        describe_import_image_tasks
        describe_import_snapshot_tasks
        describe_instance_attribute
        describe_instance_credit_specifications
        describe_instance_event_notification_attributes
        describe_instance_event_windows
        describe_instance_status
        describe_instance_type_offerings
        describe_instance_types
        describe_instances
        describe_internet_gateways
        describe_ipam_pools
        describe_ipam_resource_discoveries
        describe_ipam_resource_discovery_associations
        describe_ipam_scopes
        describe_ipams
        describe_ipv6_pools
        describe_key_pairs
        describe_launch_template_versions
        describe_launch_templates
        describe_local_gateway_route_table_virtual_interface_group_associations
        describe_local_gateway_route_table_vpc_associations
        describe_local_gateway_route_tables
        describe_local_gateway_virtual_interface_groups
        describe_local_gateway_virtual_interfaces
        describe_local_gateways
        describe_managed_prefix_lists
        describe_moving_addresses
        describe_nat_gateways
        describe_network_acls
        describe_network_insights_access_scope_analyses
        describe_network_insights_access_scopes
        describe_network_insights_analyses
        describe_network_insights_paths
        describe_network_interface_attribute
        describe_network_interface_permissions
        describe_network_interfaces
        describe_placement_groups
        describe_prefix_lists
        describe_principal_id_format
        describe_public_ipv4_pools
        describe_regions
        describe_replace_root_volume_tasks
        describe_reserved_instances
        describe_reserved_instances_listings
        describe_reserved_instances_modifications
        describe_reserved_instances_offerings
        describe_route_tables
        describe_scheduled_instance_availability
        describe_scheduled_instances
        describe_security_group_references
        describe_security_group_rules
        describe_security_groups
        describe_snapshot_attribute
        describe_snapshot_tier_status
        describe_snapshots
        describe_spot_datafeed_subscription
        describe_spot_fleet_instances
        describe_spot_fleet_request_history
        describe_spot_fleet_requests
        describe_spot_instance_requests
        describe_spot_price_history
        describe_stale_security_groups
        describe_store_image_tasks
        describe_subnets
        describe_tags
        describe_traffic_mirror_filters
        describe_traffic_mirror_sessions
        describe_traffic_mirror_targets
        describe_transit_gateway_attachments
        describe_transit_gateway_connect_peers
        describe_transit_gateway_connects
        describe_transit_gateway_multicast_domains
        describe_transit_gateway_peering_attachments
        describe_transit_gateway_policy_tables
        describe_transit_gateway_route_table_announcements
        describe_transit_gateway_route_tables
        describe_transit_gateway_vpc_attachments
        describe_transit_gateways
        describe_trunk_interface_associations
        describe_verified_access_endpoints
        describe_verified_access_groups
        describe_verified_access_instance_logging_configurations
        describe_verified_access_instances
        describe_verified_access_trust_providers
        describe_volume_attribute
        describe_volume_status
        describe_volumes
        describe_volumes_modifications
        describe_vpc_attribute
        describe_vpc_classic_link
        describe_vpc_classic_link_dns_support
        describe_vpc_endpoint_connection_notifications
        describe_vpc_endpoint_connections
        describe_vpc_endpoint_service_configurations
        describe_vpc_endpoint_service_permissions
        describe_vpc_endpoint_services
        describe_vpc_endpoints
        describe_vpc_peering_connections
        describe_vpcs
        describe_vpn_connections
        describe_vpn_gateways
        """


