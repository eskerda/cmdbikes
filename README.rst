cmdbikes
========
Have you ever thought

    Damn, I wish I could check the status of my local bike
    sharing network on a terminal

Well, now with ``cmdbikes`` you can!

.. image:: http://i.imgur.com/3LJqFjp.gif

About
-----
This is a silly client to showcase `python-citybikes`_, a python wrapper for
the `Citybikes API`_. You can learn more about the project at
https://citybik.es.

If your network is not supported, add an issue or a PR on `pybikes`_.

.. _`python-citybikes`: http://github.com/eskerda/python-citybikes
.. _`Citybikes API`: https://api.citybik.es
.. _`pybikes`: http://github.com/eskerda/pybikes
Installation
------------
.. code-block::

    $ pip install cmdbikes

Usage
-------------
.. code-block::

    $ cmdbikes show --help
    Usage: cmdbikes show [OPTIONS] ADDRESS

      Display status of station on a given address.

    Options:
      --geocode / --no-geocode  Geocode station positions into a readable address
      -n INTEGER                Number of stations to show.
      --color / --no-color      Use colors on output
      --json                    Return JSON representation
      --help                    Show this message and exit.

Check the list of supported networks

.. code-block::

    $ cmdbikes ls
    Argentina [2]
    ├ Buenos Aires (Ecobici)
    └ Rosario (Mi bici tu bici)

    Australia [4]
    ├ Melbourne (Melbourne Bike Share)
    ├ Brisbane (CityCycle)
    ├ Curtin University, Perth, WA (Curtin Bike Share)
    └ Melbourne, AU (Monash BikeShare)

    Austria [23]
    ├ Wien (Citybike Wien)
    ├ Wachau (LEIHRADL)
    ...

