#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Michelin Guide data preprocessor.
Parses XML data and exports addresses and coordinates
"""
import os
import csv
from glob import glob
from xml.etree.ElementTree import parse


class MGPreprocessor:
    """ Michelin Guide data preprocessor """

    def preprocess(self, input, output_filename, sample_rate=1):
        """ Extract a  data from xml file and store in csv file."""
        outdir = os.path.join(os.getcwd(), "test_data", "output")
        if not os.path.isdir(outdir):
            os.mkdir(outdir)

        input_filenames = glob(input)
        for filename in input_filenames:
            basename = os.path.basename(filename)
            fname = basename.split('_')[-2]
            fname = os.path.join(outdir, "%s_poi.csv" % fname)
            with open(fname, "w", encoding="utf-8") as output_file:
                out_writer = csv.writer(
                    output_file,
                    delimiter=",",
                    quotechar="|",
                    quoting=csv.QUOTE_MINIMAL,
                    lineterminator="\n",
                )
                # Adding columns to output file
                out_writer.writerow(
                    [
                        "latitude", "longitude",
                        "name", "street", "city", "country", "postal_code",
                        "local_phone", "int_phone", "e164_phone",
                        "email", "web"
                    ]
                )
                print("Storing '%s' file records into '%s' file..." % (
                        os.path.basename(filename),
                        os.path.basename(fname)
                    )
                )
                with open(filename, "rb") as xf:
                    xml_tree = parse(xf)
                    root = xml_tree.getroot()
                    for xoi in root.findall("xoi"):
                        lat = float(xoi.find("geoposition").find(
                            "lat").text)
                        lon = float(xoi.find("geoposition").find(
                            "lon").text)
                        main_info = xoi.find("main_information")
                        street = getattr(
                            main_info.find('street'), 'text', None
                        )
                        city = getattr(main_info.find('city'), 'text', None)
                        pc = getattr(main_info.find('postcode'), 'text', None)
                        country = getattr(
                            main_info.find('country'), 'text', None
                        )
                        local_ph = getattr(
                            main_info.find('local_phone1'), 'text', None
                        )
                        int_ph = getattr(
                            main_info.find('int_phone1'), 'text', None
                        )
                        el_phone = getattr(
                            main_info.find('e164_phone1'), 'text', None
                        )
                        name = getattr(main_info.find('name'), 'text', None)
                        email = getattr(main_info.find('email'), 'text', None)
                        web = getattr(main_info.find('web'), 'text', None)
                        out_writer.writerow(
                            [
                                lat, lon,
                                name, street, city, country, pc,
                                local_ph, int_ph, el_phone,
                                email, web]
                        )
                print(
                    "Process of storing '%s' file records into '%s'" % (
                        os.path.basename(filename),
                        os.path.basename(fname)
                    ),
                    "file was complete."
                )


if __name__ == '__main__':
    inp = "%s/test_data/*.xml" % (os.getcwd())
    out = "%s/test_data/gm_digest.csv" % (os.getcwd())
    MGPreprocessor().preprocess(inp, out, 5 / 100)
