#!/usr/bin/env bash

if [[ -z ${1+.} ]]; then
	echo "URI not specified."
	exit 1
fi

uri=$1
echo "Waiting for OK response from '${uri}'."
curl=$(type -P curl) || exit

until response=$("${curl}" -s -o /dev/null -w "%{http_code}" "${uri}") &>/dev/null &&
		[[ ${response} == 200 ]]; do
	sleep 1
done
