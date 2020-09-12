import pandas as pd
import sys
LEN_ARGV = 4
def get_inputs(argv):
    inputs = {}

    for i in range(1, len(argv), 2):
       inputs[argv[i-1]] = argv[i]
    return inputs

def parse_inputs(inputs):
    min_date = "2020-01-01"
    max_date = "2020-06-30"
    top = 3
    try:
        min_date = inputs["--min-date"]
        pass
    except Exception as e:
        print(f"[INFO] You did not set {e}. It will be used {min_date}")
        pass

    try:
        max_date = inputs["--max-date"]
        pass
    except Exception as e:
        print(f"[INFO] You did not set {e}. It will be used {max_date}")
        pass

    try:
        top = int(inputs["--top"])
        pass
    except Exception as e:
        print(f"[INFO] You did not set {e}. It will be used {top}")
        pass

    return min_date, max_date, top


inputs = get_inputs(sys.argv[1:])
min_date, max_date, top = parse_inputs(inputs)

product_fname = "product.csv"
sales_fname = "sales.csv"
store_fname = "store.csv"

product_df = pd.read_csv(product_fname)
sales_df = pd.read_csv(sales_fname)
store_df = pd.read_csv(store_fname)

date_mask = ((sales_df["date"] >= min_date) &
             (sales_df["date"] <= max_date))

masked_sales_df = sales_df[date_mask]


# -- top seller product --
top_seller_product_df = masked_sales_df.loc[:, ["product", "quantity"]]\
                                        .groupby("product")\
                                        .sum()\
                                        .nlargest(top, 'quantity', keep="all")

top_seller_product_df = pd.merge(top_seller_product_df,
                                 product_df,
                                 left_on="product", 
                                 right_on="id")\
                            .loc[:, ["name", "quantity"]]

# -- top seller store --
top_seller_store_df = masked_sales_df.loc[:, ["store", "quantity"]]\
                                     .groupby("store")\
                                     .sum()\
                                     .nlargest(top, 'quantity', keep="all")

top_seller_store_df = pd.merge(top_seller_store_df,
                               store_df, 
                               left_on="store", 
                               right_on="id")\
                        .loc[:, ["name", "quantity"]]
 
#-- top seller brand --
top_seller_brand_df = pd.merge(masked_sales_df,
                               product_df, 
                               left_on="product", 
                               right_on="id")\
                        .loc[:, ["brand", "quantity"]]

top_seller_brand_df = top_seller_brand_df.groupby("brand")\
                                         .sum()\
                                         .nlargest(top, 'quantity', keep="all")

# -- top seller city --
top_seller_city_df = pd.merge(masked_sales_df, 
                              store_df, 
                              left_on="store", 
                              right_on="id")\
                        .loc[:, ["city", "quantity"]]

top_seller_city_df = top_seller_city_df.groupby("city")\
                                        .sum()\
                                        .nlargest(top, 'quantity', keep="all")


# print results
print("-- top seller product --")
print(top_seller_product_df)

print("-- top seller store --")
print(top_seller_store_df)

print("-- top seller brand --")
print(top_seller_brand_df)

print("-- top seller city --")
print(top_seller_city_df)