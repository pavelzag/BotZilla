import bugzilla
import configuration
import logging

URL = configuration.get_config(parameter_type='bugzilla-creds', parameter_name='bugzilla-url')
bzapi = bugzilla.Bugzilla(URL)
default_product = configuration.get_config(parameter_type='default-params', parameter_name='default_product')
default_component = configuration.get_config(parameter_type='default-params', parameter_name='default_component')


def normalize_component_new(selected_component, selected_product):
    # TODO Temporary fix. Figure out why sometimes None product
    print('default product is: ' + default_product + ' and default component is: ' + default_component)
    if not selected_product:
        selected_product = default_product
    components = bzapi.getcomponents(product=selected_product)
    print(components)
    lowered_components = [item.lower() for item in components]
    if not selected_component:
        return ''
    if selected_component in lowered_components:
        index = lowered_components.index(selected_component)
        return components[index]


def normalize_product_new(selected_product):
    if not selected_product:
        selected_product = default_product.lower()
    include_fields = ["name", "id"]
    products = bzapi.getproducts(include_fields=include_fields)
    logging.debug('The selected product is : ' + selected_product)
    products_list = []
    # Converting products dictionary to products list with product names
    for product in products:
        single_product1 = str(list(product.values())[0])
        single_product2 = str(list(product.values())[1])
        # Check which of the values is string and select only the string
        if not isproductalpha(single_product1) and not isproductalpha(single_product2):
            print('name and id are numbers, need to skip this product ' + single_product1 + " " + single_product2)
        else:
            if single_product1.isalpha():
                single_product = single_product1
            else:
                single_product = single_product2
            products_list.append(single_product)
    lowered_products = [item.lower() for item in products_list]
    if selected_product in lowered_products:
        index = lowered_products.index(selected_product)
        return products_list[index]
    else:
        print('something\'s wrong')


def isproductalpha(product):
    # TODO Fix this ugly monstrosity
    if ' ' in product:
        return True
    elif '-' in product:
        return True
    elif '.' in product:
        return True
    elif '_' in product:
        return True
    elif product.isalpha():
        return True
    else:
        return False