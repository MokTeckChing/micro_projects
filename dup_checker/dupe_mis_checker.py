# explanation: this is a quick set of functions written to show the differences between two sets of data based on the column "token". For this function to work, it is best if "tokens" are unique.

#function to extract missing rows and equalize datasets

def de_dupe_clean(df1, df2, namecol, token):

    # removing name columns (if datasets start off merged, and are differentiated by a column's value)
    
    try:
        df1.drop(columns = namecol, inplace = True)
    except:
        pass
    try:
        df2.drop(columns = namecol, inplace = True)
    except:
        pass
    
    # merging datasets to extract missing rows
    
    df_merged = pd.merge(df1, 
                         df2,
                         how = 'outer',
                         left_on = [token],
                         right_on = [token], 
                         indicator = True)

    # extract missing rows from df1
    
    df1_missing = df_merged[df_merged["_merge"] == "left_only"]
    df1_mis_token = list(df1_missing[token])
    
    # extract missing rows from df2
    
    df2_missing = df_merged[df_merged["_merge"] == "right_only"]
    df2_mis_token = list(df2_missing[token])
    
    # removing missing rows from both df1 and df2
    
    df1 = df1[~df1.token.isin(df1_mis_token)]
    df2 = df2[~df2.token.isin(df2_mis_token)]
    
    df1_clean = df1[~df1.token.isin(df1_mis_token)]
    df2_clean = df2[~df2.token.isin(df2_mis_token)]

    df1_clean.reset_index(drop = True, inplace = True)
    df2_clean.reset_index(drop = True, inplace = True)
    
    # comparing datasets
    
    changes = df1_clean.compare(df2_clean)
    
    # extracting tokens for rows with differences
    
    changes[token] = [df1_clean[token].iloc[i] for i in changes.index]
    
    return df1_mis_token, df2_mis_token, changes

# function to print different results based on whether there are changes

def de_dupe_check(df1, df2, namecol = "namecol", token = "token"):

    mis1, mis2, change = de_dupe_clean(df1, df2, namecol, token)

    # printing missing rows
    
    if len(mis1) > 0:
        print (f'The following tokens are missing from dataset 1: {mis1}')
    if len(mis2) > 0:
        print (f'The following tokens are missing from dataset 2: {mis1}')
    if len(mis1) == 0 and len(mis2) == 0:
        print ("number of rows are identical")

    # printing rows with differences
        
    print ("\n----------\n")
    if len(change) == 0 and len(mis1) == 0 and len(mis2) == 0:
        print ("datasets are identical")
    elif len(change) == 0:
        print ("other than missing rows, datasets are identical")
    else:
        print (change)
