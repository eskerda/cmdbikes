# -*- coding: utf-8 -*-

import itertools
import json

import citybikes
import click
import geocoder
import colorama
from iso3166 import countries

__version__ = '0.1.8'

client = citybikes.Client()

network_name_template = u'Found network: {0[name]}, {1[city]} ({1[country]})'
country_name_template = u'{} [{}]'

epilog = ''.join([
    """\b
Brought to you by the fine folks at Citybikes.
""", colorama.Fore.GREEN,
    """\b
    cccccccccccccccccccccccccccccccccccccccccc
    ccccccccccccccccccccc    cccccccc   cccccc
    ccccccccccccccccccccc    ccccccc     ccccc
    cccccccccc     cccccc        ccc     ccccc
    cccccccccc                   ccc      cccc
    cccccccccc                            cccc
    cccccccccc              cccc           ccc
    ccccc                 cc   cc            c
    ccccc                      ccc           c
    ccccc      cc               ccc          c
    ccccc      ccccccc     cccccccc          c
    c             cc   cccc  cccccc          c
    c             ccccc      cc  ccc         c
    c      cccccccc  cc   ccc   ccccccc      c
    c    ccc   ccccc  cccc     ccccc   cc    c
    c   ccc   cc  ccc cc      cc  cc    cc   c
    c   ccc       cc  cccc     c        cc   c
    c    ccc     ccc           ccccccccccc   c
    c     cccccccc                cccccc     c
    c                                        c
    ccccccccccccccccccccccc https://citybik.es

""", colorama.Style.RESET_ALL])


def get_color(number):
    if number > 5:
        return 'green'
    elif number > 1:
        return 'yellow'
    else:
        return 'red'


def format_address(loc):
    keys = [
        # Stupid ping pong to get readable address out of bike station osm
        # nodes. Nominatim seems to ignore osm_type query, which would make
        # things easier
        lambda addr: addr.get('address29') or addr.get('road'),
        'house_number',
        'postcode',
        'city'
    ]
    address = loc.raw['address']
    components = [k(address) if callable(k) else address.get(k) for k in keys]
    return ", ".join(filter(None, components))


def display_station(station, geocode=False, use_colors=False):
    bar_width = 30
    padding = ' ' * 1
    total_slots = station.get('extra', {}).get('slots')
    if not total_slots:
        if station['empty_slots']:
            total_slots = station['free_bikes'] + station['empty_slots']
        else:
            total_slots = 0

    total_slots = float(total_slots)
    bikes = int(station['free_bikes'])
    slots = int(station['empty_slots'] or 0)
    bikes_s = '%s bikes' % bikes
    slots_s = '%s slots' % slots

    try:
        perc = int((bikes/total_slots) * bar_width)
    except ZeroDivisionError:
        perc = 0
    status_bar = u'█' * perc + u'░' * (bar_width - perc)
    status_pad = (bar_width - len(bikes_s) - len(slots_s)) * ' '
    status = u''.join([
        click.style(bikes_s, fg=get_color(bikes)),
        status_pad,
        click.style(slots_s, fg=get_color(slots))
    ])

    if geocode:
        loc = geocoder.osm([station['latitude'], station['longitude']],
                           method='reverse')
        address = format_address(loc)
    else:
        address = 'lat, lng: {:.6f}, {:.6f}'.format(station['latitude'],
                                                    station['longitude'])
    click.echo(padding + station['name'].title(), color=use_colors)
    click.echo(click.style(padding + status_bar, fg=get_color(bikes)),
               color=use_colors)
    click.echo(click.style(padding + status), color=use_colors)
    click.echo(padding + address)


@click.group(epilog=epilog)
def cli():
    """A command line client for the Citybikes API."""
    pass


@click.command()
@click.argument('address', default=None)
@click.option('--geocode / --no-geocode', is_flag=True, default=True,
              help='Geocode station positions into a readable address')
@click.option('-n', default=5, help='Number of stations to show.', type=int)
@click.option('--color / --no-color', is_flag=True, default=True,
              help='Use colors on output')
@click.option('--json', 'output_json', is_flag=True, default=False,
              help='Return JSON representation')
def show(address, geocode, n, color, output_json):
    """Display status of station on a given address."""

    lat, lng = geocoder.osm(address).latlng
    network, distance = next(iter(client.networks.near(lat, lng)))

    if n == 0 or n > 10:
        click.echo('Disabling geocoder, too many stations to geocode',
                   err=True, color=color)
        geocode = False
    if n == 0:
        n = len(network.stations)

    stations = [s for s, d in network.stations.near(lat, lng)][:n]
    net_name = network_name_template.format(network, network['location'])

    click.echo(click.style(net_name, fg='green'), err=True, color=color)

    if output_json:
        click.echo(json.dumps(stations, cls=citybikes.resource.JSONEncoder,
                              indent=4))
        return

    for station in stations:
        display_station(station, geocode=geocode, use_colors=color)
        click.echo()


@click.command()
def ls():
    """List all bike sharing networks supported."""
    def get_ccode(network):
        return network['location']['country']

    def get_country(code):
        try:
            return countries.get(code.lower()).name
        except KeyError:
            return code
    # Create iter of (country, network)
    networks = ((get_country(get_ccode(n)), n) for n in client.networks)
    # Sort networks by country
    s_networks = sorted(networks, key=lambda cn: cn[0])
    # Group networks by country
    g_networks = itertools.groupby(s_networks, key=lambda cn: cn[0])
    for country, networks in g_networks:
        networks = [n for _, n in networks]
        click.echo(country_name_template.format(country, len(networks)))
        for i, n in enumerate(networks):
            name = u'{0[location][city]} ({0[name]})'.format(n)
            click.echo((u'├' if i < len(networks)-1 else u'└') + ' ' + name)
        click.echo()


cli.add_command(show)
cli.add_command(ls)

if __name__ == '__main__':
    cli()
