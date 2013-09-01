import re

from django.template.base import kwarg_re, TemplateSyntaxError, FilterExpression
from django.template import Variable, VariableDoesNotExist

QUOTED_STRING = re.compile(r'^["\'](?P<noquotes>.+)["\']$')


def handle_var(value, context):
    if isinstance(value, FilterExpression) or isinstance(value, Variable):
        return value.resolve(context)
    stringval = QUOTED_STRING.search(value)
    if stringval:
        return stringval.group('noquotes')
    else:
        try:
            return Variable(value).resolve(context)
        except VariableDoesNotExist:
            return value


def parse_token_contents(parser, token):
    bits = token.split_contents()
    tag = bits.pop(0)
    args = []
    kwargs = {}
    asvar = None
    if len(bits) >= 2 and bits[-2] == 'as':
        asvar = bits[-1]
        bits = bits[:-2]
    if len(bits):
        for bit in bits:
            match = kwarg_re.match(bit)
            if not match:
                raise TemplateSyntaxError('Malformed arguments to tag "%s"' % tag)
            name, value = match.groups()
            if name:
                kwargs[name] = parser.compile_filter(value)
            else:
                args.append(parser.compile_filter(value))
    return {
        'tag': tag,
        'args': args,
        'kwargs': kwargs,
        'asvar': asvar,
    }


