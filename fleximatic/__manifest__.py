# -*- coding: utf-8 -*-
{
    'name': "Fleximatic",

    'summary': """
        New features Odoo""",

    'description': """
        Inherit some views , new views , reports
    """,

    'author': "Estrasol -Kevin Daniel del Campo",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','product','sale','stock','sale_margin','sale_management','purchase'
    ,'stock_picking_batch'],

    # always loaded
    'data': [
    #Views
        'views/sale/sale.xml',
        'views/pricelist/pricelist.xml',
        'views/product/product.xml',
        'views/product/product_product.xml',
        'views/templates/templates.xml',
        'views/stock/stock_batch_picking.xml',
        'views/purchase/purchase.xml',
        'views/stock/stock_picking.xml',
        #WIZARDS
        'wizard/sale_details.xml',
        'wizard/promotional_products.xml',
        'wizard/warning_client.xml',

    ],  
     'qweb': [
        
         ]
        ,
    'demo': [
    ],
    'application': True,
}
