from sdk.app_template_csclient.csclient import CSClient

CSCinstance = CSClient("E3000 Router API IPsec configuration")

VPN_API_Config_URL = '/config/vpn/tunnels/'

Connection_Test_URL = '/status/wan/connection_state'

VPN_API_Status_URL = '/status/vpn/tunnels/'

VPN_Data = {
    "responder_mode": False,
    "enabled": True,
    "wan_trigger_field": "uid",
    "wan_trigger_predicate": "is",
    "wan_trigger_neg": False,
    "local_identity": "",
    "local_identity_type": "auto",
    "remote_identity": "",
    "remote_identity_type": "auto",
    "auth_method": "pre_shared_key",
    "mode": "tunnel",
    "ike_version": 1,
    "mobike": True,
    "protocol": "any",
    "initiator_mode": "demand",
    "remote_port": 500,
    "ike1_exchange_mode": "main",
    "ike1_encryption": "aes 128,aes 256",
    "ike1_hash": "sha256,sha384,sha512",
    "ike1_dh_group": "5",
    "ike1_key_lifetime": 28800,
    "ike2_encryption": "aes 128,aes 256",
    "ike2_hash": "hmac_sha256,hmac_sha384,hmac_sha512",
    "ike2_dh_group": "5",
    "ike2_key_lifetime": 3600,
    "ike2_pfs": True,
    "ike2_split_ts": False,
    "fail_over_to": "",
    "fail_back_to": "",
    "fail_back_period": 10,
    "dpd_enabled": True,
    "dpd_conn_idle_time": 30,
    "dpd_request_freq": 15,
    "dpd_max_requests": 5,
    "no_dhcp": False,
    "interface_ip_mode": "local",
    "interface_nat": False,
    "name": "Test0",
    "preshared_key": "123",
    "remote_gateway": "gate",
    "local_network": [],
    "remote_network": [],
    "vti_routes": [],
    "interface_ips": [
        {},
        {}
    ],
    "pools": [
        {},
        {}
    ],
    "ipverify": [
        {
            "test_id": "",
            "on_pass": False,
            "change_tunnel_state": "connect"
        },
        {
            "test_id": "",
            "on_pass": False,
            "change_tunnel_state": "connect"
        }
    ]
}

Router_Connection_Status = CSCinstance.get(Connection_Test_URL)

print("Router_Connection_Status :\n", Router_Connection_Status)

Add_VPN_Response = CSCinstance.post(VPN_API_Config_URL, VPN_Data)

print("Add_VPN_Response :\n", Add_VPN_Response)

Get_Configured_VPNs = CSCinstance.get(VPN_API_Config_URL)

print("Get_Configured_VPNs :\n", Get_Configured_VPNs)

Get_VPNs_Status = CSCinstance.get(VPN_API_Status_URL)

print("Get_VPNs_Status :\n", Get_VPNs_Status)
