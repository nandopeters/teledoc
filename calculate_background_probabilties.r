probs <- read.table('data/who_data_set.txt', header = TRUE,sep=",")
codes_to_names <- read.table('data/disease_code_to_name.txt', header = TRUE,sep=",")
# Probability for a dease by country P(D|C)
d_occured_over_all_countrys <- sqldf("select  GHO as id,sum(Display) as count_pre_disease  from probs group by GHO")

pe1<-sqldf("select REGION, COUNTRY, GHO, sum(p.Display)/oc.count_pre_disease as probability, sum(p.Display), oc.count_pre_disease from probs p inner join d_occured_over_all_countrys as oc on (oc.id == p.GHO) group by COUNTRY,GHO order by REGION,COUNTRY,GHO")

result <- sqldf("select * from  pe1 inner join codes_to_names cn on (cn.code == pe1.GHO) order by REGION,COUNTRY,GHO ")
write.table(result,file="data/disease_prob_for_country.txt",sep=",")
pe1<-sqldf("select  REGION,sum(Numeric)  from probs group by REGION")
