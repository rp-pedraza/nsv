#!/usr/bin/env bash

shopt -s nullglob

# Set localhost as default server name
NSV_FRONTEND_SERVERNAME=${NSV_FRONTEND_SERVERNAME:-localhost}

# Set 80 as default port
NSV_FRONTEND_PORT=${NSV_FRONTEND_PORT:-80}

# Set 0.0.0.0 as default IP adddress
NSV_FRONTEND_IP=${NSV_FRONTEND_IP:-0.0.0.0}

# Set "[::]" as default IPv6 address
NSV_FRONTEND_IPV6=${NSV_FRONTEND_IPV6:-[::]}

# Process every template placed in /etc/nginx/conf.d/.
for TEMPLATE in /etc/nginx/conf.d/*.conf.template; do
	TARGET=${TEMPLATE%.template}

	# We always override possibly existing '.conf' files so it would
	# reflect changes in the values of NSV_FRONTEND_SERVERNAME, NSV_FRONTEND_IP, NSV_FRONTEND_IPV6,
	# and NSV_FRONTEND_PORT.

	# To prevent a .conf file from being updated, the corresponding
	# '.template' file should be removed.

	[[ ${NSV_FRONTEND_DEBUG} == true ]] && echo "Creating ${TARGET} based on ${TEMPLATE}."

	sed -e "s|<NSV_FRONTEND_SERVERNAME>|${NSV_FRONTEND_SERVERNAME}|g" \
			-e "s|<NSV_FRONTEND_IP>|${NSV_FRONTEND_IP}|g" \
			-e "s|<NSV_FRONTEND_IPV6>|${NSV_FRONTEND_IPV6}|g" \
			-e "s|<NSV_FRONTEND_PORT>|${NSV_FRONTEND_PORT}|g" \
			"${TEMPLATE}" > "${TARGET}"

	# Dump the content to screen if NSV_FRONTEND_DEBUG is set to 'true'.

	if [[ ${NSV_FRONTEND_DEBUG} == true ]]; then
		MSG="----- ${TARGET} -----"
		echo "${MSG}"
		cat "${TARGET}"
		echo "${MSG//?/-}"
	fi
done
