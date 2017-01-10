#! /usr/bin/env python

import click
import dns.resolver
from geoip import geolite2


class DNSHelper(object):
	def __init__(self, host='google.com', geo_lookup=False, first_type='MX'):
		self.host = host
		self.geo_lookup = geo_lookup
		self.first_type = first_type

@click.group()
@click.argument('host')
@click.option('--first_type', default='MX', help="Initial lookup type (MX is default).")
@click.option('--geo_lookup', is_flag=True, help="Country lookup?")
@click.pass_context
def cli(ctx, host, first_type, geo_lookup):
	ctx.obj = DNSHelper(host, geo_lookup, first_type)

@cli.command()
@click.pass_obj
def mx_lookup(obj):
	"""Get MX records as list of IPs"""
	obj.first_type = 'MX'
	_lookups()

@click.pass_obj
def _lookups(obj):
	lookups = [(obj.host, obj.first_type)]
	while lookups:
		lookup = lookups.pop()
		answers = dns.resolver.query(lookup[0], lookup[1])
		for answer in answers:
			if hasattr(answer, 'address'):
				if obj.geo_lookup:
					address = answer.address
					match = geolite2.lookup(address)
					if match is not None:
						print('{0} {1}'.format(address, match.country))
				else:
					print answer.address
			else:
				lookups.append((answer.exchange.to_text(), 'A'))


if __name__ == '__main__':
	cli()