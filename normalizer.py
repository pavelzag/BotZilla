import bugzilla
import configuration
import logging

URL = configuration.get_config(parameter_type='bugzilla-creds', parameter_name='bugzilla_url')
bzapi = bugzilla.Bugzilla(URL)
default_product = configuration.get_config(parameter_type='default-params', parameter_name='default_product')
default_component = configuration.get_config(parameter_type='default-params', parameter_name='default_component')


def normalize_component_new(selected_component, selected_product):
    # TODO Temporary fix. Figure out why sometimes None product
    # print('default product is: ' + default_product + ' and default component is: ' + default_component)
    if not selected_product:
        selected_product = default_product
    components = bzapi.getcomponents(product=selected_product)
    lowered_components = [item.lower() for item in components]
    if not selected_component:
        return ''
    if selected_component in lowered_components:
        index = lowered_components.index(selected_component)
        return components[index]
    else:
        print('selected component is not in there')


def normalize_product_new(selected_product):
    if not selected_product:
        selected_product = default_product
    include_fields = ["name", "id"]
    products = bzapi.getproducts(include_fields=include_fields)
    products_list = []
    for product in products:
        single_product1 = str(list(product.values())[0])
        single_product2 = str(list(product.values())[1])
        if not isproductalpha(single_product1) and not isproductalpha(single_product2):
            print('name and id are numbers, need to skip this product ' + single_product1 + " " + single_product2)
        else:
            if isproductalpha(single_product1):
                single_product = single_product1
            else:
                single_product = single_product2
            products_list.append(single_product)
    lowered_products = [item.lower() for item in products_list]
    if selected_product.lower() in lowered_products:
        index = lowered_products.index(selected_product.lower())
        return products_list[index]
    else:
        print('something\'s wrong')


def isproductalpha(product):
    # TODO Fix this ugly stuff
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