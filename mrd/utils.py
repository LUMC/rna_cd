"""
mrd
Copyright (C) 2018  Leiden University Medical Center, Sander Bollen

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import datetime
import click


def echo(msg: str):
    """Wrapper around click.secho to include datetime"""
    fmt = "[ {0} ] {1}".format(str(datetime.datetime.utcnow()), msg)
    click.secho(fmt, fg="green", err=True)
