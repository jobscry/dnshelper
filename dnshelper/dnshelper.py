#! /usr/bin/env python

import click
import dns.resolver
from geoip import geolite2


@click.command()
@click.argument('host')
@click.option('--first_type', default='MX', help="Initial lookup type (MX is default).")
@click.option('--geo_lookup', is_flag=True, help="Country lookup?")
def get_records(host, first_type, geo_lookup):
	"""Get DNS records as list of IPs"""
	lookups = [(host, first_type)]
	while lookups:
		lookup = lookups.pop()
		answers = dns.resolver.query(lookup[0], lookup[1])
		for answer in answers:
			if hasattr(answer, 'address'):
				if geo_lookup:
					address = answer.address
					match = geolite2.lookup(address)
					if match is not None:
						print('{0} {1}'.format(address, match.country))
				else:
					print answer.address
			else:
				lookups.append((answer.exchange.to_text(), 'A'))


if __name__ == '__main__':
	get_records()