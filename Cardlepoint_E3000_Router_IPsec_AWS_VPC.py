# Cradlepoint info step
# -----------------------------------
# 1. Connect to distance Cradlepoint router using its public address
#
# AWS VPN creation steps
# -----------------------------------
# 1. Create Customer Gateway
# 2. Create Virtual Private Gateway
# 3. Attach VGW to VPC
# 4. Create VPN Connection using CGW + VPG
# 5. View Downloaded config with public IP and password
# 6. Add LAN routes to VPN table
# 7. Propogate VPC subnet into VPG
#
# Cradlepoint VPN Creation step
# ------------------------------------
# 1. create json data of VPN
# 2. send VPN data of the IPsec configuration using SDK functions
#
# AWS Code
# ------------------------------------
# awscli multiple profiles managed in the 2 files config and credentials in C:\Users\[user]\.aws\
# manually edit the files, or use '$ aws configure --profile profilename
#
# BOTO3 ec2 guide - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html
#
#
# Cradlepoint Code
# ------------------------------------
# API Guide - https://customer.cradlepoint.com/s/article/NCOS-SDK-v2-0-Application-Development-Guide
# Built on SDK v2.0 (https://github.com/cradlepoint/sdk-samples)
#

from sdk.app_template_csclient.csclient import CSClient
import boto3
import json
import time
import xmltodict
import ipaddress

# Cradlepoint router informations, already mentioned in sdk setting file
app_name = 'app_template_csclient'
dev_client_username = 'admin'
dev_client_ip = '166.157.83.227:8080'
dev_client_password = 'WA2017RA002161'

Cradlepoint_router_public_ip = '166.157.83.227'

# Cradlepoint router lans as an example
Primary_LAN = "192.168.1.0/24"
Guest_LAN = "192.168.10.0/24"
Deep = "192.168.196.0/24"

aws_public_ip = "x.x.x.x"

myPassPhrase = "x"
# my_aws_lan_subnet = ['10.100.0.0/24']  AWS VPC subnet (VPC->subnets) [REQUIRED]

cscinstance = CSClient("e3000 router api ipsec configuration")


def get_local_lans_cradlepoint_router():
    local_lans_cradlepoint_router = []

    lan_url = '/status/lan'

    for i in cscinstance.get(lan_url)["networks"].values():
        local_lans_cradlepoint_router.append(', '.join(i["info"]["ip_addresses"]))

    return local_lans_cradlepoint_router


def Cradlepoint_router_vpn():
    vpn_api_config_url = '/config/vpn/tunnels/'

    vpn_data = {
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
        "initiator_mode": "always",
        "remote_port": 500,
        "ike1_exchange_mode": "main",
        "ike1_encryption": "aes 128",
        "ike1_hash": "sha1",
        "ike1_dh_group": "2",
        "ike1_key_lifetime": 28800,
        "ike2_encryption": "aes 128",
        "ike2_hash": "hmac_sha1",
        "ike2_dh_group": "2",
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
        "name": "Test1",
        "remote_gateway": aws_public_ip,
        "anonymous": False,
        "preshared_key": myPassPhrase,
        "router_services": False,
        "local_network": [
            {
                "ip_network": "192.168.1.0/24",
                "port": None,
                "nat_to": "",
                "exclude": False
            }
        ],
        "remote_network": [
            {
                "ip_network": "10.0.0.0/24",
                "port": None,
                "exclude": False
            }
        ],
        "vti_routes": [

        ],
        "interface_ips": [
            {

            },
            {

            }
        ],
        "pools": [
            {

            },
            {

            }
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

    vpn_data["name"] = input("Enter e3000 router ipsec tunnel name\n")

    # vpn_data["local_network"][0]["exclude"] = true
    # vpn_data["remote_gateway"] = aws_public_ip

    add_vpn_response = cscinstance.post(vpn_api_config_url, vpn_data)

    if add_vpn_response["success"]:
        print("Cradlepoint router VPN created successfully!\n")
    else:
        print(add_vpn_response["data"]["reason"])


def aws_vpn():
    # ---------------------------------------------
    global Cradlepoint_router_public_ip
    global myPassPhrase
    global aws_public_ip

    profile_name = input("Enter aws profile name: (eg:omarb98)\n")
    vpcTag = input("Enter vpc tag: (eg:VPC-test)\n")
    myRegion = input("Enter region: (eg:us-east-2)\n")
    myRouteTable = input("Enter route table tag: (eg:vpc-test-route-table) \n")

    vpcTag = "VPC-test2"
    myRegion = "us-east-2"
    myRouteTable = "vpc-test2-route-table"

    boto3.setup_default_session(profile_name=profile_name)
    ec2 = boto3.resource('ec2', region_name=myRegion)
    client = boto3.client('ec2', region_name=myRegion)

    filters = [{'Name': 'tag:Name', 'Values': [vpcTag]}]
    vpcs = list(ec2.vpcs.filter(Filters=filters))

    for vpc in vpcs:
        myVpc = vpc.id
        # response = client.describe_vpcs(VpcIds=[vpc.id,])
        # print(json.dumps(response, sort_keys=True, indent=4))
    print("\nVPC ID:", myVpc)

    response = client.describe_route_tables()

    for routes in response["RouteTables"]:
        for myTags in routes["Tags"]:
            if myTags["Key"] == "Name" and myTags["Value"] == myRouteTable:
                myRouteID = routes["RouteTableId"]

    print("Route Table ID: ", myRouteID)

    #
    # 1. create a customer gateway (requires Meraki MX Public IP)
    #

    response = client.create_customer_gateway(
        BgpAsn=65000,
        PublicIp=Cradlepoint_router_public_ip,
        Type='ipsec.1',
        DeviceName='CradlepointE3000Router',
        DryRun=False
    )

    print("\nCustomer Gateway result:")
    print(json.dumps(response["CustomerGateway"], sort_keys=True, indent=4))
    print("Customer GatewayID:", response["CustomerGateway"]["CustomerGatewayId"])
    myCGW = response["CustomerGateway"]["CustomerGatewayId"]

    #
    # 2. Create Virtual Private Gateway
    #
    response = client.create_vpn_gateway(
        Type='ipsec.1',
    )

    print("\nVirtual Private Gateway result:")
    print(json.dumps(response["VpnGateway"], sort_keys=True, indent=4))
    print("VGW ID:", response["VpnGateway"]["VpnGatewayId"])
    myVGW = response["VpnGateway"]["VpnGatewayId"]

    #
    # 3. Attach VGW to VPC
    #
    response = client.attach_vpn_gateway(
        VpcId=myVpc,
        VpnGatewayId=myVGW
    )

    print("\nAttachement result:")
    print(json.dumps(response["VpcAttachment"], sort_keys=True, indent=4))
    print("Status:", response["VpcAttachment"]["State"])
    status = response["VpcAttachment"]["State"]
    print("Waiting for [attached] status (rechecking every 5s)")
    while status != "attached":
        time.sleep(5)
        response = client.describe_vpn_gateways(
            VpnGatewayIds=[
                myVGW,
            ],
        )

        for line in response["VpnGateways"]:
            for line2 in line["VpcAttachments"]:
                status = line2["State"]
                print("Status:", status)

    #
    # 4. Create VPN Connection using CGW + VPG
    # 5. Display VPN config data (public IP/passphrase)
    #
    response = client.create_vpn_connection(
        CustomerGatewayId=myCGW,
        Type='ipsec.1',
        VpnGatewayId=myVGW,
        Options={
            'StaticRoutesOnly': True
        }
    )

    myVPN = response["VpnConnection"]["VpnConnectionId"]
    print("VPN ID:", myVPN)
    print("\nVPN Configuration Data (showing VPN0)\n----------------------------------")

    doc = xmltodict.parse(response["VpnConnection"]["CustomerGatewayConfiguration"])
    #    print(json.dumps(doc, sort_keys=True, indent=4))
    for tunnels in doc["vpn_connection"]["ipsec_tunnel"]:
        print("VPN0 Passphrase:", tunnels["ike"]["pre_shared_key"])
        myPassPhrase = tunnels["ike"]["pre_shared_key"]
        print("VPN0 Public IP:", tunnels["vpn_gateway"]["tunnel_outside_address"]["ip_address"])
        aws_public_ip = tunnels["vpn_gateway"]["tunnel_outside_address"]["ip_address"]
        break

    #
    # 6. Add remote LAN routes to VPN table
    #
    client.create_vpn_connection_route(
        DestinationCidrBlock=str(ipaddress.ip_network(get_local_lans_cradlepoint_router()[0], strict=False)),
        VpnConnectionId=myVPN
    )

    #
    # 7. Propogate VPN routes to route table
    #
    client.enable_vgw_route_propagation(
        RouteTableId=myRouteID,
        GatewayId=myVGW
    )

    #
    # Wait for VPN to be ready to use
    #
    status = response["VpnConnection"]["State"]
    print("\nStatus:", status)
    print("Waiting for [available] status (rechecking every 30s)")
    while status != "available":
        time.sleep(30)
        response = client.describe_vpn_connections(
            VpnConnectionIds=[
                myVPN,
            ],
        )
        for line in response["VpnConnections"]:
            status = line["State"]
            print("Status:", status)


if __name__ == "__main__":
    aws_vpn()
    Cradlepoint_router_vpn()
    print("\n VPN Tunnel is Configured!")
    input("Press enter to close")
