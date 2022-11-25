from django.shortcuts import render
import pandas as pd




def question_1(request):
    df_listings = pd.read_csv("listings.csv")
    df_reviews = pd.read_csv("reviews.csv")
    number_of_reviews = df_listings[['number_of_reviews']].groupby(df_listings.neighbourhood_cleansed).sum()
    number_of_reviews["number_of_host"] = df_listings['host_id'].groupby(df_listings.neighbourhood_cleansed).nunique()

    df_listings['host_acceptance_rate'] = df_listings['host_acceptance_rate'].str.rstrip("%").astype(float)
    df_listings['host_response_rate'] = df_listings['host_response_rate'].str.rstrip("%").astype(float)
    mean_acceptance= df_listings['host_acceptance_rate'].mean()
    mean_response= df_listings['host_response_rate'].mean()

    df_listings["phone"] = df_listings["host_verifications"].apply(lambda x: "1" if "phone" in x else "0")
    phone_pourcentage = df_listings["phone"].astype('int').sum()/len (df_listings["phone"])
    df_listings.host_verifications.replace(to_replace = 'work_email', value = 'work' )
    df_listings["work"] = df_listings["host_verifications"].apply(lambda x: "1" if "work" in x else "0")
    work_pourcentage = df_listings["work"].astype('int').sum()/len (df_listings["work"])
    df_listings["email"] = df_listings["host_verifications"].apply(lambda x: "1" if "email" in x else "0")
    email_pourcentage = df_listings["email"].astype('int').sum()/len (df_listings["email"])

    df_listings["number_of_amenities"] =df_listings.amenities.str.count(',')
    df_listings["number_of_amenities"] =df_listings.number_of_amenities.astype(int)
    df_listings["number_of_amenities"] = df_listings.number_of_amenities.apply(lambda x:x+1)
    amenities= df_listings.groupby(df_listings.room_type).number_of_amenities.agg(["mean","std"])

    df_listings["price"] = df_listings["price"].str.replace("$","").str.replace(",","").astype("float")
    price = df_listings["price"].groupby(df_listings.room_type).describe()
    price=price.drop(["count","mean","std"], axis=1)

    df_bath= df_listings["bathrooms_text"]
    df_bath = df_bath.dropna()
    df_bath = df_bath.str.replace("baths","bath").str.replace("-"," ").str.replace("Private","private bath").str.replace("Bath","bath").str.replace("Half","half bath").str.replace("Shared","shared bath").str.replace("private bath", "2").str.replace("shared bath","0.5").str.replace("half bath","0.5").str.replace("bath","1")
    df_listings[["num","type"]] = df_bath.str.split(" ",1,expand=True)
    df_listings["num"] = df_listings["num"].astype("float")
    df_listings["type"] = df_listings["type"].astype("float")
    df_listings["result"] = df_listings["type"] * df_listings["num"]
    bath = df_listings.num.groupby(df_listings.result).count()

    df_listings["description"] = df_listings["description"].astype("string")
    df_listings = df_listings.dropna(subset="description")
    df_listings["description_length"] = df_listings["description"].apply(len)
    coorelation = df_listings["description_length"].corr(df_listings["number_of_reviews"])

    df_merge = df_listings.merge(df_reviews, how='inner', left_on = 'id', right_on = 'listing_id')
    faux_commentaire = df_merge[df_merge["host_name"]==df_merge["reviewer_name"]].shape[0]
    faux_commentaire = faux_commentaire/len(df_merge)*100

    return render(request,  "city/list_question.html", {'question1':number_of_reviews.to_html,
                                                            'acceptance':mean_acceptance, 
                                                            'response': mean_response, 
                                                            'phone':phone_pourcentage, 
                                                            'work':work_pourcentage, 
                                                             'email':email_pourcentage, 
                                                                  'amenities':amenities.to_html, 
                                                                'price':price.to_html, 
                                                              'bath':bath,
                                                             'corelation':coorelation, 
                                                             'faux':faux_commentaire 
                                                             })


   