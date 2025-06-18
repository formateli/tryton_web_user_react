#####################
Tryton Web User React
#####################

A simple frontend implementation for *Tryton Web User Module* using *React*.

`Tryton <https://tryton.org>`_ is business software, ideal for companies of any size, easy to use, complete and 100% Open Source.

This project take advange of the excelent `React Mega Tutorial <https://blog.miguelgrinberg.com/post/introducing-the-react-mega-tutorial>`_ for the frontend development.


Running ...
-----------

  - Tryton server must be `installed <https://docs.tryton.org/latest/server/topics/install.html#topics-install>`_ and runnig with `Web User <https://docs.tryton.org/latest/modules-web-user/index.html>`_ and `Web User Routes <https://github.com/formateli/trytond_web_user_routes>`_ modules.
  - Add cors entries in Tryton config file pointing to the react app server.

  .. code-block:: bash
    [cors]
    https:servername_or_ip:3000

  - Add an .env file in the react frontend folde with two variables:

  .. code-block:: bash

    TRYTON_SERVER=servername_or_ip:port
    TRYTON_DATABASE=database_name

  - Run the react app server

  .. code-block:: bash

    $ git clone https://github.com/formateli/tryton_web_user_react.git -b develop
    $ docker pull node:24-alpine
    $ docker run -p 3000:3000 -v <PATH>/tryton_web_user_react/frontend:/app -w /app -it node:24-alpine yarn start


