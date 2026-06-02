
def removing_invalid_payment_orders(olist_orders,olist_payments):
    op = olist_orders.merge(olist_payments,on = 'order_id',how = 'left')
    olist_orders = olist_orders[~olist_orders['order_id'].isin(op[(op['order_status'] == 'delivered') & (op['payment_type'].isna())]['order_id'])]
    return olist_orders

#olist_orders = removing_invalid_payment_orders(olist_orders,olist_payments)

def remove_invalid_cancelled_orders(olist_orders,olist_customers):
    oc = olist_orders.merge(olist_customers,on = 'customer_id',how = 'left')
    olist_orders = olist_orders[~olist_orders['order_id'].isin(oc[(oc['order_status'] == 'canceled') & (oc['order_delivered_customer_date'].notna())]['order_id'])]
    return olist_orders

#olist_orders = remove_invalid_cancelled_orders(olist_orders,olist_customers)

def remove_customers_without_orders(olist_customers,olist_orders):
    olist_customers = olist_customers[~olist_customers.merge(olist_orders,on = 'customer_id',how = 'left')['order_id'].isna()]
    return olist_customers

#olist_customers = remove_customers_without_orders(olist_customers,olist_orders)
def remove_invalid_cancelled_orders_items(olist_orders,olist_order_items):
    olist_order_items = olist_order_items[olist_order_items['order_id'].isin(olist_orders['order_id'])]
    return olist_order_items



def product_change(olist_products,product_category_name_translations):
    op = olist_products.merge(product_category_name_translations,on = 'product_category_name')
    product_chn = op.drop(columns = 'product_category_name',inplace = True)
    
    product_chn = op['product_category_name_english'] =  op['product_category_name_english'].replace({'costruction_tools_garden':'construction_tools_garden','fashio_female_clothing':'fashion_female_clothing','home_confort':'home_comfort','costruction_tools_tools':'construction_tools_tools'})
    product_chn = op.rename(columns = {'product_category_name_english':'product_category'})
    import numpy as np

    category_map = {
    
        # Fashion
        'fashion_shoes':'Fashion',
        'fashion_bags_accessories':'Fashion',
        'fashion_underwear_beach':'Fashion',
        'fashion_male_clothing':'Fashion',
        'fashion_female_clothing':'Fashion',
        'fashion_sport':'Fashion',
        'fashion_childrens_clothes':'Fashion',
        'luggage_accessories':'Fashion',
    
        # Electronics & Tech
        'computers_accessories':'Electronics',
        'computers':'Electronics',
        'electronics':'Electronics',
        'telephony':'Electronics',
        'fixed_telephony':'Electronics',
        'tablets_printing_image':'Electronics',
        'consoles_games':'Electronics',
        'audio':'Electronics',
        'cine_photo':'Electronics',
    
        # Home & Furniture
        'furniture_decor':'Home_Furniture',
        'home_appliances':'Home_Furniture',
        'home_appliances_2':'Home_Furniture',
        'bed_bath_table':'Home_Furniture',
        'housewares':'Home_Furniture',
        'office_furniture':'Home_Furniture',
        'furniture_living_room':'Home_Furniture',
        'furniture_bedroom':'Home_Furniture',
        'furniture_mattress_and_upholstery':'Home_Furniture',
        'kitchen_dining_laundry_garden_furniture':'Home_Furniture',
        'home_comfort':'Home_Furniture',
        'home_comfort_2':'Home_Furniture',
        'small_appliances':'Home_Furniture',
        'small_appliances_home_oven_and_coffee':'Home_Furniture',
        'air_conditioning':'Home_Furniture',
    
        # Construction & Tools
        'construction_tools_safety':'Construction_Tools',
        'construction_tools_construction':'Construction_Tools',
        'construction_tools_tools':'Construction_Tools',
        'construction_tools_lights':'Construction_Tools',
        'construction_tools_garden':'Construction_Tools',
        'garden_tools':'Construction_Tools',
        'home_construction':'Construction_Tools',
    
        # Books & Media
        'books_general_interest':'Books_Media',
        'books_technical':'Books_Media',
        'books_imported':'Books_Media',
        'dvds_blu_ray':'Books_Media',
        'cds_dvds_musicals':'Books_Media',
        'music':'Books_Media',
    
        # Food & Drinks
        'food':'Food_Drinks',
        'food_drink':'Food_Drinks',
        'drinks':'Food_Drinks',
        'la_cuisine':'Food_Drinks',
    
        # Kids & Baby
        'baby':'Kids_Baby',
        'toys':'Kids_Baby',
        'diapers_and_hygiene':'Kids_Baby',
    
        # Health & Beauty
        'health_beauty':'Health_Beauty',
        'perfumery':'Health_Beauty',

        # Sports & Leisure
        'sports_leisure':'Sports_Leisure',
    
        # Pet Supplies
        'pet_shop':'Pet_Supplies',
    
        # Automotive
        'auto':'Automotive',
    
        # Office & Business
        'stationery':'Office_Business',
        'industry_commerce_and_business':'Office_Business',
        'market_place':'Office_Business',
        'agro_industry_and_commerce':'Office_Business',
    
        # Entertainment & Hobby
        'art':'Entertainment_Hobby',
        'arts_and_craftmanship':'Entertainment_Hobby',
        'musical_instruments':'Entertainment_Hobby',
        'cool_stuff':'Entertainment_Hobby',
        'party_supplies':'Entertainment_Hobby',
        'christmas_supplies':'Entertainment_Hobby',
        'flowers':'Entertainment_Hobby',
        'watches_gifts':'Entertainment_Hobby',
    
        # Security
        'signaling_and_security':'Security',
        'security_and_services':'Security',
    
        # Misc
        np.nan:'Unknown'
    }
    
    product_chn['product_category_map'] = product_chn['product_category'].map(category_map)
    product_chn
    
    return product_chn

def run_preprocessing(
    olist_orders,
    olist_payments,
    olist_customers,
    olist_order_items,
    olist_products,
    product_category_name_translations
):

    olist_orders = removing_invalid_payment_orders(
        olist_orders,
        olist_payments
    )

    olist_orders = remove_invalid_cancelled_orders(
        olist_orders,
        olist_customers
    )

    olist_customers = remove_customers_without_orders(
        olist_customers,
        olist_orders
    )

    olist_order_items = remove_invalid_cancelled_orders_items(
        olist_orders,
        olist_order_items
    )

    product_chn = product_change(
        olist_products,product_category_name_translations
    )

    return (
        olist_orders,
        olist_customers,
        olist_order_items,
        product_chn
    )