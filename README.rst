#####################
Tryton Web User React
#####################

A simple frontend for *Tryton Web User Module* using *React*.

        - Tryton server as an API backend.
        - User Login and Registration process.
        - Email user verification and password change.
        - User Authentication and Autorization (token management).

`Tryton <https://tryton.org>`_ is business software, ideal for companies of any size, easy to use, complete and 100% Open Source.

Thanks to the excelent `React Mega Tutorial <https://blog.miguelgrinberg.com/post/introducing-the-react-mega-tutorial>`_ used in the learning process for the frontend design and development.

Running ...
-----------

  - Tryton server must be `installed <https://docs.tryton.org/latest/server/topics/install.html#topics-install>`_ and runnig with `Web User <https://docs.tryton.org/latest/modules-web-user/index.html>`_ and `Web User Routes <https://github.com/formateli/trytond_web_user_routes>`_ modules installed in all databases.
    
  - Add `cors entries <https://docs.tryton.org/latest/server/topics/configuration.html#cors>`_ in Tryton config file pointing to the react app server.
    
  - Add an .env file in the react frontend folde with following variables:

  .. code-block:: bash

    REACT_APP_TRYTON_SERVER=servername_or_ip:port
    REACT_APP_TRYTON_DATABASE=database_name

  - Run the react app server

  .. code-block:: bash

    $ git clone https://github.com/formateli/tryton_web_user_react.git -b develop
    $ docker pull node:24-alpine
    $ docker run -p 3000:3000 -v ./tryton_web_user_react/frontend:/app -w /app -it node:24-alpine yarn start


