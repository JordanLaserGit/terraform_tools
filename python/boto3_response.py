import boto3

class Boto3Response():

    def __init__(self):
        self.ec2  = boto3.client('ec2')
        self.ec2_responses = dict()

        self.ec2_responses_failed : list

        self.region = boto3.session.Session().region_name

    def tag_split(self):      
        tag_response  = self.ec2_responses['tags']

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

    def gen_all_responses(self):        

        failed = []

        # try:
        #     self.ec2_responses['account_attributes']                                               = self.ec2.describe_account_attributes()
        # except:
        #     failed.append('describe_account_attributes')
        # try:
        #     self.ec2_responses['address_transfers']                                                = self.ec2.describe_address_transfers()
        # except:
        #     failed.append('describe_address_transfers')
        # try:
        #     self.ec2_responses['addresses']                                                        = self.ec2.describe_addresses()
        # except:
        #     failed.append('describe_addresses')
        # try:
        #     self.ec2_responses['addresses_attribute']                                              = self.ec2.describe_addresses_attribute()
        # except:
        #     failed.append('describe_addresses_attribute')
        # try:
        #     self.ec2_responses['aggregate_id_format']                                              = self.ec2.describe_aggregate_id_format()
        # except:
        #     failed.append('describe_aggregate_id_format')
        # try:
        #     self.ec2_responses['availability_zones']                                               = self.ec2.describe_availability_zones()
        # except:
        #     failed.append('describe_availability_zones')
        # try:
        #     self.ec2_responses['aws_network_performance_metric_subscriptions']                     = self.ec2.describe_aws_network_performance_metric_subscriptions()
        # except:
        #     failed.append('describe_aws_network_performance_metric_subscriptions')
        # try:
        #     self.ec2_responses['bundle_tasks']                                                     = self.ec2.describe_bundle_tasks()
        # except:
        #     failed.append('describe_bundle_tasks')
        # try:
        #     self.ec2_responses['byoip_cidrs']                                                      = self.ec2.describe_byoip_cidrs()
        # except:
        #     failed.append('describe_byoip_cidrs')
        # try:
        #     self.ec2_responses['capacity_reservation_fleets']                                      = self.ec2.describe_capacity_reservation_fleets()
        # except:
        #     failed.append('describe_capacity_reservation_fleets')
        # try:
        #     self.ec2_responses['capacity_reservations']                                            = self.ec2.describe_capacity_reservations()
        # except:
        #     failed.append('describe_capacity_reservations')
        # try:
        #     self.ec2_responses['carrier_gateways']                                                 = self.ec2.describe_carrier_gateways()
        # except:
        #     failed.append('describe_carrier_gateways')
        # try:
        #     self.ec2_responses['classic_link_instances']                                           = self.ec2.describe_classic_link_instances()
        # except:
        #     failed.append('describe_classic_link_instances')
        # try:
        #     self.ec2_responses['client_vpn_authorization_rules']                                   = self.ec2.describe_client_vpn_authorization_rules()
        # except:
        #     failed.append('describe_client_vpn_authorization_rules')
        # try:
        #     self.ec2_responses['client_vpn_connections']                                           = self.ec2.describe_client_vpn_connections()
        # except:
        #     failed.append('describe_client_vpn_connections')
        # try:
        #     self.ec2_responses['client_vpn_endpoints']                                             = self.ec2.describe_client_vpn_endpoints()
        # except:
        #     failed.append('describe_client_vpn_endpoints')
        # try:
        #     self.ec2_responses['client_vpn_routes']                                                = self.ec2.describe_client_vpn_routes()
        # except:
        #     failed.append('describe_client_vpn_routes')
        # try:
        #     self.ec2_responses['client_vpn_target_networks']                                       = self.ec2.describe_client_vpn_target_networks()
        # except:
        #     failed.append('describe_client_vpn_target_networks')
        # try:
        #     self.ec2_responses['coip_pools']                                                       = self.ec2.describe_coip_pools()
        # except:
        #     failed.append('describe_coip_pools')
        # try:
        #     self.ec2_responses['conversion_tasks']                                                 = self.ec2.describe_conversion_tasks()
        # except:
        #     failed.append('describe_conversion_tasks')
        # try:
        #     self.ec2_responses['customer_gateways']                                                = self.ec2.describe_customer_gateways()
        # except:
        #     failed.append('describe_customer_gateways')
        # try:
        #     self.ec2_responses['dhcp_options']                                                     = self.ec2.describe_dhcp_options()
        # except:
        #     failed.append('describe_dhcp_options')
        # try:
        #     self.ec2_responses['egress_only_internet_gateways']                                    = self.ec2.describe_egress_only_internet_gateways()
        # except:
        #     failed.append('describe_egress_only_internet_gateways')
        # try:
        #     self.ec2_responses['elastic_gpus']                                                     = self.ec2.describe_elastic_gpus()
        # except:
        #     failed.append('describe_elastic_gpus')
        # try:
        #     self.ec2_responses['export_image_tasks']                                               = self.ec2.describe_export_image_tasks()
        # except:
        #     failed.append('describe_export_image_tasks')
        # try:
        #     self.ec2_responses['export_tasks']                                                     = self.ec2.describe_export_tasks()
        # except:
        #     failed.append('describe_export_tasks')
        # try:
        #     self.ec2_responses['fast_launch_images']                                               = self.ec2.describe_fast_launch_images()
        # except:
        #     failed.append('describe_fast_launch_images')
        # try:
        #     self.ec2_responses['fast_snapshot_restores']                                           = self.ec2.describe_fast_snapshot_restores()
        # except:
        #     failed.append('describe_fast_snapshot_restores')
        # try:
        #     self.ec2_responses['fleet_history']                                                    = self.ec2.describe_fleet_history()
        # except:
        #     failed.append('describe_fleet_history')
        # try:
        #     self.ec2_responses['fleet_instances']                                                  = self.ec2.describe_fleet_instances()
        # except:
        #     failed.append('describe_fleet_instances')
        # try:
        #     self.ec2_responses['fleets']                                                           = self.ec2.describe_fleets()
        # except:
        #     failed.append('describe_fleets')
        # try:
        #     self.ec2_responses['flow_logs']                                                        = self.ec2.describe_flow_logs()
        # except:
        #     failed.append('describe_flow_logs')
        # try:
        #     self.ec2_responses['fpga_image_attribute']                                             = self.ec2.describe_fpga_image_attribute()
        # except:
        #     failed.append('describe_fpga_image_attribute')
        # try:
        #     self.ec2_responses['fpga_images']                                                      = self.ec2.describe_fpga_images()
        # except:
        #     failed.append('describe_fpga_images')
        # try:
        #     self.ec2_responses['host_reservation_offerings']                                       = self.ec2.describe_host_reservation_offerings()
        # except:
        #     failed.append('describe_host_reservation_offerings')
        # try:
        #     self.ec2_responses['host_reservations']                                                = self.ec2.describe_host_reservations()
        # except:
        #     failed.append('describe_host_reservations')
        # try:
        #     self.ec2_responses['hosts']                                                            = self.ec2.describe_hosts()
        # except:
        #     failed.append('describe_hosts')
        # try:
        #     self.ec2_responses['iam_instance_profile_associations']                                = self.ec2.describe_iam_instance_profile_associations()
        # except:
        #     failed.append('describe_iam_instance_profile_associations')
        # try:
        #     self.ec2_responses['id_format']                                                        = self.ec2.describe_id_format()
        # except:
        #     failed.append('describe_id_format')
        # try:
        #     self.ec2_responses['identity_id_format']                                               = self.ec2.describe_identity_id_format()
        # except:
        #     failed.append('describe_identity_id_format')
        # try:
        #     self.ec2_responses['image_attribute']                                                  = self.ec2.describe_image_attribute()
        # except:
        #     failed.append('describe_image_attribute')
        # try:
        #     self.ec2_responses['images']                                                           = self.ec2.describe_images()
        # except:
        #     failed.append('describe_images')
        # try:
        #     self.ec2_responses['import_image_tasks']                                               = self.ec2.describe_import_image_tasks()
        # except:
        #     failed.append('describe_import_image_tasks')
        # try:
        #     self.ec2_responses['import_snapshot_tasks']                                            = self.ec2.describe_import_snapshot_tasks()
        # except:
        #     failed.append('describe_import_snapshot_tasks')
        # try:
        #     self.ec2_responses['instance_attribute']                                               = self.ec2.describe_instance_attribute()
        # except:
        #     failed.append('describe_instance_attribute')
        # try:
        #     self.ec2_responses['instance_credit_specifications']                                   = self.ec2.describe_instance_credit_specifications()
        # except:
        #     failed.append('describe_instance_credit_specifications')
        # try:
        #     self.ec2_responses['instance_event_notification_attributes']                           = self.ec2.describe_instance_event_notification_attributes()
        # except:
        #     failed.append('describe_instance_event_notification_attributes')
        # try:
        #     self.ec2_responses['instance_event_windows']                                           = self.ec2.describe_instance_event_windows()
        # except:
        #     failed.append('describe_instance_event_windows')
        # try:
        #     self.ec2_responses['instance_status']                                                  = self.ec2.describe_instance_status()
        # except:
        #     failed.append('describe_instance_status')
        # try:
        #     self.ec2_responses['instance_type_offerings']                                          = self.ec2.describe_instance_type_offerings()
        # except:
        #     failed.append('describe_instance_type_offerings')
        # try:
        #     self.ec2_responses['instance_types']                                                   = self.ec2.describe_instance_types()
        # except:
        #     failed.append('describe_instance_types')
        try:
            self.ec2_responses['instances']                                                        = self.ec2.describe_instances()
        except:
            failed.append('describe_instances')
        # try:
        #     self.ec2_responses['internet_gateways']                                                = self.ec2.describe_internet_gateways()
        # except:
        #     failed.append('describe_internet_gateways')
        # try:
        #     self.ec2_responses['ipam_pools']                                                       = self.ec2.describe_ipam_pools()
        # except:
        #     failed.append('describe_ipam_pools')
        # try:
        #     self.ec2_responses['ipam_resource_discoveries']                                        = self.ec2.describe_ipam_resource_discoveries()
        # except:
        #     failed.append('describe_ipam_resource_discoveries')
        # try:
        #     self.ec2_responses['ipam_resource_discovery_associations']                             = self.ec2.describe_ipam_resource_discovery_associations()
        # except:
        #     failed.append('describe_ipam_resource_discovery_associations')
        # try:
        #     self.ec2_responses['ipam_scopes']                                                      = self.ec2.describe_ipam_scopes()
        # except:
        #     failed.append('describe_ipam_scopes')
        # try:
        #     self.ec2_responses['ipams']                                                            = self.ec2.describe_ipams()
        # except:
        #     failed.append('describe_ipams')
        # try:
        #     self.ec2_responses['ipv6_pools']                                                       = self.ec2.describe_ipv6_pools()
        # except:
        #     failed.append('describe_ipv6_pools')
        # try:
        #     self.ec2_responses['key_pairs']                                                        = self.ec2.describe_key_pairs()
        # except:
        #     failed.append('describe_key_pairs')
        # try:
        #     self.ec2_responses['launch_template_versions']                                         = self.ec2.describe_launch_template_versions()
        # except:
        #     failed.append('describe_launch_template_versions')
        # try:
        #     self.ec2_responses['launch_templates']                                                 = self.ec2.describe_launch_templates()
        # except:
        #     failed.append('describe_launch_templates')
        # try:
        #     self.ec2_responses['local_gateway_route_table_virtual_interface_group_associations']   = self.ec2.describe_local_gateway_route_table_virtual_interface_group_associations()
        # except:
        #     failed.append('describe_local_gateway_route_table_virtual_interface_group_associations')
        # try:
        #     self.ec2_responses['local_gateway_route_table_vpc_associations']                       = self.ec2.describe_local_gateway_route_table_vpc_associations()
        # except:
        #     failed.append('describe_local_gateway_route_table_vpc_associations')
        # try:
        #     self.ec2_responses['local_gateway_route_tables']                                       = self.ec2.describe_local_gateway_route_tables()
        # except:
        #     failed.append('describe_local_gateway_route_tables')
        # try:
        #     self.ec2_responses['local_gateway_virtual_interface_groups']                           = self.ec2.describe_local_gateway_virtual_interface_groups()
        # except:
        #     failed.append('describe_local_gateway_virtual_interface_groups')
        # try:
        #     self.ec2_responses['local_gateway_virtual_interfaces']                                 = self.ec2.describe_local_gateway_virtual_interfaces()
        # except:
        #     failed.append('describe_local_gateway_virtual_interfaces')
        # try:
        #     self.ec2_responses['local_gateways']                                                   = self.ec2.describe_local_gateways()
        # except:
        #     failed.append('describe_local_gateways')
        # try:
        #     self.ec2_responses['managed_prefix_lists']                                             = self.ec2.describe_managed_prefix_lists()
        # except:
        #     failed.append('describe_managed_prefix_lists')
        # try:
        #     self.ec2_responses['moving_addresses']                                                 = self.ec2.describe_moving_addresses()
        # except:
        #     failed.append('describe_moving_addresses')
        # try:
        #     self.ec2_responses['nat_gateways']                                                     = self.ec2.describe_nat_gateways()
        # except:
        #     failed.append('describe_nat_gateways')
        # try:
        #     self.ec2_responses['network_acls']                                                     = self.ec2.describe_network_acls()
        # except:
        #     failed.append('describe_network_acls')
        # try:
        #     self.ec2_responses['network_insights_access_scope_analyses']                           = self.ec2.describe_network_insights_access_scope_analyses()
        # except:
        #     failed.append('describe_network_insights_access_scope_analyses')
        # try:
        #     self.ec2_responses['network_insights_access_scopes']                                   = self.ec2.describe_network_insights_access_scopes()
        # except:
        #     failed.append('describe_network_insights_access_scopes')
        # try:
        #     self.ec2_responses['network_insights_analyses']                                        = self.ec2.describe_network_insights_analyses()
        # except:
        #     failed.append('describe_network_insights_analyses')
        # try:
        #     self.ec2_responses['network_insights_paths']                                           = self.ec2.describe_network_insights_paths()
        # except:
        #     failed.append('describe_network_insights_paths')
        # try:
        #     self.ec2_responses['network_interface_attribute']                                      = self.ec2.describe_network_interface_attribute()
        # except:
        #     failed.append('describe_network_interface_attribute')
        # try:
        #     self.ec2_responses['network_interface_permissions']                                    = self.ec2.describe_network_interface_permissions()
        # except:
        #     failed.append('describe_network_interface_permissions')
        # try:
        #     self.ec2_responses['network_interfaces']                                               = self.ec2.describe_network_interfaces()
        # except:
        #     failed.append('describe_network_interfaces')
        # try:
        #     self.ec2_responses['placement_groups']                                                 = self.ec2.describe_placement_groups()
        # except:
        #     failed.append('describe_placement_groups')
        # try:
        #     self.ec2_responses['prefix_lists']                                                     = self.ec2.describe_prefix_lists()
        # except:
        #     failed.append('describe_prefix_lists')
        # try:
        #     self.ec2_responses['principal_id_format']                                              = self.ec2.describe_principal_id_format()
        # except:
        #     failed.append('describe_principal_id_format')
        # try:
        #     self.ec2_responses['public_ipv4_pools']                                                = self.ec2.describe_public_ipv4_pools()
        # except:
        #     failed.append('describe_public_ipv4_pools')
        # try:
        #     self.ec2_responses['regions']                                                          = self.ec2.describe_regions()
        # except:
        #     failed.append('describe_regions')
        # try:
        #     self.ec2_responses['replace_root_volume_tasks']                                        = self.ec2.describe_replace_root_volume_tasks()
        # except:
        #     failed.append('describe_replace_root_volume_tasks')
        # try:
        #     self.ec2_responses['reserved_instances']                                               = self.ec2.describe_reserved_instances()
        # except:
        #     failed.append('describe_reserved_instances')
        # try:
        #     self.ec2_responses['reserved_instances_listings']                                      = self.ec2.describe_reserved_instances_listings()
        # except:
        #     failed.append('describe_reserved_instances_listings')
        # try:
        #     self.ec2_responses['reserved_instances_modifications']                                 = self.ec2.describe_reserved_instances_modifications()
        # except:
        #     failed.append('describe_reserved_instances_modifications')
        # try:
        #     self.ec2_responses['reserved_instances_offerings']                                     = self.ec2.describe_reserved_instances_offerings()
        # except:
        #     failed.append('describe_reserved_instances_offerings')
        # try:
        #     self.ec2_responses['route_tables']                                                     = self.ec2.describe_route_tables()
        # except:
        #     failed.append('describe_route_tables')
        # try:
        #     self.ec2_responses['scheduled_instance_availability']                                  = self.ec2.describe_scheduled_instance_availability()
        # except:
        #     failed.append('describe_scheduled_instance_availability')
        # try:
        #     self.ec2_responses['scheduled_instances']                                              = self.ec2.describe_scheduled_instances()
        # except:
        #     failed.append('describe_scheduled_instances')
        # try:
        #     self.ec2_responses['security_group_references']                                        = self.ec2.describe_security_group_references()
        # except:
        #     failed.append('describe_security_group_references')
        # try:
        #     self.ec2_responses['security_group_rules']                                             = self.ec2.describe_security_group_rules()
        # except:
        #     failed.append('describe_security_group_rules')
        # try:
        #     self.ec2_responses['security_groups']                                                  = self.ec2.describe_security_groups()
        # except:
        #     failed.append('describe_security_groups')
        # try:
        #     self.ec2_responses['snapshot_attribute']                                               = self.ec2.describe_snapshot_attribute()
        # except:
        #     failed.append('describe_snapshot_attribute')
        # try:
        #     self.ec2_responses['snapshot_tier_status']                                             = self.ec2.describe_snapshot_tier_status()
        # except:
        #     failed.append('describe_snapshot_tier_status')
        # try:
        #     self.ec2_responses['snapshots']                                                        = self.ec2.describe_snapshots()
        # except:
        #     failed.append('describe_snapshots')
        # try:
        #     self.ec2_responses['spot_datafeed_subscription']                                       = self.ec2.describe_spot_datafeed_subscription()
        # except:
        #     failed.append('describe_spot_datafeed_subscription')
        # try:
        #     self.ec2_responses['spot_fleet_instances']                                             = self.ec2.describe_spot_fleet_instances()
        # except:
        #     failed.append('describe_spot_fleet_instances')
        # try:
        #     self.ec2_responses['spot_fleet_request_history']                                       = self.ec2.describe_spot_fleet_request_history()
        # except:
        #     failed.append('describe_spot_fleet_request_history')
        # try:
        #     self.ec2_responses['spot_fleet_requests']                                              = self.ec2.describe_spot_fleet_requests()
        # except:
        #     failed.append('describe_spot_fleet_requests')
        # try:
        #     self.ec2_responses['spot_instance_requests']                                           = self.ec2.describe_spot_instance_requests()
        # except:
        #     failed.append('describe_spot_instance_requests')
        # try:
        #     self.ec2_responses['spot_price_history']                                               = self.ec2.describe_spot_price_history()
        # except:
        #     failed.append('describe_spot_price_history')
        # try:
        #     self.ec2_responses['stale_security_groups']                                            = self.ec2.describe_stale_security_groups()
        # except:
        #     failed.append('describe_stale_security_groups')
        # try:
        #     self.ec2_responses['store_image_tasks']                                                = self.ec2.describe_store_image_tasks()
        # except:
        #     failed.append('describe_store_image_tasks')
        try:
            self.ec2_responses['subnets']                                                          = self.ec2.describe_subnets()
        except:
            failed.append('describe_subnets')
        try:
            self.ec2_responses['tags']                                                             = self.ec2.describe_tags()
        except:
            failed.append('describe_tags')
        # try:
        #     self.ec2_responses['traffic_mirror_filters']                                           = self.ec2.describe_traffic_mirror_filters()
        # except:
        #     failed.append('describe_traffic_mirror_filters')
        # try:
        #     self.ec2_responses['traffic_mirror_sessions']                                          = self.ec2.describe_traffic_mirror_sessions()
        # except:
        #     failed.append('describe_traffic_mirror_sessions')
        # try:
        #     self.ec2_responses['traffic_mirror_targets']                                           = self.ec2.describe_traffic_mirror_targets()
        # except:
        #     failed.append('describe_traffic_mirror_targets')
        # try:
        #     self.ec2_responses['transit_gateway_attachments']                                      = self.ec2.describe_transit_gateway_attachments()
        # except:
        #     failed.append('describe_transit_gateway_attachments')
        # try:
        #     self.ec2_responses['transit_gateway_connect_peers']                                    = self.ec2.describe_transit_gateway_connect_peers()
        # except:
        #     failed.append('describe_transit_gateway_connect_peers')
        # try:
        #     self.ec2_responses['transit_gateway_connects']                                         = self.ec2.describe_transit_gateway_connects()
        # except:
        #     failed.append('describe_transit_gateway_connects')
        # try:
        #     self.ec2_responses['transit_gateway_multicast_domains']                                = self.ec2.describe_transit_gateway_multicast_domains()
        # except:
        #     failed.append('describe_transit_gateway_multicast_domains')
        # try:
        #     self.ec2_responses['transit_gateway_peering_attachments']                              = self.ec2.describe_transit_gateway_peering_attachments()
        # except:
        #     failed.append('describe_transit_gateway_peering_attachments')
        # try:
        #     self.ec2_responses['transit_gateway_policy_tables']                                    = self.ec2.describe_transit_gateway_policy_tables()
        # except:
        #     failed.append('describe_transit_gateway_policy_tables')
        # try:
        #     self.ec2_responses['transit_gateway_route_table_announcements']                        = self.ec2.describe_transit_gateway_route_table_announcements()
        # except:
        #     failed.append('describe_transit_gateway_route_table_announcements')
        # try:
        #     self.ec2_responses['transit_gateway_route_tables']                                     = self.ec2.describe_transit_gateway_route_tables()
        # except:
        #     failed.append('describe_transit_gateway_route_tables')
        # try:
        #     self.ec2_responses['transit_gateway_vpc_attachments']                                  = self.ec2.describe_transit_gateway_vpc_attachments()
        # except:
        #     failed.append('describe_transit_gateway_vpc_attachments')
        # try:
        #     self.ec2_responses['transit_gateways']                                                 = self.ec2.describe_transit_gateways()
        # except:
        #     failed.append('describe_transit_gateways')
        # try:
        #     self.ec2_responses['trunk_interface_associations']                                     = self.ec2.describe_trunk_interface_associations()
        # except:
        #     failed.append('describe_trunk_interface_associations')
        # try:
        #     self.ec2_responses['verified_access_endpoints']                                        = self.ec2.describe_verified_access_endpoints()
        # except:
        #     failed.append('describe_verified_access_endpoints')
        # try:
        #     self.ec2_responses['verified_access_groups']                                           = self.ec2.describe_verified_access_groups()
        # except:
        #     failed.append('describe_verified_access_groups')
        # try:
        #     self.ec2_responses['verified_access_instance_logging_configurations']                  = self.ec2.describe_verified_access_instance_logging_configurations()
        # except:
        #     failed.append('describe_verified_access_instance_logging_configurations')
        # try:
        #     self.ec2_responses['verified_access_instances']                                        = self.ec2.describe_verified_access_instances()
        # except:
        #     failed.append('describe_verified_access_instances')
        # try:
        #     self.ec2_responses['verified_access_trust_providers']                                  = self.ec2.describe_verified_access_trust_providers()
        # except:
        #     failed.append('describe_verified_access_trust_providers')
        # try:
        #     self.ec2_responses['volume_attribute']                                                 = self.ec2.describe_volume_attribute()
        # except:
        #     failed.append('describe_volume_attribute')
        # try:
        #     self.ec2_responses['volume_status']                                                    = self.ec2.describe_volume_status()
        # except:
        #     failed.append('describe_volume_status')
        # try:
        #     self.ec2_responses['volumes']                                                          = self.ec2.describe_volumes()
        # except:
        #     failed.append('describe_volumes')
        # try:
        #     self.ec2_responses['volumes_modifications']                                            = self.ec2.describe_volumes_modifications()
        # except:
        #     failed.append('describe_volumes_modifications')
        try:
            self.ec2_responses['vpc_classic_link']                                                 = self.ec2.describe_vpc_classic_link()
        except:
            failed.append('describe_vpc_classic_link')
        try:
            self.ec2_responses['vpc_classic_link_dns_support']                                     = self.ec2.describe_vpc_classic_link_dns_support()
        except:
            failed.append('describe_vpc_classic_link_dns_support')
        try:
            self.ec2_responses['vpc_endpoint_connection_notifications']                            = self.ec2.describe_vpc_endpoint_connection_notifications()
        except:
            failed.append('describe_vpc_endpoint_connection_notifications')
        try:
            self.ec2_responses['vpc_endpoint_connections']                                         = self.ec2.describe_vpc_endpoint_connections()
        except:
            failed.append('describe_vpc_endpoint_connections')
        try:
            self.ec2_responses['vpc_endpoint_service_configurations']                              = self.ec2.describe_vpc_endpoint_service_configurations()
        except:
            failed.append('describe_vpc_endpoint_service_configurations')
        try:
            self.ec2_responses['vpc_endpoint_service_permissions']                                 = self.ec2.describe_vpc_endpoint_service_permissions()
        except:
            failed.append('describe_vpc_endpoint_service_permissions')
        try:
            self.ec2_responses['vpc_endpoint_services']                                            = self.ec2.describe_vpc_endpoint_services()
        except:
            failed.append('describe_vpc_endpoint_services')
        try:
            self.ec2_responses['vpc_endpoints']                                                    = self.ec2.describe_vpc_endpoints()
        except:
            failed.append('describe_vpc_endpoints')
        try:
            self.ec2_responses['vpc_peering_connections']                                          = self.ec2.describe_vpc_peering_connections()
        except:
            failed.append('describe_vpc_peering_connections')
        try:
            self.ec2_responses['vpcs']                                                             = self.ec2.describe_vpcs()
        except:
            failed.append('describe_vpcs')
        try:
            self.ec2_responses['vpn_connections']                                                  = self.ec2.describe_vpn_connections()
        except:
            failed.append('describe_vpn_connections')
        try:
            self.ec2_responses['vpn_gateways']                                                     = self.ec2.describe_vpn_gateways()
        except:
            failed.append('describe_vpn_gateways')    

        try:
            self.ec2_responses['enableDnsSupport']                 = []
            self.ec2_responses['enableDnsHostnames']               = []
            self.ec2_responses['enableNetworkAddressUsageMetrics'] = []

            for jvpc in range(len(self.ec2_responses['vpcs']['Vpcs'])):
                vpc_id = self.ec2_responses['vpcs']['Vpcs'][jvpc]['VpcId']
                self.ec2_responses['enableDnsSupport'].append(
                                                                self.ec2.describe_vpc_attribute(Attribute='enableDnsSupport',
                                                                                                VpcId=vpc_id))
                self.ec2_responses['enableDnsHostnames'].append(
                                                                self.ec2.describe_vpc_attribute(Attribute='enableDnsHostnames',
                                                                                                VpcId=vpc_id))
                self.ec2_responses['enableNetworkAddressUsageMetrics'].append(
                                                                self.ec2.describe_vpc_attribute(Attribute='enableNetworkAddressUsageMetrics',
                                                                                                VpcId=vpc_id))                                
        except:
            failed.append('describe_vpc_attribute')                


        self.ec2_responses_failed = failed