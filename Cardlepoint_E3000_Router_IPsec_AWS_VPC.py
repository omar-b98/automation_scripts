from sdk.app_template_csclient.csclient import CSClient
import boto3
import json
import time
import xmltodict
import ipaddress

Cradlepoint_router_public_ip = '166.157.83.227'

aws_public_ip = "x.x.x.x"

myPassPhrase = "x"
aws_lan_net = "172.31.0.0/16"
ipsecname = "x"

TAGS = [[{'Key': 'Name', 'Value': 'xx'}],
        [{'Key': 'Name', 'Value': 'xx'}],
        [{'Key': 'Name', 'Value': 'xx'}]]

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
                "ip_network": "0.0.0.0/0",
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

    vpn_data["name"] = ipsecname

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
    global ipsecname
    global TAGS
    '''
    profile_name = "waltham.5glabs"#input("Enter AWS profile name: (eg:omarb98)\n")
    myRegion = "us-east-1"#input("Enter region: (eg:us-east-2)\n")
    vpcTag = "Test-VPC"#input("Enter VPC tag: (eg:VPC-test2)\n")
    myRouteTable = "Test-Private-rtb"#input("Enter route table tag: (eg:vpc-test2-route-table) \n")
    TAGS[0][0]["Value"] = input("Enter Customer Gateway tag name : \n")
    TAGS[1][0]["Value"] = input("Enter Virtual Private Gateway tag name : \n")
    TAGS[2][0]["Value"] = input("Enter VPN tag name : \n")
    
    Cradlepoint_router_public_ip = "63.47.184.88"#str(input("Enter e3000 router public ip address (eg:166.157.83.226) \n"))
    ipsecname = "test99"#input("Enter e3000 router ipsec tunnel name\n")

    #**********************************************default*********************************************************************
    profile_name = input("Enter AWS profile name: (eg:omarb98)\n")
    myRegion = input("Enter region: (eg:us-east-2)\n")
    vpcTag = input("Enter VPC tag: (eg:VPC-test2)\n")
    myRouteTable = input("Enter route table tag: (eg:vpc-test2-route-table) \n")
    TAGS[0][0]["Value"] = input("Enter Customer Gateway tag name : \n")
    TAGS[2][0]["Value"] = input("Enter VPN tag name : \n")
    
    Cradlepoint_router_public_ip = str(input("Enter e3000 router public ip address (eg:166.157.83.226) \n"))
    ipsecname = input("Enter e3000 router ipsec tunnel name\n")
    '''
    profile_name = "omarb98"  # input("Enter AWS profile name: (eg:omarb98)\n")
    myRegion = "us-west-2"  # input("Enter region: (eg:us-east-2)\n")
    vpcTag = "VPC-test2"  # input("Enter VPC tag: (eg:VPC-test2)\n")
    myRouteTable = "vpc-test2-route-table"  # input("Enter route table tag: (eg:vpc-test2-route-table) \n")
    TAGS[0][0]["Value"] = "mycgw"  # input("Enter Customer Gateway tag name : \n")
    TAGS[2][0]["Value"] = "myvpn"  # input("Enter VPN tag name : \n")

    Cradlepoint_router_public_ip = "63.47.184.88"  # str(input("Enter e3000 router public ip address (eg:166.157.83.226) \n"))
    ipsecname = "test99"  # input("Enter e3000 router ipsec tunnel name\n")

    boto3.setup_default_session(profile_name=profile_name)
    ec2 = boto3.resource('ec2', region_name=myRegion)
    client = boto3.client('ec2', region_name=myRegion)

    filters = [{'Name': 'tag:Name', 'Values': [vpcTag]}]
    vpcs = list(ec2.vpcs.filter(Filters=filters))

    for vpc in vpcs:
        myVpc = vpc.id

    print("\nVPC ID:", myVpc)

    myVGW = None
    for vpg in client.describe_vpn_gateways()["VpnGateways"]:
        for vpcAtt in vpg["VpcAttachments"]:
            if vpcAtt["VpcId"] == myVpc and vpcAtt["State"] == "attached":
                myVGW = vpg["VpnGatewayId"]
    if not myVGW:
        TAGS[1][0]["Value"] = input(
            "VPC " + myVpc + " is not attached to a Virtual Private Gateway \n Enter Virtual Private Gateway tag name : \n")

    response = client.describe_route_tables()

    for routes in response["RouteTables"]:
        for myTags in routes["Tags"]:
            if myTags["Key"] == "Name" and myTags["Value"] == myRouteTable:
                myRouteID = routes["RouteTableId"]

    print("Route Table ID: ", myRouteID)

    #
    # 1. create a customer gateway CGW
    #

    response = client.create_customer_gateway(

        BgpAsn=65000,
        PublicIp=Cradlepoint_router_public_ip,
        Type='ipsec.1',
        DeviceName='CradlepointE3000Router_VPN_' + TAGS[2][0]["Value"],
        DryRun=False
    )

    print("\nCustomer Gateway result:")
    print(json.dumps(response["CustomerGateway"], sort_keys=True, indent=4))
    print("Customer GatewayID:", response["CustomerGateway"]["CustomerGatewayId"])
    myCGW = response["CustomerGateway"]["CustomerGatewayId"]
    client.create_tags(Tags=TAGS[0], Resources=[myCGW])
    #
    # 2. Create Virtual Private Gateway VPG
    #
    if not myVGW:
        response = client.create_vpn_gateway(
            Type='ipsec.1',
        )

        print("\nVirtual Private Gateway result:")
        print(json.dumps(response["VpnGateway"], sort_keys=True, indent=4))
        print("VGW ID:", response["VpnGateway"]["VpnGatewayId"])
        myVGW = response["VpnGateway"]["VpnGatewayId"]

        client.create_tags(Tags=TAGS[1], Resources=[myVGW])
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

    client.create_tags(Tags=TAGS[2], Resources=[myVPN])

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
    input("block")
    Cradlepoint_router_vpn()
    print("\n VPN Tunnel is Configured!")
    input("Press enter to close")
