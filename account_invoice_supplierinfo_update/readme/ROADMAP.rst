This module does not manage correctly difference if

* invoice line taxes are not the same as products taxes. (If one is
  marked as tax included in the price and the other is marked as
  tax excluded in the price)
* Refactor that module to share algorithm with similar module
  `purchase_order_supplierinfo_update`
