import sys

from randblog.admin import parser

args = parser.parse_args()
args.func(args)

