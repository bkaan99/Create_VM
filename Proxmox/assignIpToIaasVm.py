import requests

def assign_ip_to_proxmox_iaas_vm(headersWithCookie,vmid, ipAddress, netMask, gateWay, nodename, serverOs):
    nodename = "nestedproxmox01" #@TODO Nodaneme generic olacak
    #@TODO Commandler sudoerse göre güncelelenecektir.
    if serverOs == "Windows 2018 ":
        commandToAddIP = 'netsh interface ip set address name="Ethernet" static '+ ipAddress + ' ' + netMask + ' ' + gateWay
        #commandToAddIP = "ipconfig"
    elif serverOs == "Linux":
        commandToAddIP = "ip addr del" + ipAddress + "/24 dev ens18 "
        commandToSetGateWay = "ip route add default via " + gateWay


    run_agent_for_ip_operations_config = {
        "command": commandToAddIP,
        #"vmid": vmid,
        "node": nodename
    }


    setIpOnGivenVmWithAgent = requests.post(
        "https://10.14.46.11:8006/api2/extjs/nodes/nestedproxmox01/qemu/" + str(int(vmid) + 100) + "/agent/exec",
        headers=headersWithCookie, verify=False, json=run_agent_for_ip_operations_config)
    if serverOs=="Linux":
        run_agent_for_ip_operations_gateway_config = {
            "command": commandToSetGateWay,
            "vmid": vmid,
            "node": nodename,
        }
        setGatewayOnGivenVmWithAgent = requests.post(
            "https://10.14.46.11:8006/api2/extjs/nodes/nestedproxmox01/qemu/" + str(vmid + 100) + "/agent/exec",
            headers=headersWithCookie, verify=False, json=run_agent_for_ip_operations_gateway_config)