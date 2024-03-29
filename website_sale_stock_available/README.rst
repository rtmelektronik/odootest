============================
Website Sale Stock Available
============================

.. !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   !! This file is generated by oca-gen-addon-readme !!
   !! changes will be overwritten.                   !!
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

.. |badge1| image:: https://img.shields.io/badge/maturity-Beta-yellow.png
    :target: https://odoo-community.org/page/development-status
    :alt: Beta
.. |badge2| image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3
.. |badge3| image:: https://img.shields.io/badge/github-OCA%2Fe--commerce-lightgray.png?logo=github
    :target: https://github.com/OCA/e-commerce/tree/13.0/website_sale_stock_available
    :alt: OCA/e-commerce
.. |badge4| image:: https://img.shields.io/badge/weblate-Translate%20me-F47D42.png
    :target: https://translation.odoo-community.org/projects/e-commerce-13-0/e-commerce-13-0-website_sale_stock_available
    :alt: Translate me on Weblate
.. |badge5| image:: https://img.shields.io/badge/runbot-Try%20me-875A7B.png
    :target: https://runbot.odoo-community.org/runbot/113/13.0
    :alt: Try me on Runbot

|badge1| |badge2| |badge3| |badge4| |badge5| 

This module extends the functionality of 'Product Availability' module
(Technical name: website_sale_stock) so that for the 'Website shop' the
'Available' quantity of a product is taken into account instead of
'Forecasted' quantity.

This image shows where you can see those quantities:

.. image:: https://raw.githubusercontent.com/OCA/e-commerce/13.0/website_sale_stock_available/static/description/product_quantities.png
    :width: 600 px
    :alt: Product quantities

|

If a product is configured to 'prevent sales if not enough stock'
(see configuration section) and its page is accessed in the Website Shop,
the availability messages will be based on the 'Available' quantity instead of
'Forecasted' quantity. And also, the Website shop wont allow you to buy more
products than 'Available' quantity (not 'Forecasted' quantity is taken
into account).

**Table of contents**

.. contents::
   :local:

Configuration
=============

To configure this module, you need to:

#. Go to *Inventory > Master Data > Products* and edit a product that
   you only want to sell in the website shop if there is enough stock.
#. Navigate to 'Availability' field in the 'eCommerce' tab and set
   one of these options:

   * Show inventory on website and prevent sales if not enough stock
   * Show inventory below a threshold and prevent sales if not enough stock.
#. Go to *Inventory > Configuration > Settings*, navigate to *Stock available
   to promise* section and set the desired option. If you do not choose any,
   the value of 'Available' quantity will be equal to 'Forecasted' quantity.

Usage
=====

To use this module, you need to:

#. Go to your Website shop.
#. Select a product that you has previously configured to 'prevent sales
   if not enough stock' for the web product page.
#. Odoo doesn't allow you to add the product to the car if 'Available'
   quantity (not 'Forecasted' quantity) is equal or less than zero.
   Besides, availability messages will be based on the 'Available'
   quantity instead of the 'Forecasted' quantity.

.. image:: https://raw.githubusercontent.com/OCA/e-commerce/13.0/website_sale_stock_available/static/description/availability_message.png
    :width: 600 px
    :alt: Availability message

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/e-commerce/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed
`feedback <https://github.com/OCA/e-commerce/issues/new?body=module:%20website_sale_stock_available%0Aversion:%2013.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Do not contact contributors directly about support or help with technical issues.

Credits
=======

Authors
~~~~~~~

* Tecnativa

Contributors
~~~~~~~~~~~~

* `Tecnativa <https://www.tecnativa.com>`_:

  * Ernesto Tejeda
  * Pedro M. Baeza
  * Víctor Martínez

Maintainers
~~~~~~~~~~~

This module is maintained by the OCA.

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

This module is part of the `OCA/e-commerce <https://github.com/OCA/e-commerce/tree/13.0/website_sale_stock_available>`_ project on GitHub.

You are welcome to contribute. To learn how please visit https://odoo-community.org/page/Contribute.
