"""Tests for Shaarli client utilities"""
# pylint: disable=invalid-name
from argparse import ArgumentParser
from unittest import mock

from shaarli_client.utils import generate_endpoint_parser


@mock.patch('argparse.ArgumentParser.add_argument')
def test_generate_endpoint_parser_noparam(addargument):
    """Generate a parser from endpoint metadata - no params"""
    name = 'put-stuff'
    metadata = {
        'path': 'stuff',
        'method': 'PUT',
        'help': "Changes stuff",
        'params': {},
    }
    parser = ArgumentParser()
    subparsers = parser.add_subparsers()

    generate_endpoint_parser(subparsers, name, metadata)

    addargument.assert_has_calls([
        # first helper for the main parser
        mock.call('-h', '--help', action='help',
                  default=mock.ANY, help=mock.ANY),

        # second helper for the 'put-stuff' subparser
        mock.call('-h', '--help', action='help',
                  default=mock.ANY, help=mock.ANY)
    ])


@mock.patch('argparse.ArgumentParser.add_argument')
def test_generate_endpoint_parser_single_param(addargument):
    """Generate a parser from endpoint metadata - single param"""
    name = 'get-stuff'
    metadata = {
        'path': 'stuff',
        'method': 'GET',
        'help': "Gets stuff",
        'params': {
            'param1': {
                'help': "First param",
            },
        },
    }
    parser = ArgumentParser()
    subparsers = parser.add_subparsers()

    generate_endpoint_parser(subparsers, name, metadata)

    addargument.assert_has_calls([
        # first helper for the main parser
        mock.call('-h', '--help', action='help',
                  default=mock.ANY, help=mock.ANY),

        # second helper for the 'put-stuff' subparser
        mock.call('-h', '--help', action='help',
                  default=mock.ANY, help=mock.ANY),

        # param1
        mock.call('--param1', help="First param")
    ])


@mock.patch('argparse.ArgumentParser.add_argument')
def test_generate_endpoint_parser_multi_param(addargument):
    """Generate a parser from endpoint metadata - multiple params"""
    name = 'get-stuff'
    metadata = {
        'path': 'stuff',
        'method': 'GET',
        'help': "Gets stuff",
        'params': {
            'param1': {
                'help': "First param",
                'type': int,
            },
            'param2': {
                'choices': ['a', 'b', 'c'],
                'help': "Second param",
                'nargs': '+',
            },
        },
    }
    parser = ArgumentParser()
    subparsers = parser.add_subparsers()

    generate_endpoint_parser(subparsers, name, metadata)

    addargument.assert_has_calls([
        # first helper for the main parser
        mock.call('-h', '--help', action='help',
                  default=mock.ANY, help=mock.ANY),

        # second helper for the 'put-stuff' subparser
        mock.call('-h', '--help', action='help',
                  default=mock.ANY, help=mock.ANY),

        # param1
        mock.call('--param1', help="First param", type=int),

        # param2
        mock.call('--param2', choices=['a', 'b', 'c'],
                  help="Second param", nargs='+')
    ])


@mock.patch('argparse.ArgumentParser.add_argument')
def test_generate_endpoint_parser_resource(addargument):
    """Generate a parser from endpoint metadata - API resource"""
    name = 'get-stuff'
    metadata = {
        'path': 'stuff',
        'method': 'GET',
        'help': "Gets stuff",
        'resource': {
            'help': "API resource",
            'type': int,
        },
        'params': {},
    }
    parser = ArgumentParser()
    subparsers = parser.add_subparsers()

    generate_endpoint_parser(subparsers, name, metadata)

    addargument.assert_has_calls([
        # first helper for the main parser
        mock.call('-h', '--help', action='help',
                  default=mock.ANY, help=mock.ANY),

        # second helper for the 'put-stuff' subparser
        mock.call('-h', '--help', action='help',
                  default=mock.ANY, help=mock.ANY),

        # resource
        mock.call('resource', help="API resource", type=int)
    ])
