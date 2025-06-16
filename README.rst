#####################
Tryton Web User React
#####################

A simple frontend implementation for *Tryton Web User Module* using *React*.

`Tryton <https://tryton.org>`_ is business software, ideal for companies of any size, easy to use, complete and 100% Open Source.

This project take advange of the excelent `React Mega Tutorial <https://blog.miguelgrinberg.com/post/introducing-the-react-mega-tutorial>`_.


Running with docker
-------------------

  .. code-block:: bash

    $ git clone https://github.com/formateli/tryton_web_user_react.git -b develop
    $ docker pull node:24-alpine
    $ docker run -p 3000:3000 -v <PATH>/tryton_web_user_react/frontend:/app -w /app -it node:24-alpine yarn start


