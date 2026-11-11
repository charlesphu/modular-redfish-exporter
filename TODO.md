# TODO list

## Implement http client
1. deep expansion and filter properties
    - should use this only if bmc supports it
    - try: `curl -k -s -u "admin:password" https://<BMC_IP>/redfish/v1/ | jq .ProtocolFeaturesSupported`
    - otherwise direct testing:
        - select: `curl -k -I -u "admin:password" "https://<BMC_IP>/redfish/v1/Systems/1?\$select=PowerState"`
        - expand: `curl -k -I -u "admin:password" "https://<BMC_IP>/redfish/v1/Systems?\$expand=.(\$levels=1)"`
1. should keep connections allive
    - establish a session using `/redfish/v1/SessionService/Sessions`

## Check the telemntry service
`/redfish/v1/TelemetryService`

## Implement cache 
1. each bmc has its own cache on what paths to query
1. can cross compare with other bmc in the same space (rack or whatever)
1. refreshes its cashe every X minutes

## Bmc state collector
1. polls for health, power state, firmware status, hardware status, event logs, etc...