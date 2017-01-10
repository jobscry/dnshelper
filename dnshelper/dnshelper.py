#! /usr/bin/env python

import click
import dns.resolver
from geoip import geolite2


class DNSHelper(object):
	def __init__(self, host='google.com', geo_lookup=False):
		self.host = host
		self.geo_lookup = geo_lookup

@click.group()
@click.argument('host')
@click.option('--geo_lookup', is_flag=True, help="Country lookup?")
@click.pass_context
def cli(ctx, host, geo_lookup):
	ctx.obj = DNSHelper(host, geo_lookup)

@cli.command()
@click.pass_obj
def mx_lookup(obj):
	"""Get MX records as list of IPs"""
	_lookups(first_type='MX')

@click.pass_obj
def _lookups(obj, first_type):
	lookups = [(obj.host, first_type)]
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