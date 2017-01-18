# -*- coding: utf-8 -*-
#! /usr/bin/env python
'''
Finds all IPs that can send/recieve email from a FQDN via the DNS records.
Will continue to resolve hostnames until an IP is found.
'''
import click
import dns.resolver
import ipaddress
from geoip import geolite2
from SPF2IP import SPF2IP


class DNSHelper(object):
    '''DNS Helper

    Helper object for click grouping.
    '''
    def __init__(self, host='google.com', geo_lookup=False):
        self.host = host
        self.geo_lookup = geo_lookup


@click.group()
@click.argument('host')
@click.option('--geo_lookup', is_flag=True, help="Country lookup?")
@click.pass_context
def cli(ctx=None, host=None, geo_lookup=None):
    '''cli

    Entry point for click group.
    '''
    ctx.obj = DNSHelper(host, geo_lookup)


@cli.command()
def mx_lookup():
    """Get MX records as list of IPs"""
    _lookups(None, first_type='MX')


@cli.command()
@click.pass_obj
def spf_lookup(obj):
    """Lookup SPF record, generate list of IPs."""
    lookup = SPF2IP(obj.host)
    for addr in lookup.IPArray():
        click.echo(_echo_ip(addr, obj.geo_lookup))


@click.pass_obj
def _lookups(obj, first_type):
    '''_lookups

    Internal helper for performing lookups.
    '''
    lookups = [(obj.host, first_type)]
    while lookups:
        lookup = lookups.pop()
        answers = dns.resolver.query(lookup[0], lookup[1])
        for answer in answers:
            if hasattr(answer, 'address'):
                click.echo(_echo_ip(answer.address, obj.geo_lookup))
            else:
                lookups.append((answer.exchange.to_text(), 'A'))


def _echo_ip(display_address, geo_lookup=False):
    '''_echo ip

    Internal helper for echoing IP addresses.
    '''
    if '/' in display_address:
        if '/32' in display_address:
            lookup_address = display_address[0:-3]
        else:
            network = ipaddress.ip_network(display_address)
            lookup_address = str(next(network.hosts()))
    else:
        lookup_address = display_address
    if geo_lookup:
        match = geolite2.lookup(lookup_address)
        if match is not None:
            return '{0},{1}'.format(display_address, match.country)
    return display_address


if __name__ == '__main__':
    cli()
