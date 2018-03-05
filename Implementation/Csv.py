import sys
import re
import csv
import getopt
#import ConfigParser
import fileinput
import codecs
import time
import datetime
import warnings
#import urllib2

import rdflib

from rdflib import RDF, RDFS
from rdflib.namespace import split_uri


_all__ = [ 'CSV2RDF' ]

HELP = """
csv2rdf.py \
    -b <instance-base> \
    -p <property-base> \
    [-c <classname>] \
    [-i <identity column(s)>] \
    [-l <label columns>] \
    [-s <N>] [-o <output>] \
    [-f configfile] \
    [--col<N> <colspec>] \
    [--prop<N> <property>] \
    <[-d <delim>] \
    [-C] [files...]"

Reads csv files from stdin or given files
if -d is given, use this delimiter
if -s is given, skips N lines at the start
Creates a URI from the columns given to -i, or automatically by numbering if
none is given
Outputs RDFS labels from the columns given to -l
if -c is given adds a type triple with the given classname
if -C is given, the class is defined as rdfs:Class
Outputs one RDF triple per column in each row.
Output is in n3 format.
Output is stdout, unless -o is specified

Long options also supported: \
    --base, \
    --propbase, \
    --ident, \
    --class, \
    --label, \
    --out, \
    --defineclass

Long options --col0, --col1, ...
can be used to specify conversion for columns.
Conversions can be:
    float(), int(), split(sep, [more]), uri(base, [class]), date(format)

Long options --prop0, --prop1, ...
can be used to use specific properties, rather than ones auto-generated
from the headers

-f says to read config from a .ini/config file - the file must contain one
section called csv2rdf, with keys like the long options, i.e.:

[csv2rdf]
out=output.n3
base=http://example.org/
col0=split(";")
col1=split(";", uri("http://example.org/things/",
                    "http://xmlns.com/foaf/0.1/Person"))
col2=float()
col3=int()
col4=date("%Y-%b-%d %H:%M:%S")

"""

# bah - ugly global
uris = {}


def toProperty(label):
    """
    CamelCase + lowercase inital a string


    FIRST_NM => firstNm

    firstNm => firstNm

    """
    label = re.sub("[^\w]", " ", label)
    label = re.sub("([a-z])([A-Z])", "\\1 \\2", label)
    label = label.split(" ")
    return "".join([label[0].lower()] + [x.capitalize() for x in label[1:]])


def toPropertyLabel(label):
    if not label[1:2].isupper():
        return label[0:1].lower() + label[1:]
    return label


def index(l, i):
    """return a set of indexes from a list
    >>> index([1,2,3],(0,2))
    (1, 3)
    """
    return tuple([l[x] for x in i])


def csv_reader(csv_data, dialect=csv.excel, **kwargs):

    csv_reader = csv.reader(csv_data,
                            dialect=dialect, **kwargs)
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield [unicode(cell, 'utf-8', errors='replace') for cell in row]


def prefixuri(x, prefix, class_=None):
    if prefix:
        r = rdflib.URIRef(
            prefix + urllib2.quote(
                x.encode("utf8").replace(" ", "_"), safe=""))
    else:
        r = rdflib.URIRef(x)
    uris[x] = (r, class_)
    return r

# meta-language for config


class NodeMaker(object):
    def range(self):
        return rdflib.RDFS.Literal

    def __call__(self, x):
        return rdflib.Literal(x)


class NodeUri(NodeMaker):
    def __init__(self, prefix, class_):
        self.prefix = prefix
        if class_:
            self.class_ = rdflib.URIRef(class_)
        else:
            self.class_ = None

    def __call__(self, x):
        return prefixuri(x, self.prefix, self.class_)

    def range(self):
        return self.class_ or rdflib.RDF.Resource


class NodeLiteral(NodeMaker):
    def __init__(self, f=None):
        self.f = f


class NodeFloat(NodeLiteral):
    def __call__(self, x):
        if not self.f:
            return rdflib.Literal(float(x))
        if callable(self.f):
            return rdflib.Literal(float(self.f(x)))
        raise Exception("Function passed to float is not callable")

    def range(self):
        return rdflib.XSD.double


class NodeInt(NodeLiteral):
    def __call__(self, x):
        if not self.f:
            return rdflib.Literal(int(x))
        if callable(self.f):
            return rdflib.Literal(int(self.f(x)))
        raise Exception("Function passed to int is not callable")

    def range(self):
        return rdflib.XSD.int


class NodeReplace(NodeMaker):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __call__(self, x):
        return x.replace(self.a, self.b)


class NodeDate(NodeLiteral):
    def __call__(self, x):
        return rdflib.Literal(datetime.datetime.strptime(x, self.f))

    def range(self):
        return rdflib.XSD.dateTime


class NodeSplit(NodeMaker):
    def __init__(self, sep, f):
        self.sep = sep
        self.f = f

    def __call__(self, x):
        if not self.f:
            self.f = rdflib.Literal
        if not callable(self.f):
            raise Exception("Function passed to split is not callable!")
        return [
            self.f(y.strip()) for y in x.split(self.sep) if y.strip() != ""]

    def range(self):
        if self.f and isinstance(self.f, NodeMaker):
            return self.f.range()
        return NodeMaker.range(self)

default_node_make = NodeMaker()


def _config_ignore(*args, **kwargs):
    return "ignore"


def _config_uri(prefix=None, class_=None):
    return NodeUri(prefix, class_)


def _config_literal():
    return NodeLiteral


def _config_float(f=None):
    return NodeFloat(f)


def _config_replace(a, b):
    return NodeReplace(a, b)


def _config_int(f=None):
    return NodeInt(f)


def _config_date(format_):
    return NodeDate(format_)


def _config_split(sep=None, f=None):
    return NodeSplit(sep, f)

config_functions = {"ignore": _config_ignore,
                    "uri": _config_uri,
                    "literal": _config_literal,
                    "float": _config_float,
                    "int": _config_int,
                    "date": _config_date,
                    "split": _config_split,
                    "replace": _config_replace
                    }


def column(v):
    """Return a function for column mapping"""

    return eval(v, config_functions)


class CSV2RDF(object):
    def __init__(self):

        self.CLASS = None
        self.BASE = None
        self.PROPBASE = None
        self.IDENT = 'auto'
        self.LABEL = None
        self.DEFINECLASS = False
        self.SKIP = 0
        self.DELIM = ","

        self.COLUMNS = {}
        self.PROPS = {}

        self.OUT = codecs.getwriter("utf-8")(sys.stdout, errors='replace')

        self.triples = 0

