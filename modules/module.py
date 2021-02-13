import pandas as pd 
import re

# Setup methods

def cat_var(df, cols):
    cat_list = []
    for col in cols:
        cat = df[col].unique()
        cat_num = len(cat)
        cat_dict = {"categorical_variable":col,
                    "number_of_possible_values":cat_num,
                    "values":cat}
        cat_list.append(cat_dict)
    df = pd.DataFrame(cat_list).sort_values(by="number_of_possible_values", ascending=False)
    return df.reset_index(drop=True)

def cause_types(cause):
    pattern = '\d+-\d+'
    x = re.findall(pattern, cause)
    if len(x) == 0:
        return 'Single cause'
    else:
        return 'Multiple causes'

def cause_code(text):
    return text.split(" ", 1)[0]

def cause_name(text):
    return text.split(" ", 1)[1].strip()


# Transformation methods

def row_filter(df, cat_var, cat_values):
    df = df[df[cat_var].isin(cat_values)].sort_values(by='Total', ascending=False)
    return df.reset_index(drop=True)

def nrow_filter(df, cat_var, cat_values):
    df = df[~df[cat_var].isin(cat_values)].sort_values(by='Total', ascending=False)
    return df.reset_index(drop=True)

def groupby_sum(df, group_vars, agg_var='Total', sort_var='Total'):
    df = df.groupby(group_vars, as_index=False).agg({agg_var:'sum'})
    df = df.sort_values(by=sort_var, ascending=False)
    return df.reset_index(drop=True)

def pivot_table(df, col, x_axis, value='Total'):
    df = df.pivot_table(values=value,
                        columns=col,
                        index=x_axis,
                        aggfunc='sum')
    return df.reset_index()