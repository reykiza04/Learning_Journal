SELECT founded_at, founded_at_clean
FROM crunchbase_companies_clean_data ;

# liat dulu, formatnya beda tuh. Si founded_at formatnya adalah UTC (bulan,tanggal, tahun)
# si founded_at_clean formatnya adalah tahun/bulan/tanggal
# type nya juga masih varchar, blm jadi format date 

SELECT founded_at,CONVERT(founded_at, DATE) as converted_at,
founded_at_clean, CONVERT(founded_at_clean, DATE) as converted_clean
FROM crunchbase_companies_clean_data ;

#liat di kolom converted_at itu berantakan formatnya karena date di founded_at nya gk ngikutin format asli maria db 
#jadi di benerin dulu urutan formatnya 

SELECT founded_at,
	STR_TO_DATE(founded_at, '%m/%d/%y') AS changed_format_at,
    founded_at_clean
FROM crunchbase_companies_clean_data ;


#####
ALTER TABLE crunchbase_companies_clean_data
modify column founded_at DATE; #ini hasilnya error karena format tanggal founded_at msh jelek 

###
ALTER TABLE crunchbase_companies_clean_data #bikin kolom baru
add column founded_at_bersih DATE; #ini null semua tapi di state formatnya date

UPDATE crunchbase_companies_clean_data 
SET founded_at_bersih = STR_TO_DATE(founded_at, '%m/%d/%y'); #di kolom foundedatbersih di update kolom founded at yang udah dirubah format 

alter table crunchbase_companies_clean_data
drop column founded_at; #ngapus kolom founded_at karena pake kolom baru diatas

select * from crunchbase_companies_clean_data; #select cuma preview aj, kalo alter nanti kita melakukan perubahan di dataset crunchbase_companies_clean_data
#resikonya, kalo salah ya ga bisa di recover tuh table (incase nge alter)


###########
select founded_at_bersih
from crunchbase_companies_clean_data
order by founded_at_bersih;
#karena formatnya udah date, maka dia ngurutinnya sudah rapi 
# tapi kalau kolom yg dipake adl kolom yg formatnya make string, tampilannya akan beda



